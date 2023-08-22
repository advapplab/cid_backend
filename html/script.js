document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('reset');

    resetbutton.addEventListener('click', function(ev) {
        location.reload();
        console.log('reset');
        ev.preventDefault();
    }, false);

});