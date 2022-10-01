var searchQuery, redirectLink="/resultPage";

// Function executed whwn submitting the form
function execute(){
    // Get User Query
    var searchBar = document.getElementById('searchText');
    searchQuery = searchBar.value;
    // Printing stuff for debug
    query = {'query': searchQuery};
    $.post("/query/", query);
    console.log(searchQuery);
    alert(search2Param(searchQuery));
    // Redirect URL
    changeURL("/resultPage", searchQuery);
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
    console.log("string slice: ", str.slice(0, lastIndex));
    return str.slice(0, lastIndex);
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