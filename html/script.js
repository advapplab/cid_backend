




console.log("begin");

var currentURL = window.location.href;
console.log(currentURL);




document.getElementById('reset').addEventListener('click', function() {
    location.reload();
});


document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');
    const ctx = canvas.getContext('2d');

    // Adjust these constraints to get the desired resolution
    const constraints = {
        video: {
            width: 1280,
            height: 720,
            facingMode: 'user'
        }
    };

    navigator.mediaDevices.getUserMedia(constraints)
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error("Error accessing webcam: ", error);
        });

    captureButton.addEventListener('click', function() {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    });
});