from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User





class CommonExtras:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    'https://clt.manoa.hawaii.edu/lib/js/dojo/dojo.js',
  )
  css = {
    'all': ('https://clt.manoa.hawaii.edu/lib/js/dojo/dojo.css',),
  }

