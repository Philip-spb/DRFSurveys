from django.contrib import admin

from .models import *

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Answer)
admin.site.register(TestBase)
