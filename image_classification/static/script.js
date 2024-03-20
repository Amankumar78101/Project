
let cameraStream = null; // to store the camera stream
let captureCount = 0; // to keep track of captured images count
function captureImage() {
    var video = document.getElementById('video');
    var canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL('image/png');
    document.getElementById('image_data').value = dataURL; // Ensure the field name is 'image_data'
    document.getElementById('folder').value = document.getElementById('folderInput').value;
    // Submit the form asynchronously using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('Image captured successfully.');
            // Update image container only when a new image is saved
            updateImageContainer(dataURL);
        } else {
            console.error('Error capturing image:', xhr.statusText);
        }
    };
    xhr.send(new URLSearchParams(new FormData(document.getElementById('form'))));
    captureCount++; // Increment capture count
    if (captureCount < 10) {
        setTimeout(captureImage, 500); // Capture next image after 500 milliseconds
    } else {
        captureCount = 0; // Reset capture count after capturing 10 images
    }
}


function updateImageContainer(imageURL) {
    // Create a new image element and append it to the image container
    var img = document.createElement('img');
    img.src = imageURL;
    img.width = 200;
    img.height = 150;
    document.getElementById('imageContainer').appendChild(img);
}

function startCamera() {
    var video = document.getElementById('video');
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
            video.play();
            // store the camera stream
            cameraStream = stream; // Assign the stream to the global variable
        })
        .catch(function(error) {
            console.error('Error accessing the camera:', error);
        });
    } else {
        console.error('getUserMedia not supported on your browser');
    }
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => {
            track.stop();
        });
    }
}

// Make sure the DOM content is loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('startCameraBtn').addEventListener('click', function() {
        startCamera(); // Start the camera when the button is clicked
    });

    document.getElementById('captureBtn').addEventListener('click', function() {
        if (cameraStream) {
            captureImage(); // Call captureImage function on button click only if the camera stream is active
        } else {
            console.error('Camera not started yet!');
        }
    }); 
    
    document.getElementById('removeFolderBtn').addEventListener('click', function() {
        var folderToRemove = document.getElementById('removeFolderInput').value;
        document.getElementById('remove_folder').value = folderToRemove;
        // Submit the form asynchronously using AJAX when the remove folder button is clicked
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Folder removal request sent successfully.');
            } else {
                console.error('Error sending folder removal request:', xhr.statusText);
            }
        };
        xhr.send(new URLSearchParams(new FormData(document.getElementById('form'))));
    });
});

// Allow capturing image when 'S' or 's' key is pressed
document.addEventListener('keydown', function(event) {
    if (event.key === 's' || event.key === 'S') {
        if (cameraStream) {
            captureImage();
        } else {
            console.error('Camera not started yet!');
        }
    }
});
