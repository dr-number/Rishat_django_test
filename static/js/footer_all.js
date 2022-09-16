class APIStripe{

    #stripe = undefined
    
    constructor(){
        this.#stripe = Stripe("pk_test_51LgR6IHVRJovbZDJEifEzGWqm5oSz8d6XlLpLMHYrdRPi5NeZb251Vqe7SzwouLYhtlvBYZIebzm6hnDPfK5jPNT00NNFTs3Zl");
        this.initCheckOut();
        this.#initBasketByAll();
    }

    initCheckOut(){
        let selectCurently, data;

        document.querySelectorAll(".checkout-button").forEach(button => {
            button.onclick = () => {

                selectCurently = button.parentNode.querySelector("#select-curently");

                if(selectCurently)
                    data = "currently="+selectCurently.value 
                else
                    data = "currently=usd" 
                

                fetch("/buy/" + button.getAttribute("id") + "/?" + data, {
                    method: "GET",
                })
                .then(function(response){
                    return response.json();
                })
                .then((session) => {

                    if(!session.error)
                        return this.#stripe.redirectToCheckout({sessionId: session.id});
                    else
                        console.error("Session error: ", session.error);    
                })
                .then(function(result){

                    if(result.error){
                        alert(result.error.message);
                    }
                });
            }
        })
    }

    #initBasketByAll(){
        document.querySelectorAll(".basket-buy-all").forEach(button => {
            button.onclick = () => {

                const array = [];
                const ids = [];
                let name, price, count, item, currently;

                document.querySelectorAll(".product").forEach(product => {

                    name = product.querySelector(".name").innerHTML;
                    currently = product.querySelector(".currently").innerHTML;
                    price = Math.round(product.querySelector(".price").innerHTML * 100);
                    count = product.querySelector(".count-in-basket").value;

                    item = {
                        'price_data': {
                            'currency': currently,
                            'product_data': {
                            'name': name,
                            },
                            'unit_amount': price,
                        },
                        'quantity': count,
                    }

                    array.push(item);
                    ids.push(product.getAttribute("data-product-id"));

                })

                const data = {
                    'ids' : ids,
                    'data' : array
                };

                ajaxServer.runInServerFetch('buy_basket', data)
                    .then(function(response){
                        return response.json();
                    })
                    .then((session) => {

                        if(!session.error)
                            return this.#stripe.redirectToCheckout({sessionId: session.id});
                        else
                            console.error("Session error: ", session.error);    
                    })
                    .then(function(result){

                        if(result.error){
                            alert(result.error.message);
                        }
                    });
            }
        })
    }

}

const ApiStripe = new APIStripe();
class Basket{

    constructor(){
        this.#init();
    }

    #changeBasket(url, button, countElem = undefined){

        ajaxServer.runInServerFetch(url, ajaxServer.getParams(button))
            .then(function(response){
                return response.json();
            })
            .then(function(result){

                if(result.status == 'success')
                    if(countElem && result.count > 0)
                        countElem.value = result.count
                else{
                    console.error("Basket error: ", result.error);    
                }
            })
            .then(function(result){

                if(result.error){
                    alert(result.error.message);
                }
            })
            .catch(function(error){
                console.error("Error: ", error);
            });

    }

    #getCountElem(button){
        return button.parentElement.querySelector(".count-in-basket");
    }

    #init(){
        document.querySelectorAll(".basket-button").forEach(button => {
            button.onclick = () => {
                this.#changeBasket("basket/change", button);
            }
        })

        document.querySelectorAll(".basket-remove, .basket-add").forEach(button => {
            button.onclick = () => {
                this.#changeBasket("change", button, this.#getCountElem(button));    
            }
        });
    }

}

new Basket();


class Profile{

    #profilePopupBtn = document.getElementById("profile-popup-btn");
    #profilePopup = document.querySelector(".profile-popup")

    constructor(){
        this.#popup()
    }

    #popup(){

        if(this.#profilePopupBtn)
            this.#profilePopupBtn.onclick = () => {
                this.#profilePopup.classList.toggle("d-none");
            }
    }

    getProfilePopupBtnId(){
        return this.#profilePopupBtn.getAttribute("id");
    }

    hidePopup(){
        this.#profilePopup.classList.add("d-none");
    }
}

const profile = new Profile();
class Favorites{

    constructor(){
        this.#init();
    }

    #init(){
        let product, icoClassList;
        const changeFavorites = document.querySelectorAll(".change-favorites");

