let libros = document.getElementsByClassName('libro')
let autores = document.getElementsByClassName('autor')
let array = [];
for(var i = 0; i < libros.length; i++){
    array.push(libros[i].innerHTML);
    array.push(autores[i].innerHTML);
}

for(var i = 0; i < array.length; i++){
    libroActual = array[i];

    if(libroActual.slice(-1) == ' '){
        libroActual = libroActual.slice(0, -1);
        array[i] = libroActual;
    }
}
let result = [...new Set(array)];

// console.log(result);
let suggestions = result