const searchContainer = document.querySelector('.barra_busqueda')
const inputSearch = searchContainer.querySelector('input')
const boxSuggestions = document.querySelector('.contenedor-sugerencias')

inputSearch.addEventListener('keyup', function (e) {
    let userData = inputSearch.value;
    let emptyArray = [];

    if (userData) {
        emptyArray = suggestions.filter(data => {
            return data.toLocaleLowerCase().includes(userData.toLocaleLowerCase());
        });

        emptyArray = emptyArray.map(data => {
            return '<li>' + data + '</li>';
        });
        searchContainer.classList.add('active');
        showSuggestions(emptyArray);

        let allList = boxSuggestions.querySelectorAll('li');
        allList.forEach(li => {
            li.onclick = function () { select(this); };
        });
    } else {
        searchContainer.classList.remove('active');
        boxSuggestions.innerHTML = '';
    }
});

function select(element) {
    let selectUserData = element.textContent;
    inputSearch.value = selectUserData;
    searchContainer.classList.remove('active');
    boxSuggestions.innerHTML = '';
}

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        let userValue = inputSearch.value;
        listData = '<li>' + userValue + '</li>';
    } else {
        listData = list.join('');
    }
    boxSuggestions.innerHTML = listData;
}