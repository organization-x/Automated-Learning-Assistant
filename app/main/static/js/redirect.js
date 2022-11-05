
function setRedirect(query) {
  results = getCookie("numResults");
  currentUrl = getURL();
  console.log(splitOnLast(currentUrl, "/"));
  //document.querySelector('meta[name="viewport"]').setAttribute("content", "width=device-width, initial-scale=1.0");
}
setRedirect();

// Functions to use
function search2Param(query) {
    return encodeURI(query);
}

function param2Search(query) {
    return encodeURI(query);
}

function getURL() {
    return window.location.href;
}

function splitOnLast(rawString, splitStr) {
    const lastIndex = rawString.lastIndexOf(splitStr);
    return rawString.slice(0, lastIndex);
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
