from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Min, Sum, Avg
from django.contrib.auth.models import User
from datetime import datetime
from review.models import *

from django.conf import settings
import pytz
import json

@login_required
def securehome(request):
    if request.GET.get('ticket'):
        return HttpResponseRedirect("https://authn.hawaii.edu//cas/validate?service=https://llc.manoa.hawaii.edu/analytics&ticket=%s"%request.GET.get('ticket'))
    else:
        reviews = Review.objects.filter(reviewers = request.user)
        courses = Review.objects.filter(instructors = request.user)
        reports = Review.objects.filter(reviewreportstatus__reviewer = request.user)
        responses = Review.objects.filter(reviewresponse__user = request.user).annotate(cnt=Count('reviewresponse__review'))
        reports_submit_status = ReviewReportStatus.objects.filter(reviewer = request.user)#.filter(review__id = rev)
        thedate = datetime(2012, 5, 18, 13, 0, 49, 0, pytz.UTC)
        #import pdb; pdb.set_trace()
        return render(request, 'review-index.html',
                                  {'reviews' : reviews,
                                   'courses' : courses,
                                   'reports' : reports.all(),
                                   'responses' : responses,
                                   'reports_submit_status' : reports_submit_status,
                                   'thedate' : thedate}
                                  )

@login_required
def displayReviewQuestions(request, rev):
    review = Review.objects.get(pk=rev)
    sections = ReviewSurvey.objects.get(review__id=rev).questionSections
    review_reportstatus=ReviewReportStatus.objects.filter(review__id = rev).filter(reviewer__id = request.user.id)
    if review_reportstatus:
        submitted = ReviewReportStatus.objects.filter(review__id = rev).filter(reviewer__id = request.user.id)[0].submitdate
        if submitted == datetime(2012, 5, 18, 13, 0, 49, 0,pytz.UTC):
            submitted = False
    else:
        submitted = False
    # This query returns a dictionary. In the template, its iterated to determine the match between question and selected option.
    # Seems highly inefficient but will have to work for now.

    responses = ReviewResponse.objects.filter(user__id = request.user.id).filter(review__id = rev).values("question", "response")

    comments = ReviewComment.objects.filter(user__id = request.user.id).filter(review__id = rev).order_by("section__rank")

    accessors =  review.reviewers.all()
    instructors = review.instructors.all()
    #import pdb; pdb.set_trace()
    if request.user not in accessors and request.user not in instructors:
        return HttpResponseRedirect('/analytics')

    return render(request, 'review.html',
                              {
                               'review' : review,
                               'sections' : sections,
                               'responses': responses,
                               "comments": comments,
                               "submitted":submitted
                               }
                               )

@login_required
def displayReviewInfo(request, rev):
    review = Review.objects.get(pk=rev)
    reviewers = review.reviewers.all()
    reviewer_responses = review.responses()
    instructors = review.instructors.all()
    questions = review.questions()

    response_matrix = []

    for q in questions:
        # Build a question response object [<QUESTION OBJECT>, [<QUESTION RESPONSE OBJECT LIST>]]
        question_response_obj = []
        question_response_obj.append(q)

        question_responses = reviewer_responses.filter(question=q).order_by('user')
        question_response_list = []
        for reviewer in reviewers:
            # Build a response object for a user
            reviewer_response_obj = []
            reviewer_response_obj.append(reviewer)
            try:
                reviewer_response = question_responses.get(user=reviewer)
            except:
                reviewer_response = 0
            reviewer_response_obj.append(reviewer_response)

            # Add response object to list of responses to this question
            question_response_list.append(reviewer_response_obj)


        question_response_obj.append(question_response_list)
        response_matrix.append(question_response_obj)

    survresp = SurveyResponse.objects.filter(review__id = review.id)
    reviewersreport = ReviewReportStatus.objects.filter(review__id = rev).values("reviewer")

    return render(request, 'review-info.html', {
                              'review' : review,
                              'reviewers': reviewers,
                              'instructors': instructors,
                              "survresponses": survresp,
                              "report": reviewersreport.all(),
                              'response_matrix': response_matrix
                              }
                              )

