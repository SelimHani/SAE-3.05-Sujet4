
r

function openNav() {
    const sidenav = document.querySelector('.sidenav');


    if (window.innerWidth <= 600) { // Ajout de la condition pour changer la largeur en 100% si la taille de l'écran est inférieure ou égale à 600 pixels
        sidenav.style.width = "100%";
        sidenav.style.height = "100%";
    } else {
        sidenav.style.width = "250px";
    }

    document.getElementById("tdb").style.zIndex = "-1";
}
  
function closeNav() {
    

    setTimeout(function() {
        console.log("test");
        document.getElementById("tdb").style.zIndex = "0";
        
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
    