class Profile{

    #profilePopupBtn = document.getElementById("profile-popup-btn");
    #profilePopup = document.querySelector(".profile-popup")

    constructor(){
        this.#popup()
    }

    #popup(){

        if(this.#profilePopupBtn)
            this.#profilePopupBtn.onclick = () => {
                this.#profilePopup.classList.toggle("d-none");
            }
    }

    getProfilePopupBtnId(){
        return this.#profilePopupBtn.getAttribute("id");
    }

    hidePopup(){
        this.#profilePopup.classList.add("d-none");
    }
}

const profile = new Profile();