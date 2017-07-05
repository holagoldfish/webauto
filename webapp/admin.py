# -.- coding:utf-8 -.-
from django.contrib import admin

# Register your models here.
from webapp.models import *

class project(admin.ModelAdmin):
    fieldsets = [('用户名',{'fields': ['name']}),
        ("项目负责人",{"fields":["pro_user"]}),
        ("项目状态",{"fields":["pro_status"],"classes":["collapse"]})]




admin.site.register(Project,project)
admin.site.register(Method)
admin.site.register(Action)