import json
import os
import sys
from django.urls import resolve
from django.shortcuts import render
from rishat_test.settings import IS_SEPARATION_STATIC, STRIPE_PUBLIC_KEY

def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def getCurrentHost(request):
    return request.META['HTTP_REFERER']

def get_app_name(request):
    return sys.modules[resolve(request.path_info).func.__module__].__package__

def include_static(dir, allow, to_top=[], to_end=[], init=[], exp=''):

    filelist = []
    list_dir = os.walk(dir)

    result = []
    to_end_file = []
    to_top_file = []
    to_init_file = []

    to_top = set(to_top)
    to_end = set(to_end)
    init = set(init)
    
    for root, dirs, files in list_dir: 
        for file in files: 
            filelist.append(os.path.join(root, file))

            for name in filelist: 
                if exp and exp != os.path.splitext(name)[1]:
                    continue

                filter = name.split("/")
                if list(set(allow) & set(filter)):

                    if to_top and (to_top & set(filter)):
                        to_top_file.append(name)
                    elif to_end and (to_end & set(filter)):
                        to_end_file.append(name)
                    elif init and (init & set(filter)):
                        to_init_file.append(name)
                    else:
                        result.append(name)

    if to_top_file:
        result = to_top_file + result

    if to_end_file:
        result = result + to_end_file

    if to_init_file:
        result = result + to_init_file

    return list(dict.fromkeys(result))



def custom_render(request, template_name, data = {}):

    STRIPE_KEY = { 'stripe_public_key' : STRIPE_PUBLIC_KEY }

    if not IS_SEPARATION_STATIC:
        data.update(STRIPE_KEY)
        return render(request, template_name, data)

    app_name = get_app_name(request)

    header_js = include_static('static/js/header', 
        {app_name, 'init', 'main'}, 
        {'ajax_server.js'},
        {'init.js'}
    )

    footer_js = include_static('static/js/footer', 
        {app_name, 'custom_user', 'init', 'main'},
        to_end={'init.js'},
        init={'ajax_modals.js', 'question.js'}
    )

    styles_css = include_static('static/css/', 
        {app_name, 'custom_user', 'main', 'favorites', 'APIStripe'},
        exp='.css'
    )

    data.update(STRIPE_KEY)

    data.update({ 
        'header_js' : header_js,
        'footer_js' : footer_js,
        'styles_css' : styles_css
    })

    return render(request, template_name, data)


class ModelJsonData:

    def get_data(self, model, user_id, from_field):
        data = model.objects.filter(user_id=user_id).values(from_field).first()

        if data:
            data = data.get(from_field)
            return json.loads(data)

        return []

    def set_data(self, model, user_id, to_field, array):
        
        updated_values = {
                to_field : json.dumps(list(dict.fromkeys(array)))
            }

        result = model.objects.update_or_create(
            user_id = user_id,
            defaults = updated_values
        )

        return result[0].pk