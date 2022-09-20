class APIStripe{

    #stripe = undefined
    
    constructor(){
        this.#stripe = Stripe("pk_test_51LgR6IHVRJovbZDJEifEzGWqm5oSz8d6XlLpLMHYrdRPi5NeZb251Vqe7SzwouLYhtlvBYZIebzm6hnDPfK5jPNT00NNFTs3Zl");
        this.initCheckOut();
        this.initBasketByAll();
    }

    #getSelectedCurently(elem){
        const selectCurently = elem.parentNode.querySelector("#select-curently");

        if(selectCurently)
            return selectCurently.value;

        return "usd";
    }

    initCheckOut(){
        let data;

        document.querySelectorAll(".checkout-button").forEach(button => {
            button.onclick = () => {

                data = "currently=" + this.#getSelectedCurently(button);

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

    initBasketByAll(){
        document.querySelectorAll(".basket-buy-all").forEach(button => {
            button.onclick = () => {

                const array = [];
                const ids = [];
                let name, price, count, item;

                const currency = this.#getSelectedCurently(button);
                const basket = document.getElementById("box-products");

                if(!basket)
                    return;

                basket.querySelectorAll(".product").forEach(product => {

                    name = product.querySelector(".name").innerHTML;
                    price = Math.round(product.querySelector(".price").innerHTML * 100);
                    count = product.querySelector(".count-in-basket").value;

                    item = {
                        'price_data': {
                            'currency': currency,
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