function get() {
    // Set up parameter calling
    var allParams = new URLSearchParams(window.location.search);
    var query;
    // Retrieve parameter name
    query = allParams.get("query");
    // console.log("Query:", query);
    return query;
}

function setSearchBarValue(){
    // Get Search form value
    var searchBar = document.getElementById('searchText');
    // console.log("Search Bar Name:", searchBar.name);
    if (searchBar.name == "result"){
        searchBar.setAttribute('value',get());
    }
}

//console.log(get());
setSearchBarValue();

/*
$.ajax({
            type: "post",
            url: window.location.href,
            cache: false,
            async: 'asynchronous',
            dataType: 'html',
            data: get(),
            success: function(data) {
                console.log(data)
            },
            error: function(request, status, error){
                console.log("Error: " + error)
            }
        })
*/
