/*
To do list:
1) Create cookies if nonexistent
2) If user has data stored in cookies, transfer the values from cookies to HTML
3) If user close settings, take the data from settings
*/

// If settingClicked == true, then settings popup shows
var settingClicked = 0, buttonClicked=false;


// Main Code
// Transfer cookies to HTML
cookieStart();

// Data transferred when settings is closed
function settings(){
    // Get Settings
    radioButton = radioButtonGet();
    roadmap = roadmapGet();
    numResults = numResultGet();
    tilting = tiltingGet();
    // Upload to cookies
    cookieCreate_Time(radioButton, roadmap, numResults);
    console.log("Radio Button: " + radioButton);
    console.log("Roadmap: " + roadmap);
    console.log("Tilting: " + tilting);
    console.log("Num Results: " + numResults);
    console.log("Cookie Created: " + document.cookie);
}

/*
Cookies Section
*/

// Never Expire Cookie
function cookieCreate_Time(radioButton, roadmap, numResults, tilting){
    const daysToExpire = new Date(2147483647 * 1000).toUTCString();
    document.cookie = "radioButton=" + radioButton + ";" +' expires=' + daysToExpire + "; path=/";
    document.cookie = "roadmap=" + roadmap + ";" +' expires=' + daysToExpire + "; path=/";
    document.cookie = "tilting=" + tilting + ";" +' expires=' + daysToExpire + "; path=/";
    document.cookie = "numResults=" + numResults + ";" +' expires=' + daysToExpire + "; path=/";
    console.log(document.cookie);
}

// Get Cookie Value
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

// Update Document from Cookies
function cookieStart() {
    // Long CookieString
    // Cookie names
    var cookieString;
    var radioButton, roadmap, numResults, tilting;
    const radioCheck = document.cookie.indexOf("radioButton=");
    const roadCheck = document.cookie.indexOf("roadmap=");
    const resultCheck = document.cookie.indexOf("numResults=");
    const tiltingCheck = document.cookie.indexOf("tilting=");
    if (radioCheck <= -1 || roadCheck <= -1 || resultCheck <= -1 || tiltingCheck <= -1) {
        cookieCreate_Time(radioButtonGet(), roadmapGet(), numResultGet());
    }
    else {
        radioButton = getCookie("radioButton");
        roadmap = getCookie("roadmap");
        numResults = getCookie("numResults");
        tilting = getCookie("tilting");
        // Apply cookie to document
        // Themes
        radioButtonSet(radioButton);
        roadmapSet(roadmap);
        tiltingSet(tilting);
        numResultSet(numResults);
    }
}

/*
Execution Section
*/
// Executes when settings is closed
function exitSettings() {
    settingClicked = 0;
    console.log("Settings Exit: " + settingClicked);
    buttonClicked = false;
    settings();
    return;
}

// Executes when settings is opened
function enterSettings() {
    console.log("Settings Entered: " + settingClicked);
    buttonClicked = true;
    return;
}


/*
Necessary stuff below! Don't Change!!!
*/
// Set Settings
function radioButtonSet(value){
    var themes = document.getElementsByName('themes');
        for(i = 0; i < themes.length; i++) {
            if(themes[i].checked){
                // Add changes to stuff if the element is checked
                if (themes[i].id != value){
                    themes[i].checked = false;
                    document.querySelector('#'+value).checked = true;
                    document.getElementById(themes[i].id + "Button").classList.remove('active');
                    document.getElementById(value + "Button").classList.add('active');
                }
            }
        }
}
function roadmapSet(value){
    var roadMap = document.querySelector('#buttonroadMap');
    var buttonPress = document.getElementById("buttonroadMap");
    console.log("Value before: " + value);
    if (value == "true"){
        value = "roadmap";
    }
    else {
        value = "";
    }
    console.log("Value: " + value);
    roadMap.setAttribute('roadmap', value);
    if (roadMap.getAttribute('roadmap') == "roadmap" && hasClass(buttonPress, 'active') == false){
        buttonPress.classList.add('active');
    }
    else if (roadMap.getAttribute('roadmap') != "roadmap" && hasClass(buttonPress, 'active') == true) {
        buttonPress.classList.remove('active');
    }
}
function tiltingSet(value){
    var tilting = document.querySelector('#buttonTilting');
    var buttonPress = document.getElementById("buttonTilting");
    console.log("Value before: " + value);
    if (value == "true"){
        value = "tilting";
    }
    else {
        value = "";
    }
    console.log("Value: " + value);
    tilting.setAttribute('tilting', value);
    if (tilting.getAttribute('tilting') == "tilting" && hasClass(buttonPress, 'active') == false){
        buttonPress.classList.add('active');
    }
    else if (tilting.getAttribute('tilting') != "tilting" && hasClass(buttonPress, 'active') == true) {
        buttonPress.classList.remove('active');
    }
}
function numResultSet(value){
    if (value > 4){
        value = 4;
    }
    numResult = document.getElementById("numResult").setAttribute('value', value);
}


// Read Settings
function radioButtonGet(){
    var themes = document.getElementsByName('themes');
        for(i = 0; i < themes.length; i++) {
            if(themes[i].checked){
                // Add changes to stuff if the element is checked
                return themes[i].id;
            }
        }
}
function roadmapGet(){
    var roadMap = document.querySelector('#buttonroadMap');
    if (roadMap.getAttribute('roadmap') == "roadmap"){
        return true;
    }
    else {
        return false;
    }
}
function tiltingGet(){
    var tilting = document.querySelector('#buttonTilting');
    if (tilting.getAttribute('tilting') == "tilting"){
        return true;
    }
    else {
        return false;
    }
}
function numResultGet() {
    numResult = document.getElementById("numResult").value;
    if (numResult > 4){
        numResult = 4;
        document.getElementById("numResult").setAttribute('value', numResult);
    }
    return numResult;
}
// Modify Settings
function upload2cookies(theme, roadMap){
    // Change button display
    themeButton = document.getElementsByName(theme.id + 'Button');
    roadMapButton = document.getElementsByName(roadMap.id + 'Button');
    // Assign
}
/*
Event listeners
*/
// Create func to check if there's a class inside
function hasClass(el,classname){
      if(el.classList.contains(classname)){
          return true;
      }else{
          return false;
      }
   }


// Execute if Settings have been clicked
function settingsCheck() {
    if (settingClicked == 0 && hasClass(document.getElementById('settingsBody'), "show") == true) {
        settingClicked = 1;
        enterSettings();
        return "enter";
    }
}

// Event Listeners
// Settings
function settingsPopup() {
    var buttonPress = document.getElementById("settingButton");
    buttonPress.addEventListener("click", function(event) {
        settingsCheck();
        event.preventDefault();
    });
}

function addClassNameListener(elemId, targetChange, funcDoAfter) {
    var elem = document.getElementById(elemId);
    var clickPrev = false, clickNow = false;
    window.setInterval(function() {
        if (hasClass(document.getElementById(elemId), targetChange) == true) {
            clickNow = true;
        }
        else{
            if (clickPrev == true){
                clickPrev = false;
            }
            if (clickNow == true){
                clickPrev = true;
                clickNow = false;
                funcDoAfter();
            }
        }
    },10);
}

// Activate listeners
function activateListeners() {
    settingsPopup();
    addClassNameListener("settingsBody", "show", function(){exitSettings();});
}
activateListeners();
