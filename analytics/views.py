from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

import analytics.settings

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def login_select(request):
    return render_to_response('login_select.html', context_instance=RequestContext(request))

def local_login(request):
    if request.POST:
        print request.POST
        u = request.POST['username']
        p = request.POST['passwd']
        user = authenticate(username=u, password=p)

        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")

            login(request, user)
            return render_to_response('index.html', context_instance=RequestContext(request))

        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

    return render_to_response('index.html', context_instance=RequestContext(request))
