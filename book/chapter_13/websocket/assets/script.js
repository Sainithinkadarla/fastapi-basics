const IMAGE_INTERVAL_MS = 42;

const drawObjects = (video, canvas, objects) => {
  const ctx = canvas.getContext('2d');

  // Set context dimensions based on the video element's current size
  // Note: ctx.width/height is not a standard property, we use canvas.width/height
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  ctx.beginPath();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const object of objects.objects) {
    const [x1, y1, x2, y2] = object.box;
    const label = object.label;
    
    // Draw bounding box
    ctx.strokeStyle = '#49fb35';
    ctx.lineWidth = 2; // Added line width for better visibility
    ctx.beginPath();
    ctx.rect(x1, y1, x2 - x1, y2 - y1);
    ctx.stroke();

    // Draw label
    ctx.font = 'bold 16px sans-serif';
    ctx.fillStyle = '#ff0000';
    // Adjust label position for better visibility (above the box)
    ctx.fillText(label, x1, y1 - 5); 
  }
};

// Updated function signature: No deviceId, assumes video.srcObject is already set or is about to be set
const startObjectDetection = (video, canvas) => {
  // Ensure the video is loaded and playing before starting the socket and interval
  if (video.readyState < 2) { // HTMLMediaElement.HAVE_CURRENT_DATA
    console.log('Video not ready yet, waiting for "loadeddata" event...');
    return null; 
  }

  const socket = new WebSocket(`ws://${location.host}/predict`);
  let intervalId;

  // Connection opened
  socket.addEventListener('open', function () {
    video.play().then(() => {
      // Adapt overlay canvas size to the video size
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // Send an image in the WebSocket every 42 ms
      intervalId = setInterval(() => {
        // Create a virtual canvas to draw current video image
        const tempCanvas = document.createElement('canvas'); // Renamed to tempCanvas to avoid conflict
        const ctx = tempCanvas.getContext('2d');
        tempCanvas.width = video.videoWidth;
        tempCanvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

        // Convert it to JPEG and send it to the WebSocket
        tempCanvas.toBlob((blob) => socket.send(blob), 'image/jpeg');
      }, IMAGE_INTERVAL_MS);
    });
  });

  // Listen for messages
  socket.addEventListener('message', function (event) {
    drawObjects(video, canvas, JSON.parse(event.data));
  });

  // Stop the interval and video playback on socket close
  socket.addEventListener('close', function () {
    window.clearInterval(intervalId);
    video.pause();
    // Revoke the Object URL to free up memory if it was used
    if (video.src.startsWith('blob:')) {
        URL.revokeObjectURL(video.src);
    }
  });

  // Handle errors
  socket.addEventListener('error', (error) => {
    console.error("WebSocket Error:", error);
    window.clearInterval(intervalId);
    video.pause();
  });


  return socket;
};

window.addEventListener('DOMContentLoaded', (event) => {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  // New element: file input for video upload
  const videoUpload = document.getElementById('video-upload'); 
  let socket;
  
  // The video stream is not played automatically, we rely on the video playback starting 
  // after the socket is open in startObjectDetection.
  
  // --- New Logic to handle Video File Selection ---
  videoUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];
    
    if (!file || !file.type.startsWith('video/')) {
        alert('Please select a valid video file.');
        return;
    }

    // Close previous socket if there is one
    if (socket) {
      socket.close();
      socket = null; // Clear the reference
    }

    // Create a local URL for the selected file
    const videoURL = URL.createObjectURL(file);
    video.src = videoURL;
    
    // Clear previous object URL after the video metadata is loaded
    video.addEventListener('loadedmetadata', function cleanup() {
        // Adapt overlay canvas size to the video size (can be done here too)
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Start detection once the file is loaded and we have its dimensions
        socket = startObjectDetection(video, canvas);
        
        // The cleanup listener is only needed once
        video.removeEventListener('loadedmetadata', cleanup); 
    });
    
    // Optionally: Automatically trigger playback and detection when the file is ready to play
    video.addEventListener('canplay', function startDetectionOnReady() {
        if (!socket) { // Only start if it hasn't been started by loadedmetadata
             // This can be an alternative or a fallback to loadedmetadata
             // socket = startObjectDetection(video, canvas);
        }
        video.removeEventListener('canplay', startDetectionOnReady);
    });
  });
  
  // Clean up the initial webcam listing and submission logic
  // The original code for listing cameras and the form-connect listener are removed.
});