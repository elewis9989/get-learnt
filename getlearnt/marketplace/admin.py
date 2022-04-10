from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Skill)
admin.site.register(Tag)
admin.site.register(Transaction)
admin.site.register(Listing)
admin.site.register(UserProfile)