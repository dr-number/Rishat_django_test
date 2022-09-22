from django.http import JsonResponse
import json

from django.views import View
from main.functions import get_app_name
from django.template.loader import render_to_string
from django.http import HttpRequest

def prepare_params(params: str) -> str:
    if params != '': 
        params = json.dumps(params)
    
    return params

def render_button_ajax_modal(request: HttpRequest, 
    modal_id: str, text: str, classes: str = '', params: str = '', 
    buttom_id: str = '', custom_title: str = '', 
    rerender_always: str = '', run_after_init: str = '') -> str:

    return render_to_string('main/includes/button_ajax_modal.html', {
        'modal_id' : modal_id,
        'app_name' : get_app_name(request),
        'text_button' : text,
        'classes' : classes,
        'params' : prepare_params(params),
        'buttom_id' : buttom_id,
        'custom_title' : custom_title,
        'rerender_always' : rerender_always,
        'run_after_init' : run_after_init
    })

def render_button_ajax_modal_svg(request: HttpRequest, modal_id: str, 
    svg: str, svg_classes: str = '', classes: str = '', 
    params: str = '', buttom_id: str = '', 
    custom_title: str = '', 
    rerender_always: str = '', app_name: str = '', 
    run_after_init: str = '', run_after_close: str = '') -> str:

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
        'run_after_init' : run_after_init,
        'run_after_close' : run_after_close
    })

def prepare_arguments_function(params: str) -> str:

    if params == '':
        return ''

    result = ''
    params = json.loads(params)

    for key, value in params.items():
        result += key + '=' + value + ','

    if len(result) != 0:
        result = result[:-1]

    return result


class CallBack(View):

    def __RESPONSE():
        return {
            'additional_data' : '',
            'result' : '',
            'error' : '',
            'code' : 200, 
        }

    def post(self, request, *args, **kwargs):

        response = self.__RESPONSE()

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


