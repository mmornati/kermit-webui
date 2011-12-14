'''
Created on Nov 17, 2011

@author: mmornati
'''
from django.http import HttpResponse
from django.utils import simplejson as json
import logging
from celery.result import AsyncResult
from webui.restserver.template import render_agent_template

logger = logging.getLogger(__name__)

def get_progress(request, taskname, taskid):
    logger.info("Requesting taskid: %s"%taskid)
    result = AsyncResult(taskid, backend=None, task_name=taskname)
    logger.info("TASKID: %s"%result.task_id)
    
    dict = {}
    if (result.state == 'PENDING'):
        dict['state'] = 'Waiting for worker to execute task...'
    elif (result.state == 'PROGRESS'):
        dict['state'] = 'Operation in progress..'
    else:
        dict['state'] = result.state
    if result.result:
        if isinstance(result.result, tuple):
            response,content,agent,action=result.result
            print response
            print content
            print agent
            print action
            if response.status == 200:
                json_data = render_agent_template(request, {}, content, {}, agent, action)
                return HttpResponse(json_data, mimetype="application/json")
        else:
            value = float(1.0*result.result['current']/result.result['total'])*100
            dict['value'] = value
    else: 
        dict['value'] = 0
    json_data = json.dumps(dict)
    return HttpResponse(json_data, mimetype="application/json")