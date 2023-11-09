
let etat = false;

function openNav() {
    const sidenav = document.querySelector('.sidenav');


    if (window.innerWidth <= 600) { 
        sidenav.style.width = "100%";
        sidenav.style.height = "100%";
        etat = true;
    } else {
        sidenav.style.width = "250px";
        etat = true
    }

    try {
        document.getElementById("scroll").style.zIndex = "-1";
    } catch (error) {
        document.getElementById("tdb").style.zIndex = "-1";
    }
    
}
  
function closeNav() {
    
    etat = false
    setTimeout(function() {
        try {
            document.getElementById("scroll").style.zIndex = "0";
        } catch (error) {
        document.getElementBId("tdb").style.zIndex = "0";
        }
        console.log("test2");
        
    }, 300);
    document.getElementById("mySidenav").style.width = "0";
    

}

let url = window.location.href;
if(url === "http://127.0.0.1:5000/"){
    document.getElementById("mySidenav").style.left = "-2.8vh";
    console.log("Page acceuil");
}else{
    console.log("Autre page");
}
    
document.addEventListener("click", (event) =>{
    const sidenav = document.querySelector('.sidenav');
        if(sidenav.style.width <= event.clientX){
            console.log("touche");
            closeNav();
    }
})