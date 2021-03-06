'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.restserver.views',
  #Response without templating
  url(r'^mcollective/$', 'get', name = "call_mcollective"),
  url(r'^mcollective-args/(?P<wait_for_response>[\w|\W]+)/$', 'get', name = "call_mcollective_with_arguments"),
  #Response with template
  url(r'^mcollective-template/(?P<template>[\w|\W]+)/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/$', 'getWithTemplate', name = "call_mcollective_template"),
  url(r'^mcollective-template/(?P<template>[\w|\W]+)/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<args>[\w|\W]+)/$', 'getWithTemplate', name = "call_mcollective_template_with_arguments"),
  
  #Admin Actions
  url(r'^execute/(?P<action>[\w|\W]+)/(?P<call_type>[\w|\W]+)/$', 'executeAction', name = "action_executer"),
  
  #Task information
  url(r'^taskinfo/(?P<uuid>[\w|\W]+)/$', 'get_task_info', name = "get_task_info"),
  
)
