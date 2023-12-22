let affichage = document.querySelector(".statistique");

console.log(affichage);

afficher()
function afficher(){
    if(affichage.style.opacity === "0"){
        affichage.style.opacity = "1";
        affichage.style.maxHeight = "1000px"; 
   
    } else {
        affichage.style.opacity = "0";
        affichage.style.maxHeight = "0";

    }
}