'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms

class DeployForm(forms.Form):
    bcname = forms.CharField(label=u"BarConsole Name")
    barname = forms.ChoiceField(label=u"Bar name")