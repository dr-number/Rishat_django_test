class Modals{

    #ajaxServer = undefined;

    constructor(ajaxServer){
        this.#ajaxServer = ajaxServer;
        this.#initButtons();
        this.#renderAutoUploadModals();
    }

    #getModal(modalId){
        const sectionModals = document.getElementById('ajax-modals');
        return sectionModals.querySelector("#" + modalId);
    }

    openLoadIndicator(){

        const modal = this.#getModal("indicator-loader");

        if(modal && (!modal.getAttribute("style") || modal.style.display == 'none'))
            modal.style.display = "block";
    }

    closeLoadIndicator(){

        const modal = this.#getModal("indicator-loader");

        if(modal)
            modal.style.display = "none";
            
    }

    closeModal(modal){
        modal.style.display = "none";
    }

    #openModal(modal){
        modal.style.display = "block";

        modal.querySelector('.close_modal_window').onclick = function () {
            closeModal(modal)
        }

        window.onclick = function (event) {

            if (event.target == modal) 
                closeModal(modal)
        }
    }

    #isRerenderModal(element){
        return element.hasAttribute("data-rerender-always");
    }

    #openModalError(){
        this.closeLoadIndicator();
        this.#openModal(this.#getModal("error-modal"));
    }


    #initButtons(){
        document.querySelectorAll(".oepn-modal").forEach(button => {
            button.onclick = () =>{

                const sectionModals = document.getElementById('ajax-modals');

                if(sectionModals){

                    const modalId = button.dataset.modal_id;
                    const modal = this.#getModal(modalId);
                    const isRerender = this.#isRerenderModal(button);

                    if(modal && !isRerender){
                        this.#openModal(modal);
                        return;
                    }

                    this.openLoadIndicator();

                    this.#ajaxServer.runInServerFetch('/render_modal_ajax/', this.#ajaxServer.getParams(button))
                    .then(response => response.json())
                    .then((result) => {
                        
                        if(result.code != 200){
                            this.#openModalError();
                            console.error("Failed response!");
                            return;
                        }

                        if(result.error == ''){

                            if(isRerender){
                                const rerender = document.getElementById(modalId);
                                if(rerender)
                                    rerender.remove();
                            }

                            sectionModals.insertAdjacentHTML("beforeend", result.html);
                            this.closeLoadIndicator();
                            this.#openModal(this.#getModal(modalId));


                            if(button.hasAttribute("data-run-after-init"))
                                eval(button.getAttribute("data-run-after-init"))
                        }
                        else{
                            this.#openModalError();
                            console.error(result.error);
                        }
                        
                    })
                    .catch((error) => {
                        this.#openModalError();
                        console.error('Failed render!');
                    });
                
                }

            };
            
        });
    }

    #renderAutoUploadModals(){

        const sectionModals = document.getElementById('ajax-modals');

        let url = document.location.pathname.split("/");
        let params = '';

        if(url.length >= 2){
            url = url[1];
            params = JSON.parse(JSON.stringify({ "url": url}));
        }
        else
            params = '';

        this.#ajaxServer.runInServerFetch('/auto_upload_modals/',  params)
        .then(response => response.json())
        .then(function(result){
            
            if(result.code == 200){

                if(result.warning)
                    console.warn(result.warning);

                if(result.error == '')
                    sectionModals.insertAdjacentHTML("beforeend", result.html);
                else
                    console.error(result.error);
            }
            else
                console.error("Failed response!");

        })
        .catch(function(error) {
            console.log('Failed auto upload render!');
        });
    }
}
