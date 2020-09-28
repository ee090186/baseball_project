from django.contrib import admin
from .models import Profile, Situation, Pitting, Batting, ContactedResults, UncontactedResults



admin.site.register(Profile)
admin.site.register(Situation)
admin.site.register(Pitting)
admin.site.register(Batting)
admin.site.register(ContactedResults)
admin.site.register(UncontactedResults)