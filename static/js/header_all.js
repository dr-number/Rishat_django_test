class AjaxServer{

    #getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    getParams(element){
        return JSON.parse(JSON.stringify(element.dataset));
    }

    runInServerFetch(url, params=''){

        const head = {
            method: "POST",
            credentials: 'same-origin',
            headers: {
                'Accept' : 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken' : this.#getCookie('csrftoken')
            }
        };

        if(params != '')
            head['body'] = JSON.stringify(params);

        return fetch(url, head);
    }

}

const ajaxServer = new AjaxServer();