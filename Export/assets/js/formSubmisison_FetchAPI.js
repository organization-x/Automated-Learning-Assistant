/*
// Default Vars
var searchQuery, redirectLink="/result.html", URL;

// Function executed whwn submitting the form
function execute(){
    // Get User Query
    var searchBar = document.getElementById("searchText");
    if (searchBar == null){
        var searchBar = document.getElementById("searchText_Result");
    }
    searchQuery = searchBar.value;
    // Setting up redirect URL and form to store data
    URL = giveURL(redirectLink, search2Param(searchQuery), false);
    const formBody = {query: searchQuery};
    // Printing stuff for debug
    console.log("Start debug")
  //  upload(searchQuery);
    alert(formBody);
    POST(formBody, URL);
    console.log("End debug");
    // Redirect URL
}

// Requests

function POST(formBody, URL) {
    const options = {
        method: 'POST',
        body: JSON.stringify(formBody),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(URL, options)
    .then(res => res.json())
    .then(res => console.log(res));
}

// Event Listerners
function submitButton() {
    var buttonPress = document.getElementById("searchButton");
    buttonPress.addEventListener("click", function(event) {
        execute();
        event.preventDefault();
    });
}

function submitEnterKey() {
    var submittedQuery = document.getElementById("searchText");
    if (submittedQuery == null){
        var submittedQuery = document.getElementById("searchText_Result");
    }
    submittedQuery.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            execute();
            event.preventDefault();
        }
    });
}


submitEnterKey()
submitButton()

// Pass search info

function search2Param(query) {
    return encodeURI(query);
}

function search2Param(query) {
    return encodeURI(query);
}

function getURL() {
    return window.location.href;
}

function splitOnLast(rawString, splitStr) {
    const lastIndex = rawString.lastIndexOf(splitStr);
    return rawString.slice(0, lastIndex);
} 

function giveURL(localPage, params="", redirect=false) {
    params = "?q=" + params;
    if (redirect == false){
        return splitOnLast(document.location.href, '/')+localPage+params;
    }
    else{
        return localPage+params;
    }
}

function changeURL(localPage, params="", redirect=false) {
    params = "?q=" + params;
    if (redirect == false){
        window.location.href = splitOnLast(document.location.href, '/')+localPage+params;
    }
    else{
        window.location.href = localPage+params;
    }
}

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}
*/