import json
import requests
#from conf import *
#from PIL import Image
#from cairosvg import svg2png
#from io import BytesIO
import time
#import pandas as pd

from dotenv import load_dotenv
import os


class Signavio:
    # def __init__(self, base_url, name, password,tenant):
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv('SIGNAVIO_BASE_URL')
        self.name = os.getenv('SIGNAVIO_NAME')
        self.password = os.getenv('SIGNAVIO_PASSWORD')
        self.tenant = os.getenv('SIGNAVIO_TENANT')

def authenticate():
    mySignavio = Signavio()
    login_url = mySignavio.base_url + '/p/login'
    data = {'name': mySignavio.name,
            'password': mySignavio.password,
            'tokenonly': 'true'}
    data['tenant'] = mySignavio.tenant
    login_request = requests.post(login_url, data)
    auth_token = login_request.content.decode('utf-8')
    jsesssion_ID = login_request.cookies['JSESSIONID']
    lb_route_ID = login_request.cookies['LBROUTEID']
    return { 'jsesssion_ID': jsesssion_ID, 'lb_route_ID': lb_route_ID, 'auth_token': auth_token, 'base_url':mySignavio.base_url }

# function to get the content of a directory
def get_dir_content(dir_ID):
    auth_data = authenticate()
    dir_url = auth_data['base_url'] + '/p/directory'
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    get_dir_request = requests.get(dir_url + '/' + dir_ID, cookies=cookies, headers=headers)
    dir_content = json.loads(get_dir_request.text)
    return dir_content

# function to get the model from the signavio by its revision ID
def get_model(mod_format,revision_ID):
    auth_data = authenticate()
    diagram_url =  auth_data['base_url'] + '/p' + revision_ID + '/' + mod_format
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    get_diagram_request = requests.get(diagram_url, cookies=cookies, headers=headers)
    if mod_format == 'json' or mod_format == 'bpmn2_0_xml':
        return get_diagram_request.text
    elif mod_format == 'svg' or mod_format == 'png':
        return get_diagram_request.content

def get_model_by_id(mod_format, model_id):
    auth_data = authenticate()
    diagram_url =  auth_data['base_url'] + '/p/model/'
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    get_diagram_request = requests.get(diagram_url + model_id + '/' + mod_format, cookies=cookies, headers=headers)
    if mod_format == 'json' or mod_format == 'bpmn2_0_xml':
        return get_diagram_request.text
    elif mod_format == 'svg' or mod_format == 'png':
        return get_diagram_request.content

# function to post model to signavio
def post_model(target_dir_ID,model,name):
    auth_data = authenticate()
    model_url =  auth_data['base_url'] + '/p/model'
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    data = {
       'parent': '/directory/' + target_dir_ID,
       'namespace': 'http://b3mn.org/stencilset/bpmn2.0#',
    }
    data['name'] = name
    data['json_xml'] = model
    create_diagram_request = requests.post(model_url, cookies=cookies, headers=headers, data=data)


# get all models in the signavio directiry and save them to the local folder
def save_to_local(dir_ID,target_folder):
    dir_content = get_dir_content(dir_ID)
    for d in dir_content:
        if d['rel'] == 'mod':
            revision_ID = d['rep']['revision']
            if 'xml' in mod_format:
                name = d['rep']['name'] + '.xml'
            else:
                name = '{}.{}'.format(d['rep']['name'],mod_format)
            filename = '{}/{}'.format(target_folder,name)
            model = get_model(mod_format,base_url,revision_ID)
            if mod_format == 'json':
                model = json.loads(model)
                with open(filename, "w") as f:
                    json.dump(model, f, indent=4)
            elif mod_format == 'bpmn2_0_xml' or mod_format == 'svg':
                with open(filename, "w") as f:
                    f.write(model)
            elif mod_format == 'png':
                image = Image.open(BytesIO(model))
                image.save(filename, format="PNG")

# save json models from local to signavio
def save_from_local(local_directory,target_dir_ID):
    model_url = base_url + '/p/model'
    auth_data = authenticate(base_url)
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    data = {
       'parent': '/directory/' + target_dir_ID,
       'namespace': 'http://b3mn.org/stencilset/bpmn2.0#',
    }
    for filename in os.listdir(local_directory):
        file = os.path.join(local_directory, filename)
        if file.endswith(('.json')):
            with open(file, 'r') as content:
                model = content.read()
                data['name'] = filename
                data['json_xml'] = model
                create_diagram_request = requests.post(model_url, cookies=cookies, headers=headers, data=data)
                result = str(create_diagram_request.content)