@login_required
def printReviewReport(request, rev):
    review = Review.objects.get(pk=rev)
    reviewers = review.reviewers.all()
    reviewer_responses = review.responses()
    instructors = review.instructors.all()
    questions = review.questions()
    comments = ReviewComment.objects.filter(review=review).order_by('section__rank', 'user')

    response_matrix = []
    for q in questions:
        # Build a question response object [<QUESTION OBJECT>, [<QUESTION RESPONSE OBJECT LIST>]]
        question_response_obj = []
        question_response_obj.append(q)

        question_responses = reviewer_responses.filter(question=q).order_by('user')
        question_response_list = []
        for reviewer in reviewers:
            # Build a response object for a user
            reviewer_response_obj = []
            reviewer_response_obj.append(reviewer)
            try:
                reviewer_response = question_responses.get(user=reviewer)
            except:
                reviewer_response = 0
            reviewer_response_obj.append(reviewer_response)

            # Add response object to list of responses to this question
            question_response_list.append(reviewer_response_obj)


        question_response_obj.append(question_response_list)
        response_matrix.append(question_response_obj)


    return render(request, 'review-print.html', {
                              'review' : review,
                              'reviewers': reviewers,
                              'instructors': instructors,
                              'comments': comments,
                              'response_matrix': response_matrix
                              }
                              )


@login_required
def preSurvey(request, rev):
    review = Review.objects.get(pk=rev)
    #responses = SurveyResponse.objects.filter(review__id = rev).annotate(res = Count("question__text"))
    responses = SurveyResponse.objects.filter(review__id = rev)

    print (responses)
    return render(request, 'survey.html',
                              {'review': review,
                               'survey' : review.presurv.questions,
                               'responses': responses}
                               )

@login_required
def reportReview(request, rev):
    report = ReviewReportStatus.objects.filter(reviewer__id = request.user.id).filter(review__id = rev)
    if not report:
        report = ReviewReportStatus()
        report.review = Review.objects.get(pk=rev)
        report.reviewer = request.user
        report.submitdate = datetime.now()
        report.save()
    else:
        report = report[0]
        report.submitdate = datetime.now()
        report.save()

    # Take user back to their review home.
    return HttpResponseRedirect('%s/review'%settings.SITE_ROOT)

#This is for the access code,assign current user as reviewer of this("accesscode") review
@login_required
def registerReview(request, accesskey):
    try:
        review = Review.objects.filter(accesscode = accesskey)[0]
    except:
        review = None

    if not review:
        return HttpResponseRedirect('/analytics')
    reviewers = review.reviewers.all()

    if review.isReviewer(request.user):
        return HttpResponseRedirect('%s/review/%s' %(settings.SITE_ROOT,review.id) )
    else:
        #import pdb; pdb.set_trace()
        review.reviewers.add(request.user)
        review.save()
        return HttpResponseRedirect('%s/review/%s' %(settings.SITE_ROOT,review.id) )



# URL for register access code, assign current user as instructor of this("accesscode") review
@login_required
def registerReviewforInstructor(request, accesskey):
    review = Review.objects.filter(accesscode = accesskey)[0]

    if not review:
        return HttpResponseRedirect('/analytics')
    instructors = review.instructors.all()

    if review.isInstructor(request.user):
        return HttpResponseRedirect('%s/review/%s' %(settings.SITE_ROOT,review.id) )
    else:
        #import pdb; pdb.set_trace()
        review.instructors.add(request.user)
        review.save()
        return HttpResponseRedirect('%s/review/%s' %(settings.SITE_ROOT,review.id) )



@login_required
def reportReviewunsubmit(request, rev):
    report = ReviewReportStatus.objects.filter(reviewer__id = request.user.id).filter(review__id = rev)
    report = report[0]
    #import pdb; pdb.set_trace()
    report.submitdate=datetime(2012, 5, 18, 13, 0, 49, 0,pytz.UTC)
    report.save()

    # Take user back to their review home.
    return HttpResponseRedirect('%s/review/%s'%(settings.SITE_ROOT,rev) )


