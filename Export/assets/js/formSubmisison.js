// Default Vars
var searchQuery, redirectLink="/result.html";
// Ajax Vars
URL = "/calls";

// Function executed whwn submitting the form
function execute(){
    // Get User Query
    var searchBar = document.getElementById('searchText');
    searchQuery = searchBar.value;
    // Printing stuff for debug
    console.log("URL: ", "/calls");
    console.log("Query1: ", searchQuery);
    //alert(search2Param(searchQuery));
    // Ajax calls
    console.log("Ajax before");
  //  upload(searchQuery);
    console.log("Ajax after");
    // Redirect URL
    changeURL(redirectLink, searchQuery, false);
}

// AJAX Call
function upload(query) {
    var data = {'query': query};
    $.post(URL, data, function(response){
        if(response === 'success') {
            alert('Yay!');
        }
        else {
            alert('Error! :(');
        }
    });
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
    params = "?query=" + params;
    if (redirect == false){
        return splitOnLast(document.location.href, '/')+localPage+params;
    }
    else{
        return localPage+params;
    }
}

function changeURL(localPage, params="", redirect=false) {
    params = "?query=" + params;
    if (redirect == false){
        window.location.href = splitOnLast(document.location.href, '/')+localPage+params;
    }
    else{
        window.location.href = localPage+params;
    }
}