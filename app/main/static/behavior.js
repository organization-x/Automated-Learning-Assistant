function get () {
  // Set up parameter calling
  var allParams = new URLSearchParams(window.location.search), query;
  
  // Retrieve parameter name
  query = allParams.get("query");
  return query;
}

console.log(get())