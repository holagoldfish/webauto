# -.- coding:utf-8 -.-
__author__ = 'Administrator'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django import forms

class addform(forms.Form):
    a = forms.CharField()


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
