const divFormulaire = document.querySelector('#formulaire');


function openNav() {
    const sidenav = document.querySelector('.sidenav');
    if (window.innerWidth <= 600) { 
        sidenav.style.width = "100%";
        sidenav.style.height = "100%";
        divFormulaire.style.zIndex = "-1";
    } else {
        sidenav.style.width = "250px";
        divFormulaire.style.zIndex = "0";

    }
}
  
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    divFormulaire.style.zIndex = "0";
    
}

let url = window.location.href;
if(url === "http://127.0.0.1:5000/"){
    document.getElementById("mySidenav").style.left = "-2.8vh";
    console.log("Page acceuil");
}else{
    console.log("Autre page");
}
    