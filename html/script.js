document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('reset');

    resetbutton.addEventListener('click', function(ev) {
        location.reload();
        ev.preventDefault();
    }, false);

});