        if(changeFavorites){
            changeFavorites.forEach(button => {

                button.onclick = () => {

                    product = button.closest(".product");
                    
                    ajaxServer.runInServerFetch("favorites/change", ajaxServer.getParams(product))
                        .then(function(response){
                            return response.json();
                        })
                        .then(function(result){
                
                            if(result.status == "success"){
                                icoClassList = button.querySelector(".ico").classList;

                                if(product.getAttribute("data-type-change") == "on"){
                                    product.setAttribute("data-type-change", "off");
                                    icoClassList.remove("ico-favorites-off");
                                    icoClassList.add("ico-favorites-on");
                                }
                                else{
                                    product.setAttribute("data-type-change", "on");
                                    icoClassList.remove("ico-favorites-on");
                                    icoClassList.add("ico-favorites-off");
                                }
                            }
                            else
                                console.error("Favorite error change");    
                            
                        })
                        .then(function(result){
                
                            if(result.error){
                                alert(result.error.message);
                            }
                        })
                        .catch(function(error){
                            console.error("Error: ", error);
                        });

                }
            });
        }
    }


    deleteFromFavorite(){

        const modalFavorite = document.querySelector(".modal-favorite");

        if(!modalFavorite){
            return
        }

        ajaxServer.runInServerFetch("delete", ajaxServer.getParams(modalFavorite))
            .then(function(response){
                return response.json();
            })
            .then(function(result){

                if(result.error){
                    alert(result.error.message);
                    return;
                }
    
                if(result.status == "success"){
                    const productId = modalFavorite.dataset.productId;
                    const item = document.querySelector('[product-id="' + productId + '"]');

                    if(item){
                        item.parentNode.removeChild(item);
                        
                        const countType = document.getElementById("count-type");
                        countType.innerHTML -= 1;

                        if(countType.innerHTML == '0')
                            location.reload();
                    }

                }
                else
                    console.error("Favorite error delete");    
                
            })
            .catch(function(error){
                console.error("Error: ", error);
            });
    }
}

const favorites = new Favorites();
document.addEventListener('click', function(e) {
    if (e.target.id != profile.getProfilePopupBtnId()) {
      profile.hidePopup();
    }
  });
class Modals{

    constructor(){
        this.#initButtons();
        this.#renderAutoUploadModals();
    }

    getModal(modalId){
        const sectionModals = document.getElementById('ajax-modals');
        return sectionModals.querySelector("#" + modalId);
    }

    openLoadIndicator(){

        const modal = this.getModal("indicator-loader");

        if(modal && (!modal.getAttribute("style") || modal.style.display == 'none'))
            modal.style.display = "block";
    }

    closeLoadIndicator(){

        const modal = this.getModal("indicator-loader");

        if(modal)
            modal.style.display = "none";
            
    }

    closeModal(modal){
        modal.style.display = "none";
    }

    #openModal(modal){
        modal.style.display = "block";

        modal.querySelector('.close_modal_window').onclick = () => {
            this.closeModal(modal);
        }

        window.onclick = (event) => {

            if (event.target == modal) 
                this.closeModal(modal);
        }
    }

    #isRerenderModal(element){
        return element.hasAttribute("data-rerender-always");
    }

    #openModalError(){
        this.closeLoadIndicator();
        this.#openModal(this.getModal("error-modal"));
    }


    #initButtons(){
        document.querySelectorAll(".oepn-modal").forEach(button => {
            button.onclick = () =>{

                const sectionModals = document.getElementById('ajax-modals');

                if(sectionModals){

                    const modalId = button.dataset.modal_id;
                    const modal = this.getModal(modalId);
                    const isRerender = this.#isRerenderModal(button);

                    if(modal && !isRerender){
                        this.#openModal(modal);
                        return;
                    }

                    this.openLoadIndicator();

                    ajaxServer.runInServerFetch('/render_modal_ajax/', ajaxServer.getParams(button))
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
                            this.#openModal(this.getModal(modalId));


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

        ajaxServer.runInServerFetch('/auto_upload_modals/',  params)
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

const modals = new Modals();
class Question{

    init(){

        const listElements = document.querySelectorAll(".yes, .no");
        
        if(listElements){
            listElements.forEach(button => {
                button.onclick = () => {

                    if(button.hasAttribute("function"))
                        eval(button.getAttribute("function"));

                    modals.closeModal(modals.getModal("delete_favorites"));
                }
            });
        }

    }
}

const question = new Question();