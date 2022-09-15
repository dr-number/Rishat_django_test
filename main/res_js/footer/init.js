const ajaxServer = new AjaxServer();

const modals = new Modals(ajaxServer);

const question = new Question();



document.addEventListener('click', function(e) {
    if (e.target.id != profile.getProfilePopupBtnId()) {
      profile.hidePopup();
    }
  });