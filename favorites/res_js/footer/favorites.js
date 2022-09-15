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
        alert("z");
        return

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
}

const favorites = new Favorites();