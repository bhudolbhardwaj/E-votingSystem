from django.contrib import admin

# Register your models here.
from .models import Candidate,Voter,Official,Voted

class CandidatetAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'party_name', 'district', 'vote_count']

class VoterAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'gender', 'district', 'mobile', 'aadhar_number', 'dob']

admin.site.register(Candidate,CandidatetAdmin)
admin.site.register(Voter,VoterAdmin)
admin.site.register(Official)
admin.site.register(Voted)