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