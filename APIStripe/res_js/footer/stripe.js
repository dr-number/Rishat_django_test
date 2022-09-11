const stripe = Stripe("pk_test_51LgR6IHVRJovbZDJEifEzGWqm5oSz8d6XlLpLMHYrdRPi5NeZb251Vqe7SzwouLYhtlvBYZIebzm6hnDPfK5jPNT00NNFTs3Zl")

document.querySelectorAll(".checkout-button").forEach(button => {
    button.onclick = () => {
        fetch("/buy/" + button.getAttribute("id") + "/", {
            method: "GET"
        })
        .then(function(response){
            return response.json();
        })
        .then(function(session){

            if(!session.error)
                return stripe.redirectToCheckout({sessionId: session.id});
            else
                console.error("Session error: ", session.error);    
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
})

document.querySelectorAll(".basket-buy-all").forEach(button => {
    button.onclick = () => {

        const array = [];
        const ids = [];
        let name, price, count, item;

        document.querySelectorAll(".product").forEach(product => {

            name = product.querySelector(".name").innerHTML;
            price = Math.round(product.querySelector(".price").innerHTML * 100);
            count = product.querySelector(".count-in-basket").value;

            item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': name,
                    },
                    'unit_amount': price,
                },
                'quantity': count,
            }

            array.push(item);
            ids.push(product.getAttribute("product-id"));

        })

        const data = {
            'ids' : ids,
            'data' : array
        };

        runInServerFetch('buy_basket', data)
            .then(function(response){
                return response.json();
            })
            .then(function(session){

                if(!session.error)
                    return stripe.redirectToCheckout({sessionId: session.id});
                else
                    console.error("Session error: ", session.error);    
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
})