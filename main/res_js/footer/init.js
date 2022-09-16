document.addEventListener('click', function(e) {
    if (e.target.id != profile.getProfilePopupBtnId()) {
      profile.hidePopup();
    }
  });