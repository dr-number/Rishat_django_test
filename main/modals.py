import json

from django.template.loader import render_to_string
from django.http import JsonResponse

import traceback
import logging

from main.config_main import read_config_json

def __BASE_MODAL_RESPONSE():
    return  {
        'additional_data' : '',
        'html' : '',
        'error' : '',
        'warning' : '',
        'code' : 200,
    }

def render_modal(modal_id, app_name, options):

    if 'params' in options and options['params'] != '':
        params = json.loads(options['params'])
    else:
        params = {}

    if 'title' in options:
        custom_title = options['title']
    else:
        custom_title = ''

    params['name_modal'] = modal_id
    params['custom_title'] = custom_title

    return render_to_string(app_name + '/modals/' + modal_id + '.html', params)


def auto_upload_modals(request):

    response = __BASE_MODAL_RESPONSE()

    data = read_config_json('auto_upload_modals.json')

    if data == '':
        response['error'] = 'Failed read config file!'
        JsonResponse(response)

    html = ''

    data_post = json.load(request)
    current_url = data_post["url"]

    for app_name in data.items():
        
        app_name = app_name[0]
        app_modals = data[app_name]

        for modal in app_modals:
            try:
                for_url = modal["for_url"]
                if("*" in for_url or current_url in for_url):
                    html += render_modal(modal['id'], app_name, modal)
            except Exception as e:
                response['warning'] += 'render modal (auto upload): \n App name: ' + app_name + '\n Modal id: ' + modal['id'] + '\n'
                logging.error(traceback.format_exc())

    response['html'] = html
    return JsonResponse(response)


def render_modal_ajax(request):

    response = __BASE_MODAL_RESPONSE()

    if request.method != "POST":
        response['error'] = 'Method not POST!'
        return JsonResponse(response)

    try:
        data_post = json.load(request)
        html = render_modal(data_post['modal_id'], data_post['app_name'], data_post)
        response['html'] = html
    except Exception as e:
        logging.error(traceback.format_exc())
        # Logs the error appropriately. 
        response['error'] = 'Failed render modal! ' + str(e)

    return JsonResponse(response)