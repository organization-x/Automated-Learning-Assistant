// Add listeners for buttons
function lightToggle() {
    var buttonPress = document.getElementById("lightButton");
    buttonPress.addEventListener("click", function(event) {
        darkButton = document.getElementById("darkButton");
        // Change button bold
        darkButton.classList.remove('active');
        buttonPress.classList.add('active');
    });
}
function darkToggle() {
    var buttonPress = document.getElementById("darkButton");
    buttonPress.addEventListener("click", function(event) {
        lightButton = document.getElementById("lightButton");
        lightButton.classList.remove('active');
        buttonPress.classList.add('active');
    });
}
function roadMapToggle() {
    var roadMap = document.querySelector('#buttonroadMap');
    var buttonPress = document.getElementById("buttonroadMap");
    
    if (roadMap.getAttribute('roadmap') == "roadmap" && hasClass(buttonPress, 'active') == false){
        buttonPress.classList.add('active');
    }
    else if (roadMap.getAttribute('roadmap') != "roadmap" && hasClass(buttonPress, 'active') == true) {
        buttonPress.classList.remove('active');
    }
    
    buttonPress.addEventListener("click", function(event) {
        if (roadMap.getAttribute('roadmap') != "roadmap"){
            buttonPress.classList.add('active');
            roadMap.setAttribute('roadmap', 'roadmap');
        }
        else if (roadMap.getAttribute('roadmap') == "roadmap") {
            buttonPress.classList.remove('active');
            roadMap.setAttribute('roadmap', '');
        }
    });
}

function hasClass(el,classname){
      if(el.classList.contains(classname)){
          return true;
      }else{
          return false;
      }
   }

function runEventTogglers() {
    lightToggle();
    darkToggle();
    roadMapToggle();
}
runEventTogglers();