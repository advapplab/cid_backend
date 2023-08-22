




console.log("begin");

var currentURL = window.location.href;
console.log(currentURL);

var global_width = 768
var global_height = 512


document.getElementById('reset').addEventListener('click', function() {
    location.reload();
});


document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('webcam');
    // const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-button');
    // const ctx = canvas.getContext('2d');

    // Adjust these constraints to get the desired resolution
    const constraints = {
        video: {
            width: global_width,
            height: global_height,
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

    // captureButton.addEventListener('click', function() {
    //     ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    // });
});