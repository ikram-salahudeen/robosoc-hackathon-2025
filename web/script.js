var socket = io.connect('http://' + window.location.hostname + ':' + location.port);

// Request to start stream
socket.emit('start_stream');

// Receive frames from server
socket.on('video_frame', function(data) {
        document.getElementById('video_feed').src = 'data:image/jpeg;base64,' + data.image;
});