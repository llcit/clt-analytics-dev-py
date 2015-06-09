from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from analytics.admin import CommonExtras
from django.contrib import admin

from review.models import *

class OptionsInline(admin.TabularInline):
    model = ReviewQuestionOption
    extra = 0
    
class ReviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('section', 'rank', 'text', 'getOptionTexts', 'guide')
    ordering = ('section', 'rank')
    list_filter = ['section']
    inlines = [OptionsInline]

class ReviewQuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('getSection', 'parent', 'rank', 'text')
    raw_id_fields = ('parent',)
    
class ReviewResponseAdmin(admin.ModelAdmin):
    list_display = ('lastactivity', 'question', 'response', 'user')
    list_filter = ['user', 'review']

class ReviewSectionAdmin(admin.ModelAdmin):
    list_display = ("survey","name", "text", "rank")

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("coursetitle","startdate", "completed","accesscode")
    list_filter = ['instructors', 'reviewers']
    
admin.site.register(ReviewSurvey, Media = CommonExtras)
admin.site.register(ReviewSection, ReviewSectionAdmin, Media = CommonExtras)    
admin.site.register(ReviewQuestion, ReviewQuestionAdmin, Media = CommonExtras)
admin.site.register(ReviewQuestionOption, ReviewQuestionOptionAdmin, Media = CommonExtras)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewResponse, ReviewResponseAdmin, Media = CommonExtras)
admin.site.register(ReviewComment)
admin.site.register(ReviewReportStatus)

class SurveyOptionsInline(admin.TabularInline):
    model = QuestionOption
    extra = 0

class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'rank')
    ordering = ('survey', 'rank')
    list_filter = ['survey']
    inlines = [SurveyOptionsInline]

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('review', 'question', 'response', 'user')
    list_filter = ['review']

admin.site.register(Survey, Media = CommonExtras)
admin.site.register(Question, SurveyQuestionAdmin, Media = CommonExtras)
admin.site.register(QuestionOption, Media = CommonExtras)
admin.site.register(SurveyResponse, SurveyResponseAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
