// Get Search Bar Width
const searchForm = document.getElementById('searchForm');
var styles = window.getComputedStyle(searchForm);
const width = styles.width;
console.log("Search Bar Width: " + width);


// Resize Settings
const settings = document.getElementById('settings');

settings.setAttribute('style', 'width: ' + width + 'px;');
styles = window.getComputedStyle(settings);

console.log("Width: " + styles.width);