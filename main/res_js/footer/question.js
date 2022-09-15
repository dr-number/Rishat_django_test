class Question{

    init(){

        const listElements = document.querySelectorAll(".yes, .no");
        
        if(listElements){
            listElements.forEach(button => {
                button.onclick = () => {

                if(button.hasAttribute("function"))
                        eval(button.getAttribute("function"))

                }
            });
        }

    }
}