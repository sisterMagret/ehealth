from django.contrib import admin

from .models import User, Patient, Agent, UserProfile, Category, FollowUp



class PatientAdmin(admin.ModelAdmin):
    # fields = (
    #     'first_name',
    #     'last_name',
    # )

    list_display = ['first_name', 'last_name', 'age']
    list_display_links = ['first_name']
    list_editable = ['last_name']
    list_filter = ['category']
    search_fields = ['first_name', 'last_name', 'email']



admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Agent)
admin.site.register(FollowUp)
