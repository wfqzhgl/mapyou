# -*-coding:utf-8-*-

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.contrib.auth.views import logout
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
import logging
import urllib
import urlparse

from forms import *
from models import *
from utils import *
# Create your views here.


@csrf_protect
def login_custom(request):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]
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
    log_names = settings.CLIENT_LOG_TYPE_NAMES
    log_columns = settings.CLIENT_LOG_COLUMNS
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

class BHistoryView(ListView):
    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        self.paginate_by = self.kwargs.get('numperpage') or self.request.GET.get('numperpage') or settings.DEFAULT_NUM_PER_PAGE
        return self.paginate_by  # objects per page

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BHistoryView, self).get_context_data(**kwargs)
        context['request'] = self.request
        uid = self.kwargs.get('uid', '0')
        context['uid'] = uid
        if uid and uid != '0':
            context['patient'] = Patient.objects.get(id=uid)
        return context
    
    def get_queryset(self):
        uid = self.kwargs.get('uid', '0')
        if not uid or uid == '0':
            return BHistory.objects.all().order_by('-id')
        return BHistory.objects.filter(patient__id=uid).order_by('-id')
#    context_object_name = "book_list"  ##default as object_list
#     queryset = BHistory.objects.filter(patient__id=).order_by('-id')
#    template_name = "collect/gest_list.html"



class BtypeCreate(CreateView):
    model = BType
    template_name_suffix = "_create_form"
    success_url = "/bingli/btypes/"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BtypeCreate, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
    
    
class BHistoryCreate(CreateView):
    model = BHistory
    template_name_suffix = "_create_form"

    def get_form_kwargs(self):
        kwargs = super(BHistoryCreate, self).get_form_kwargs()
        uid = self.kwargs.get('uid', '0')
        if uid and uid != '0':
            patient = Patient.objects.get(id=uid)
            kwargs['initial'].update({'patient':patient})
        return kwargs
        
    def get_context_data(self, **kwargs):
        
        uid = self.kwargs.get('uid', '0')
#         patient = Patient.objects.get(id=uid)
#         f = kwargs.get('form')
        # Call the base implementation first to get a context
        context = super(BHistoryCreate, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['uid'] = uid
        return context
    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        uid = self.kwargs.get('uid', '0')
        return "/bingli/histories/%s/" % uid
    
class PatientCreate(CreateView):
    model = Patient
    template_name_suffix = "_create_form"
    success_url = "/bingli/index/"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatientCreate, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
     
class BcateCreate(CreateView):
    model = BCategory
    template_name_suffix = "_create_form"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BcateCreate, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
#     def form_valid(self, form):
#         self.object = form.save()
#         if 'intro_pic' in self.request.FILES:
#             file=self.request.FILES['intro_pic']
#             filename=gen_file_name(file)  #生成文件 
#             handle_uploaded_file(os.path.join(settings.MEDIA_ROOT,filename),file)
# #            saveurl=re.sub(r'\\','/',os.path.join(settings.MEDIA_URL,filename))
#             saveurl='/media/'+filename
#             self.object.intro_pic=saveurl
#             self.object.intro_pic_cdn=get_cdn_url(settings.MEDIA_URL+saveurl)
#             self.object.save()
#         return super(BcateCreate, self).form_valid(form)
    success_url = "/bingli/bcates/"


class BcateUpdate(UpdateView):
    model = BCategory
    template_name_suffix = "_update_form"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BcateUpdate, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
    def get_success_url(self):
        """
        Returns the supplied URL.
        """
#         pk = self.kwargs.get('pk', '0')
        return "/bingli/bcates/"
    
    
class BtypeUpdate(UpdateView):
    model = BType
    template_name_suffix = "_update_form"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BtypeUpdate, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
    def get_success_url(self):
        """
        Returns the supplied URL.
        """
#         pk = self.kwargs.get('pk', '0')
        return "/bingli/btypes/"
    
class PatientUpdate(UpdateView):
    model = Patient
    template_name_suffix = "_update_form"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatientUpdate, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
    def get_success_url(self):
        """
        Returns the supplied URL.
        """
#         pk = self.kwargs.get('pk', '0')
        return "/bingli/index/"
    
    
class BHistoryUpdate(UpdateView):
    model = BHistory
    template_name_suffix = "_update_form"
    def get_context_data(self, **kwargs):
        uid = self.kwargs.get('uid', '0')
        # Call the base implementation first to get a context
        context = super(BHistoryUpdate, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['uid'] = uid
        return context
    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        pk = self.kwargs.get('pk', '0')
        return "/bingli/histories/%s/" % BHistory.objects.get(id=pk).patient.id
#    success_url=""
#     def form_valid(self, form):
#         self.object = form.save()
#         
#         if 'intro_pic' in self.request.FILES:
#             file=self.request.FILES['intro_pic']
#             filename=gen_file_name(file)  #生成文件 
#             handle_uploaded_file(os.path.join(settings.MEDIA_ROOT,filename),file)
# #            saveurl=re.sub(r'\\','/',os.path.join(settings.MEDIA_URL,filename))
#             saveurl='/media/'+filename
#             self.object.intro_pic=saveurl
#             self.object.intro_pic_cdn=get_cdn_url(settings.MEDIA_URL+saveurl)
#             self.object.save()
#         return super(BHistoryUpdate, self).form_valid(form)
    
        
class BcateView(ListView):
    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        self.paginate_by = self.kwargs.get('numperpage') or self.request.GET.get('numperpage') or settings.DEFAULT_NUM_PER_PAGE
        return self.paginate_by  # objects per page

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BcateView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
#    context_object_name = "book_list"  ##default as object_list
    queryset = BCategory.objects.all().order_by('-id')
#    template_name = "collect/gest_list.html"

class PatientView(ListView):
    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        self.paginate_by = self.kwargs.get('numperpage') or self.request.GET.get('numperpage') or settings.DEFAULT_NUM_PER_PAGE
        return self.paginate_by  # objects per page

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PatientView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
#    context_object_name = "book_list"  ##default as object_list
    queryset = Patient.objects.all().order_by('-id')
#    template_name = "collect/gest_list.html"
  
class BtypeView(ListView):
    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        self.paginate_by = self.kwargs.get('numperpage') or self.request.GET.get('numperpage') or settings.DEFAULT_NUM_PER_PAGE
        return self.paginate_by  # objects per page

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BtypeView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
#    context_object_name = "book_list"  ##default as object_list
    queryset = BType.objects.all().order_by('-id')
#    template_name = "collect/gest_list.html"


@login_required
def list_history(request):
    return HttpResponse('history')
