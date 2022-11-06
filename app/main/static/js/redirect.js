
function setRedirect(query) {
  results = getCookie("numResults");
  currentUrl = getURL();
  console.log(getQuery(currentUrl)); // Returns http://127.0.0.1:8000/loading
  var numResult_param = "?numResults=" + results, query_param = "?query=" + getQuery(currentUrl);
  document.getElementsByTagName("meta")[2].setAttribute("content", "0; URL=/resultPage/" + numResult_param + query_param);
  //document.querySelector('meta[name="viewport"]').setAttribute("content", "width=device-width, initial-scale=1.0");
}
setRedirect();

// Functions to use
function search2Param(query) {
    return encodeURIComponent(query);
}

function param2Search(query) {
    return decodeURIComponent(query);
}

function getURL() {
    return window.location.href;
}

function splitOnLast(rawString, splitStr) {
    const lastIndex = rawString.lastIndexOf(splitStr);
    return rawString.slice(0, lastIndex);
}

function getQuery(rawString) {
    const lastIndex = rawString.lastIndexOf("/");
    return rawString.replace(rawString.slice(0, lastIndex), "").replace("/?query=", "");
}


function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
