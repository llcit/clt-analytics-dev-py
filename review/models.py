from django.db import models

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save

from django.db.models import Count

from django.contrib.contenttypes.models import ContentType

from django.core.validators import MinLengthValidator

OPTION_CHOICES = (
    ('radio', 'One selection allowed'),
    ('checkbox', 'Multiple selections allowed'),
)

EVAL_SCALE = (
    (1, 'NEEDS ATTENTION'),  # PREVIOUS: BASELINE
    (2, 'MEETS REQUIREMENTS'),  # PREVIOUS: EFFECTIVE
    (3, 'EXEMPLARY')  # PREVIOUS: EXEMPLARY
)


class ReviewSurvey(models.Model):
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=4096)

    def questionSections(self):
        return ReviewSection.objects.filter(survey__id=self.id).order_by('rank')

    def questions(self):
        return ReviewQuestion.objects.filter(section__survey__id=self.id).order_by('section__rank', 'rank')

    def __str__(self):
        return self.title


class Survey(models.Model):
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=4096)

    def questions(self):
        # Returns all questions in this survey
        return Question.objects.filter(survey__id=self.id)

    def responses(self):
        # Returns all responses to this survey NOTE: this queryset is not
        # distinguished by review
        return SurveyResponse.objects.filter(question__survey__id=self.id)

    def __str__(self):
        return self.title


class ReviewSection(models.Model):
    survey = models.ForeignKey(ReviewSurvey)
    name = models.CharField(u"Category name", max_length=200)
    text = models.TextField(
        u"Introduction text", help_text=u"This is displayed above the list of questions you add to this category")
    rank = models.IntegerField(
        u"Category number", help_text=u"This is used for determining the order of the categories")

    def questions(self):
        return ReviewQuestion.objects.filter(section__id=self.id)

    def comments(self):
        comments = ReviewComment.objects.filter(section__id=self.id)
        return comments

    def __str__(self):
        return u"%s" % (self.name)


class ReviewQuestion(models.Model):
    section = models.ForeignKey(
        ReviewSection, help_text=u"The section that this question is part of. The user sees each category in-order on a single page, with all questions belonging to the category on the page")
    text = models.CharField(max_length=1024)
    rank = models.IntegerField()
    guide = models.TextField(blank=True)

    def getOptions(self):
        return ReviewQuestionOption.objects.filter(parent__id=self.id).order_by('rank')

    def getOptionTexts(self):
        return u'%s' % (ReviewQuestionOption.objects.filter(parent__id=self.id).order_by('rank').values_list('text'))

    # def getMatrix(self):
    #     return ReviewMatrix.objects.filter(parent__id = self.id)

    def responses(self):
        return ReviewResponse.objects.filter(question__id=self.id)

    def __str__(self):
        return self.text


class ReviewQuestionOption(models.Model):
    parent = models.ForeignKey(ReviewQuestion)
    text = models.TextField()
    answer = models.BooleanField(u"Is this the correct answer?", blank=True)
    rank = models.IntegerField(choices=EVAL_SCALE,
                               help_text=u"Scale. This also effects the order this option will appear.")
    type = models.CharField(max_length=48, choices=OPTION_CHOICES,
                            help_text=u"Allow multiple checks or only one (checkbox or radio)?", default='radio')

    def getSection(self):
        return u"%s" % (self.parent.section)

    def __str__(self):
        return u"%s" % (self.get_rank_display())


