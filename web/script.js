setInterval(() => {
    fetch("/")
        .then(response => response.text())
        .then(html => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, 'text/html');
            document.getElementById("dynamic").innerText = doc.getElementById("dynamic").innerText;
        });
}, 2000);

const socket = io(); //socketio connection to server//
socket.on("connect", () => {
    console.log("connected");
    document.getElementById("status").innerHTML = "Connected";
});

socket.on("disconnect", () => {
 console.log("disconnected");
        document.getElementById("status").innerHTML = "Disconnected";
});

function myupdate() {
  //Event sent by Client
 socket.emit("my_event", function() {
 });
}

// Event sent by Server//
socket.on("server", function(msg) {
        let myvar = JSON.parse(msg.data1);
        //Check if entire data is sent by server//
        if (myvar == "4") {
                document.getElementById("demo").innerHTML = "";
                document.querySelector('#checkbutton').innerText = "Submit";
                document.getElementById("checkbutton").style.cursor = "pointer";
                document.getElementById("checkbutton").disabled = false;
                document.getElementById("checkbutton").className = "btn btn-primary";
 
        }

        else {
                document.getElementById("demo").innerHTML += msg.data + "<br>";
                document.getElementById("checkbutton").disabled = true;
                document.getElementById("checkbutton").innerHTML = "Loading..";
                document.getElementById("checkbutton").style.cursor = "not-allowed";
                document.getElementById("checkbutton").style.pointerEvents = "auto";
        }
});