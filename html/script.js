




console.log("begin");

var currentURL = window.location.href;
console.log(currentURL);

resetbutton = document.getElementById('resetbutton');

resetbutton.addEventListener('click', function(ev) {
    location.reload();
    ev.preventDefault();
}, false);

// document.getElementById('reset').addEventListener('click', function() {
//     location.reload();
// });