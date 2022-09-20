document.addEventListener('click', function(e) {
    if (e.target.id != profile.getProfilePopupBtnId()) {
      profile.hidePopup();
    }
  });

function renderSelectCurently(){
  let opt;
  let currencies = document.getElementById("data-currencies");
  const select = document.getElementById("select-curently");

  if(currencies && select){
    
    currencies = JSON.parse(currencies.innerHTML);

    currencies.forEach(item => {
      opt = document.createElement('option');
      opt.value = item;
      opt.innerHTML = item;
      select.appendChild(opt);
    })
 }
}

function renderBasketInModal(){
  const products = document.querySelector(".products");
  const boxProducts = document.getElementById("box-products");

  Array.from(products.children).forEach(child => {
    boxProducts.appendChild(document.importNode(child, true));
  })
}

function initSelectCurently(){
  renderSelectCurently();
  ApiStripe.initCheckOut();
}

function initSelectCurentlyBasket(){
  renderBasketInModal();
  renderSelectCurently();
  ApiStripe.initBasketByAll();
}
