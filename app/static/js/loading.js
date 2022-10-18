window.rtimeOut=function(callback,delay){
    requestId = undefined;
    var dateNow=Date.now,
        requestId=window.requestAnimationFrame,
        start=dateNow(),
        stop,
        timeoutFunc=function(){
            dateNow()-start<delay?stop||requestId(timeoutFunc):callback()
        };
    requestId(timeoutFunc);
    return requestId;
}

var searchBar = document.getElementById('period');

var keywords = ['...'];
var index = 0;
var arrCounter = 0;
var timer1, timer2, requestID, stopCode = false;

function resetBox() {
    index = 0;
    
    searchBar.innerText="";
    if (stopCode == true){
        return 0;
    }
    startTyping();
}

// Replaced setTimeout with window.requestAnimation due to critical dependency of performance of 

var autoTypeBackward = function() {
    if (stopCode == true){
            return 0;
        }
    /*
    if (index ==  keywords[arrCounter].length) {
        console.log("Start Backwords");
    }
    */
    if ( index >= 0) {
        searchBar.innerText = keywords[arrCounter].substr(0, index--);
        timer1 = window.rtimeOut(autoTypeBackward,100);
        //timer1 = setTimeout("autoTypeBackward()", 50);
    } else {
        timer2 = setTimeout(resetBox, 100);
        if ((arrCounter+1) == keywords.length){
            arrCounter = 0;
        }
        else{
            arrCounter += 1;
        }
    }
};

var autoTypeForward = function() {
    if (stopCode == true){
            return 0;
        }
    /*
    if (index ==  0) {
        console.log("Start Forwards");
    }
    */
    if (index <= keywords[arrCounter].length) {
        searchBar.innerText = keywords[arrCounter].substr(0, index++);
        // timer1 = setTimeout("autoTypeForward()", 50);
        timer1 = window.rtimeOut(autoTypeForward,100);
    } else {
        index -= 1;
        timer2 = setTimeout(autoTypeBackward, 0);
    }
};

function startTyping(){
    var searchBar = document.getElementById('period');
    // console.log("Search Bar Name:", searchBar.name);
    stopCode = false;
    autoTypeForward();
}

startTyping();

$("#searchText").on("focus", function(){
    startTyping();
});
