var socket = io.connect('http://' + window.location.hostname + ':' + location.port);

// Listen for the server's response (no event name needed with `send`)
socket.on('message', function(data) {
    console.log("Received counter value:", data.value);
    document.querySelector('.counter').textContent = data.value;
});