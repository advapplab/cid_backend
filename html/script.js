document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('resetButton');

    resetbutton.addEventListener('click', function(ev) {
        location.reload();
        ev.preventDefault();
    }, false);

});