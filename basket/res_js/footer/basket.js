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

