from django.http import JsonResponse
import json

from main.functions import get_app_name
from django.template.loader import render_to_string

def prepare_params(params):
    if params != '': 
        params = json.dumps(params)
    
    return params



def render_button_ajax_modal(request, modal_id, text, classes = '', params = '', buttom_id = '', custom_title = '', rerender_always = ''):

    return render_to_string('main/includes/button_ajax_modal.html', {
        'modal_id' : modal_id,
        'app_name' : get_app_name(request),
        'text_button' : text,
        'classes' : classes,
        'params' : prepare_params(params),
        'buttom_id' : buttom_id,
        'custom_title' : custom_title,
        'rerender_always' : rerender_always
    })

def render_button_ajax_modal_svg(request, modal_id, svg, svg_classes = '', classes = '', params = '', buttom_id = '', custom_title = '', rerender_always = '', app_name = '', run_after_init = ''):

    if not app_name:
        app_name = get_app_name(request)

    return render_to_string('main/includes/button_ajax_modal_svg.html', {
        'modal_id' : modal_id,
        'app_name' : app_name,
        'svg' : svg,
        'svg_class' : svg_classes,
        'classes' : classes,
        'params' : prepare_params(params),
        'buttom_id' : buttom_id,
        'custom_title' : custom_title,
        'rerender_always' : rerender_always,
        'run_after_init' : run_after_init
    })

def prepare_arguments_function(params):

    if params == '':
        return ''

    result = ''
    params = json.loads(params)

    for key, value in params.items():
        result += key + '=' + value + ','

    if len(result) != 0:
        result = result[:-1]

    return result


def call_back(request):

    response = {
        'additional_data' : '',
        'result' : '',
        'error' : '',
        'code' : 200, 
    }

    if request.method != "POST":
        response['error'] = 'Method not POST!'
        return JsonResponse(response)

    try:
        data_post = json.load(request)
    
        method = data_post['method']

        if 'params' in data_post:
            params = prepare_arguments_function(data_post['params'])
        else:
            params = ''

        result = eval('execute_from_ajax.' + method  + '(' + params + ')')
        response['result'] = result
    except AttributeError:
        response['error'] = 'Method \'' + method + '\' does not exist or it was called incorrectly!'

    return JsonResponse(response)


