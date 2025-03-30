var socket = io.connect('http://' + window.location.hostname + ':' + location.port);

        // Listen for 'update_counter' events from the server
        socket.on('update_counter', function(data) {
            document.querySelector('.counter').textContent = data.value;
        });