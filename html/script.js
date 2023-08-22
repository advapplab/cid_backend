document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('reset');

    resetButton.addEventListener('click', function(ev) {
        location.reload();
        console.log('reset');
        ev.preventDefault();
    }, false);

});