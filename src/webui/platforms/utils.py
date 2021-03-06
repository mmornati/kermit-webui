import logging
from webui import settings
from webui.servers.models import Server
import os
import glob
from django.utils import simplejson as json
from webui.puppetclasses.models import PuppetClass
import time
from guardian.shortcuts import get_objects_for_user

logger = logging.getLogger(__name__)

def installed_platforms_list():
    path = os.path.dirname(__file__)
    installed_platforms = []
    for module in os.listdir(path):
        if os.path.isdir(path + '/' + module) == True:
            installed_platforms.append(module)
    return installed_platforms

def convert_keys_names(dictionary):
    for key,value in dictionary.items():
        if key.__contains__('-'):
            dictionary[key.replace('-', '_')]=value
            dictionary.pop(key, value)
            if type(value).__name__=='dictionary':
                convert_keys_names(value)
            elif type(value).__name__=='list':
                check_list(value)

def check_list(type_list):
    for content in type_list:
        if type(content).__name__=='dict':
            convert_keys_names(content)
        elif type(content).__name__=='list':
            check_list(content)

def read_file_info(hostname, prefix, suffix):
    if hostname:
        toSearch = settings.AMQP_RECEIVER_INVENTORY_FOLDER + '/' + prefix + hostname + suffix
        filesFound = glob.glob(toSearch)
        if (len(filesFound) == 0):
            server = Server.objects.filter(hostname=hostname)
            if server:
                fqdn = server[0].fqdn
                logger.info("No inventory files found. Trying with fqdn: " + fqdn)
                toSearch = settings.AMQP_RECEIVER_INVENTORY_FOLDER + '/' + prefix + fqdn + suffix
                filesFound = glob.glob(toSearch)
            else:
                logger.error("No server found in database with hostname " + hostname)
        file_content = None
        if (len(filesFound)>0):
            if len(filesFound) > 1:
                logger.warn("More than one inventory files found! Using just the first one")
                logger.warn(filesFound)           
                filesFound.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            try:
                file_content = open(filesFound[0], 'r').read()
            except:
                logger.error('Cannot access inventory file!!')
            
            return json.loads(file_content)
    return None
        
def extract_servers(filters, user):
    logger.debug("Extracting servers from filters to retrieve instances")
    classes = []
    server_selected = None
    class_list = filters.split(';')
    for puppet_class in class_list:
        current_filter = puppet_class.split('=')
        if current_filter[0] == 'class':
            classes.append(PuppetClass.objects.get(name=current_filter[1]))
        else: 
            try:
                server_selected = Server.objects.get(fqdn=current_filter[1])
            except:
                logger.debug("Error retrieving server using FQDN. Trying with HostName")
                server_selected = Server.objects.get(hostname=current_filter[1])
    logger.debug("Classes found in your filter: %s" % str(classes))
    logger.debug("Server selected with your filter: %s" % server_selected)
    servers_list = []
    if classes:
        logger.debug("Retrieving server using classes")
        if not user.is_superuser and settings.FILTERS_SERVER:
            servers_list = get_objects_for_user(user, 'use_server', Server).filter(puppet_classes__in = classes, deleted=False).distinct()
        else:
            servers_list = Server.objects.filter(puppet_classes__in = classes, deleted=False).distinct()
    else:
        servers_list.append(server_selected)
        
    return servers_list
        
        
def read_file_log(file_name):
    toSearch = settings.AMQP_RECEIVER_LOG_FOLDER + '/*' + file_name
    time_out = 1000
    filesFound = []
    counter = 0
    while (len(filesFound) == 0 and counter < time_out):
        time.sleep(0.1)
        filesFound = glob.glob(toSearch)
        counter = counter + 1
    if (len(filesFound) == 0):
        logger.warn("No log file found!!")
        return None
    else:
        if len(filesFound) > 1:
            logger.warn("More than one log file with the given name %s found! Using just the first one" % file_name)
            logger.warn(filesFound)           
            filesFound.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        try:
            file_content = open(filesFound[0], 'r').read()
        except:
            logger.error('Cannot access inventory file!!')
        return plaintext2html(file_content)
        
def plaintext2html(text, tabstop=4):
    new_string = text.replace("\\r\\n", "<br/>")
    new_string = new_string.replace("\\n", "<br/>")
    new_string = new_string.replace("\n", "<br/>")
    new_string = new_string.replace('\\r', '<br/>')
    new_string = new_string.replace("\r", "<br/>")
    new_string = new_string.replace(' ', '&nbsp;')
    new_string = new_string.replace('\\t', '&nbsp;&nbsp;&nbsp;&nbsp;')    
    return new_string