# AJAX #
@login_required
def respond(request):
    if request.method == 'POST':
        qid = request.POST.get("questionid")
        rid = request.POST.get("revid")
        ans = request.POST.get("choice")
        print('qid:')
        print(qid)

        numques = Review.objects.get(pk=rid).questions().count()
        allresp = ReviewResponse.objects.filter(user__id = request.user.id).filter(review__id = rid)
        resp = allresp.filter(question__id = qid )

        returndata = dict()

        if not resp: # Make a new ReviewResponse object
            resp = ReviewResponse()
            resp.review = Review.objects.get(pk=rid)
            resp.question = ReviewQuestion.objects.get(pk=qid)
            resp.user = request.user
            resp.lastactivity = datetime.utcnow()
            resp.response = ans
            resp.save()
            returndata["message"] = "Your answer has been submitted."
            returndata["counter"] = allresp.count()
        else: # Update a response
            resp = resp[0]
            resp.response = ans
            resp.lastactivity = datetime.utcnow()
            resp.save()
            returndata["message"] = "Your answer has been updated."
            returndata["counter"] = allresp.count()

        returndata["iscomp"] = numques == allresp.count()
        return HttpResponse(json.dumps(returndata), content_type="application/json")

@login_required
def clearResponse(request):
   if request.method == 'POST':
       qid = request.POST.get("questionid")
       rid = request.POST.get("revid")

       numques = Review.objects.get(pk=rid).questions().count()
       allresp = ReviewResponse.objects.filter(user__id = request.user.id).filter(review__id = rid)
       resp = allresp.filter(question__id = qid )
       returndata = dict()
       if resp: # clear the response
            resp = resp[0]
            resp.delete();

            returndata["message"] = "Your answer has been cleared."
            returndata["counter"] = allresp.count()
            returndata["iscomp"] = numques == allresp.count()
            return HttpResponse(json.dumps(returndata), content_type="application/json")

@login_required
def writeComment(request):                                            #What this post data look like
    if request.method == 'POST':
        rid = request.POST.get("revid")
        sect = request.POST.get("sectionid")
        comm = request.POST.get("comment")

        commented = ReviewComment.objects.filter(user__id = request.user.id).filter(review__id = rid).filter(section__id = sect)

        if not commented:
            comment = ReviewComment();
            comment.text = comm
            comment.user = request.user
            comment.section = ReviewSection.objects.get(pk=sect)
            comment.review = Review.objects.get(pk=rid)
            comment.postdate = datetime.now()
            comment.save()
        else:
            comment = commented[0]
            comment.text = comm
            comment.postdate = datetime.now()
            comment.save()

        return HttpResponse("Your comment has been saved.")

@login_required
def submitPrep(request):
    if request.method == 'POST':
        rid = request.POST.get("revid")
        rev = Review.objects.get(pk=rid)

        for key, value in request.POST.items():
            if key != "revid" and key != "csrfmiddlewaretoken":
                response = SurveyResponse.objects.filter(review__id = rev.id).filter(question__id = key).filter(user__id = request.user.id)

                if not response:
                    response = SurveyResponse() # Make a new SurveyResponse object
                    response.review = rev
                    response.question = Question.objects.get(pk = key)
                    response.user = request.user
                    response.response = value
                    response.save()
                    print (response)
                else:
                    response = response[0]
                    response.response = value
                    response.save()

        return HttpResponse("Your pre assessment has been submitted. Thank you.")




    #    if request.method == 'POST':
    #        rid = request.POST.get("revid")
    #        sect = request.POST.get("sectionid")
    #        comm = request.POST.get("comment")
    #
    #        commented = ReviewComment.objects.filter(user__id = request.user.id).filter(review__id = rid).filter(section__id = sect)
    #
    #        if not commented:
    #            comment = ReviewComment();
    #            comment.text = comm
    #            comment.user = request.user
    #            comment.section = ReviewSection.objects.get(pk=sect)
    #            comment.review = Review.objects.get(pk=rid)
    #            comment.postdate = datetime.now()
    #            comment.save()
    #        else:
    #            comment = commented[0]
    #            comment.text = comm
    #            comment.postdate = datetime.now()
    #            comment.save()
