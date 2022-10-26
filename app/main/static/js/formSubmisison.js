// Default Vars
var searchQuery, redirectLink="/loading";
// Ajax Vars
URL = "/calls";


// Function executed whwn submitting the form
function execute(){
    // Get User Query
    var searchBar = document.getElementById('searchText');
    searchQuery = searchBar.value;
    // Printing stuff for debug
    changeURL("/query", searchQuery, true);
    //fetch("loading")
    // changeURL("/loading")
    query = {'query': searchQuery};
    $.post("/query/", query);
    // Redirect URL
    //changeURL("/resultPage", searchQuery, true);

}
// Event Listeners
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

// function search2Param(query) {
//     return encodeURI(query);
// }

// function search2Param(query) {
//     return encodeURI(query);
// }

// function getURL() {
//     return window.location.href;
// }

// function splitOnLast(rawString, splitStr) {
//     const lastIndex = rawString.lastIndexOf(splitStr);
//     return rawString.slice(0, lastIndex);
// } 

// function giveURL(localPage, params="", redirect=false) {
//     params = "?query=" + params;
//     if (redirect == false){
//         return splitOnLast(document.location.href, '/')+localPage+params;
//     }
//     else{
//         return localPage+params;
//     }
// }

// function changeURL(localPage, params="", redirect=false) {
//     params = "?query=" + params;
//     if (redirect == false){
//         window.location.href = splitOnLast(document.location.href, '/')+localPage+params;
//     }
//     else{
//         window.location.href = localPage+params;
//     }
// }