class Review(models.Model):
    coursetitle = models.CharField(max_length=1024)
    survey = models.ForeignKey(ReviewSurvey)
    presurv = models.ForeignKey(Survey)
    instructors = models.ManyToManyField(
        User, related_name="Course Instructor(s)+")
    reviewers = models.ManyToManyField(User, related_name="Course Reviewer(s)+")

    siteurl = models.URLField()
    coursedesc = models.CharField(max_length=4096, blank=True)
    siteinfo = models.CharField(max_length=4096, blank=True)
    startdate = models.DateField(blank=True)
    completed = models.DateField(blank=True)
    accesscode = models.CharField(max_length=255, blank=True, unique=True, verbose_name='Access Code', validators=[
                                  MinLengthValidator(10)], 
                                  help_text=u"SEND THIS TO REVIEWERS TO GIVE THEM ACCESS:<br>https://llc.manoa.hawaii.edu/analytics/review/register/ACCESS_CODE_HERE")

    presurv.blank = True
    coursedesc.blank = True
    siteinfo.blank = True
    startdate.null = True
    completed.null = True
    accesscode.null = True

    def canReport(self, user):
        reviewerreport = ReviewReportStatus.objects.filter(
            review__id=self.id).filter(reviewer__id=user.id)
        return reviewerreport.count()

    def isReviewer(self, user):
        if user in self.reviewers.all():
            return True
        return False

    def isInstructor(self, user):
        if user in self.instructors.all():
            return True
        return False

    def reviewsurvey(self):
        return ReviewSurvey.objects.get(id=self.survey.id)

    def questions(self):
        return ReviewQuestion.objects.filter(section__survey__id=self.survey.id).order_by('section', 'rank')

    def responses(self):
        return ReviewResponse.objects.filter(review__id=self.id).order_by("user", "question__section__rank", "question__rank")

    def surveyquestions(self):
        return Question.objects.filter(survey__id=self.presurv.id)

    def surveyresponses(self):
        resp = SurveyResponse.objects.filter(
            review=self).order_by("review", "user", "question__rank")
        print (resp)
        return resp

    def __str__(self):
        return self.coursetitle


class ReviewResponse(models.Model):
    review = models.ForeignKey(Review)
    question = models.ForeignKey(ReviewQuestion)
    user = models.ForeignKey(User)
    response = models.IntegerField(choices=EVAL_SCALE)
    lastactivity = models.TimeField()

    def getResponseText(self):
        opts = ReviewQuestionOption.objects.filter(
            parent__id=self.question.id).get(rank=self.response)
        return opts.text

    def getUserComments(self):
        comment = ReviewComment.objects.filter(
            section=self.question.section.id).filter(user=self.user)
        if comment:
            return comment[0].text
        return ''

    def __str__(self):
        return u'%s' % self.response

#  NOTEs


class ReviewComment(models.Model):
    review = models.ForeignKey(Review)
    section = models.ForeignKey(ReviewSection)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=4096)
    postdate = models.TimeField(blank=True)

    def __str__(self):
        return self.text

# This is the one who decide whether the form is completed


class ReviewReportStatus(models.Model):
    review = models.ForeignKey(Review)
    reviewer = models.ForeignKey(User)
    submitdate = models.DateTimeField(blank=True)

    def __str__(self):
        return u'%s %s %s' % (self.review, self.reviewer, self.submitdate)

# SURVEY CLASSES ##########


class Question(models.Model):
    survey = models.ForeignKey(Survey)
    text = models.CharField(max_length=1024)
    rank = models.IntegerField()

    def getOptions(self):
        return QuestionOption.objects.filter(parent__id=self.id).order_by('rank')

    def __str__(self):
        return self.text


class QuestionOption(models.Model):
    parent = models.ForeignKey(Question)
    text = models.CharField(max_length=1024)
    answer = models.BooleanField(u"Is this the correct answer?")
    rank = models.IntegerField(help_text=u"Display order?")
    # TODO Make this an enumerator.
    type = models.CharField(max_length=48, choices=OPTION_CHOICES,
                            help_text=u"Allow multiple checks or only one (checbox or radio)?", default='radio')

    def __str__(self):
        return self.text


class SurveyResponse(models.Model):
    review = models.ForeignKey(Review)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    response = models.CharField(max_length=4096)

    def __str__(self):
        return self.response


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Custom field(s) for Review application
    department = models.CharField(max_length=512, default="NOT SET")

    def __str__(self):
        return "%s %s" % (self.user, self.department)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
