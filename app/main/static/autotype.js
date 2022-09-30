try{
    var searchBar = document.getElementById('searchText');

    var keywords = ['How do you write a class in Java?',
                    'What is OOP?',
                    'How do you write assembly language?',
                    'What is casting in C++?',
                    'How do you define variables in JavaScript?',
                    'What is CSS?'];

    var index = 0;
    var arrCounter = 0;
    var focus = false;
    var timer1, timer2;

    function resetBox() {
        searchBar.setAttribute('placeholder',"");
        searchBar.value = '';
        index = 0;
        autoType();
    }

    var autoType = function() {

        if (focus) {
            return;
        }

        if (index <= keywords[arrCounter].length) {
            searchBar.value = keywords[arrCounter].substr(0, index++);
            timer1 = setTimeout("autoType()", 50);
        } else {

            arrCounter++;
            if(arrCounter === keywords.length){
                arrCounter = 0;
            }

            timer2 = setTimeout(resetBox, 5000);
        }
    };

    autoType();
    $("#searchText").on("focus", function(){
        focus = true;
        searchBar.setAttribute('placeholder',"Start typing...");
        searchBar.value = '';
        clearTimeout(timer1);
        clearTimeout(timer2);

    }).on("blur", function(){
        setTimeout(function() {
            focus = false;
            resetBox();
        }, 1000);
    });
}
catch(err) {}