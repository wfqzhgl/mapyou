# -*-coding:utf8-*-
from django.shortcuts import render
import csv
import os
from datetime import date, timedelta
from django.views.decorators.http import condition
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import logging
import urlparse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.contrib.auth.views import logout
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.core.urlresolvers import reverse

import json

from forms import *

# Create your views here.

# @login_required
def index(request):
    return render_to_response('app/index.html', locals(), RequestContext(request))


@csrf_protect
def login_custom(request):
    print request.REQUEST
    redirect_to = request.GET.get(REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print 'redirect_to=', redirect_to
            netloc = urlparse.urlparse(redirect_to)[1]
            print 'netloc=', netloc
            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL
            auth_login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            print 'redirect_to=', redirect_to
            return HttpResponseRedirect(redirect_to)
    else:
        if request.user.is_authenticated():
            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            return HttpResponseRedirect(redirect_to)
        form = AuthenticationForm(request)

    request.session.set_test_cookie()
    current_site = get_current_site(request)
    context = {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    return render_to_response('admin/login.html', locals(), RequestContext(request))


def logout_custom(request):
    return logout(request)


def password_change(request, template_name='registration/password_change_form.html'):
    """
            修改密码
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Password successfully changed.")
    else:
        form = PasswordChangeForm(request.user)
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

