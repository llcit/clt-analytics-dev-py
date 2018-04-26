from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

import analytics.settings

def index(request):
    return render(request, 'index.html')

def local_login(request):
    context = {'request': request}
    return render(request, 'login.html', context)


def local_login_handler(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')

    errormsg = 'The username and password were incorrect.'
    if request.POST:
        u = request.POST['username']
        p = request.POST['passwd']
        user = authenticate(username=u, password=p)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('review')
                # return render_to_response('index.html', context_instance=RequestContext(request))
            else:
                errormsg = 'Sorry, your account has been disabled.'

    return render(request, 'login.html', {'errormsg': errormsg})
