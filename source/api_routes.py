from bottle import request, response, route, template
from rest_api import app
from working_packages.signavio_functions import get_model_by_id, get_dir_content, get_model
from working_packages.bpmn_shema_helper import BPMNProcessor
from working_packages.merson_converter import json_to_mermaid
import yaml
import json

def check_model(model,mod_format):
    if model:
        if mod_format == 'json':
            response.content_type = 'application/json'
            return  model
        processor = BPMNProcessor()
        transformed_data = processor.transform_to_bpmn_schema(model)
        minimal_json = processor.to_json()
        minimodel = json.loads(minimal_json)
        if mod_format == 'minijson':
            response.content_type = 'application/json'
            return  minimodel
        elif mod_format == 'yaml':
            yamlmodel = yaml.dump(minimodel)
            response.content_type = 'text/yaml; charset=UTF-8'
            return yamlmodel
        elif mod_format == 'mermaid':
            mermaidmodel = json_to_mermaid(minimodel)
            response.content_type = 'text/plain; charset=UTF-8'
            return  mermaidmodel
        else:
            response.status = 400
            return { "status": "OK!", "error": "Only json, minijson, yaml and mermaid are allowed!"}
    else:
        response.status = 400
        return { "status": "OK!", "error": "No model is found. Please check your ID!"}



@route('/docu')
def list():
    tmpl = "<!DOCTYPE html><html><h1>List of all available routes: </h1><ul>"
    route_list = app.routes
    for r in route_list:
        tmpl += "<li>{} {}</li>".format(r.method,r.rule)
    tmpl += "</ul></html>"
    response.set_header('Content-Type','text/html; charset=utf-8')
    return tmpl

@route('/test')
def test():
    return { "status": "OK!" }

@route('/model',method=['GET'])
def get_directory():
    response.content_type = 'text/plain; charset=UTF-8'
    docu = """
    This endpoint allows you to select one particular model in signavio academic and convert it to one of following formats: signavio-json, minimal-json, yaml or mermaid.\n
    To use it select desired format and provide a model ID:\n
    /model/<model_format>?id=<model_ID>
    """
    return docu

@route('/directory',method=['GET'])
def get_directory():
    response.content_type = 'text/plain; charset=UTF-8'
    docu = """
    This endpoint allows you to iterate over all models in the desired signavio academic directory and convert it to one of following formats: signavio-json, minimal-json, yaml or mermaid.\n
    To use it select desired format and provide a directory ID:\n
    /directory/<model_format>?id=<directory_ID>
    """
    return docu

@route('/model/<mod_format>',method=['GET'])
def convert_model(mod_format):
    model_id = request.query.id
    model = get_model_by_id('json', model_id)
    return check_model(model,mod_format)
#    if model:
#        if mod_format == 'json':
#            response.content_type = 'application/json'
#            return  model
#        processor = BPMNProcessor()
#        transformed_data = processor.transform_to_bpmn_schema(model)
#        minimal_json = processor.to_json()
#        minimodel = json.loads(minimal_json)
#        if mod_format == 'minijson':
#            response.content_type = 'application/json'
#            return  minimodel
#        elif mod_format == 'yaml':
#            yamlmodel = yaml.dump(minimodel)
#            response.content_type = 'text/yaml; charset=UTF-8'
#            return yamlmodel
#        elif mod_format == 'mermaid':
#            mermaidmodel = json_to_mermaid(minimodel)
#            response.content_type = 'text/plain; charset=UTF-8'
#            return  mermaidmodel
#        else:
#            response.status = 400
#            return { "status": "OK!", "error": "Only json, minijson, yaml and mermaid are allowed!"}
#    else:
#        response.status = 400
#        return { "status": "OK!", "error": "No model is found. Please check your ID!"}

@route('/directory/<mod_format>',method=['GET'])
def convert_directory(mod_format):
    output = {}
    dir_id = request.query.id
    dir_content = get_dir_content(dir_id)
    if dir_content:
        for d in dir_content:
            if d['rel'] == 'mod':
                    revision_ID = d['rep']['revision']
                    name = d['rep']['name']
                    model = get_model('json',revision_ID)
                    try:
                        output[name] = check_model(model,mod_format)
                    except:
                        output[name] = "There is some error in BPMN model. Please check it!"
        return { "status": "OK!","output": output }
    else:
        response.status = 400
        return { "status": "NOK!", "error": "No directory is found. Please check your ID!"}


