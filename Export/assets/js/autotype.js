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

var searchBar = document.getElementById('searchText');

var keywords = ['How do you write a class in Java?',
                'What is OOP?',
                'How do you write assembly language?',
                'What is casting in C++?',
                'How do you define variables in JavaScript?',
                'What is CSS?'];
var index = 0;
var arrCounter = 0;
var timer1, timer2, requestID, stopCode = false;

function resetBox() {
    index = 0;
    searchBar.setAttribute('placeholder', '');
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
    console.log("Start backwards");
    if ( index >= 0) {
        searchBar.setAttribute('placeholder', keywords[arrCounter].substr(0, index--));
        timer1 = window.rtimeOut(autoTypeBackward,50);
        //timer1 = setTimeout("autoTypeBackward()", 50);
    } else {
        timer2 = setTimeout(resetBox, 2500);
        if ((arrCounter+1) == keywords.length){
            arrCounter = 0;
        }
        else{
            arrCounter += 1;
        }
		console.log("Word Done");
    }
};

var autoTypeForward = function() {
    if (stopCode == true){
            return 0;
        }
    //console.log("Start forwards");
    if (index <= keywords[arrCounter].length) {
        searchBar.setAttribute('placeholder', keywords[arrCounter].substr(0, index++));
        // timer1 = setTimeout("autoTypeForward()", 50);
        timer1 = window.rtimeOut(autoTypeForward,50);
    } else {
        index -= 1;
        timer2 = setTimeout(autoTypeBackward, 2500);
		//console.log("Word Done");
    }
};

function startTyping(){
    stopCode = false;
    autoTypeForward();
}

function stopTyping(){
    if (timer1){
        window.cancelAnimationFrame(timer1);
        timer1 = undefined;
        console.log("timer1 stopped");
    }
    if (timer2){
        clearTimeout(timer2);
        timer2 = undefined;
        console.log("timer2 stopped");
    }
    if (requestID){
        window.cancelAnimationFrame(requestID);
        requestID = undefined;
        console.log("requestID stopped");
    }
    searchBar.setAttribute('placeholder', '');
}

startTyping();

$("#searchText").on("focus", function(){
    stopCode = true;
    searchBar.setAttribute('placeholder','Start typing...');
}).on("blur", function(){
    console.log("Stopped Typing");
    setTimeout(function() {
        startTyping();
    });
});

