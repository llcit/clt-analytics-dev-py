from django.conf.urls import include, url
from  .views import *

urlpatterns = [
    url(r'^$', securehome, name='review'),
    url(r'^resp/$', respond),
    url(r'^respclear/$', clearResponse),
    url(r'^comm/$', writeComment),
    url(r'^respprep/$', submitPrep),
    url(r'^info/(\d+)$', displayReviewInfo), # Note toggle results presented
    url(r'^info/print/(\d+)$', printReviewReport),
    url(r'^prep/(\d+)$', preSurvey),
    url(r'^report/(\d+)$', reportReview),
    url(r'^report/unsubmit/(\d+)$', reportReviewunsubmit),
    url(r'^(\d+)$', displayReviewQuestions),  # Note toggle
    url(r'^register/(\w+)/$', registerReview),  # URL for register access code, assign current user as reviewer of this("accesscode") review
    url(r'^registerInstructor/(\w+)/$', registerReviewforInstructor),  # URL for register access code, assign current user as instructor of this("accesscode") review
]
