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
                    
                    runInServerFetch("favorites/change", getParams(product))
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

        runInServerFetch("delete", getParams(modalFavorite))
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
                        document.getElementById("count-type").innerHTML -= 1;
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