function  getAdresse(){
    const lieuValue = document.getElementById('lieu').innerText;
    const addressSplit = lieuValue.split(" ");
    const addressReconstruct = addressSplit.join("+");
    return addressReconstruct;
}

const address = getAdresse();
console.log(address);
let API_KEY = "AIzaSyD6OQZ9MSy_zphm1WHjcO4tSRvUue8Q93g"

let iframe = document.getElementById('map');
iframe.src = `https://www.google.com/maps/embed/v1/place?key=${API_KEY}&q=${address}`;