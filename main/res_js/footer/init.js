document.addEventListener('click', function(e) {
    if (e.target.id != profile.getProfilePopupBtnId()) {
      profile.hidePopup();
    }
  });

function initSelectCurently(){

  let opt;
  let currencies = document.getElementById("data-currencies");
  const select = document.getElementById("select-curently");

  if(currencies && select){
    
    currencies = JSON.parse(currencies.innerHTML);
    currencies = currencies["currencies"];

    currencies.forEach(item => {
      opt = document.createElement('option');
      opt.value = item;
      opt.innerHTML = item;
      select.appendChild(opt);
    })

    ApiStripe.initCheckOut();
  }
}