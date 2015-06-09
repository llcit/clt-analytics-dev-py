from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

import analytics.settings


def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


def local_login(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', context_instance=RequestContext(request))

    return render_to_response('login.html', context_instance=RequestContext(request))


def local_login_handler(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', context_instance=RequestContext(request))

    errormsg = 'The username and password were incorrect.'
    if request.POST:
        u = request.POST['username']
        p = request.POST['passwd']
        user = authenticate(username=u, password=p)

        if user is not None:
            if user.is_active:
                login(request, user)
                print 'user authenticated'
                return render_to_response('index.html', context_instance=RequestContext(request))
            else:
                errormsg = 'Sorry, your account has been disabled.'

    return render_to_response('login.html', {'errormsg': errormsg}, context_instance=RequestContext(request))
