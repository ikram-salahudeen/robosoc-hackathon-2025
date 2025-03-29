setInterval(() => {
    fetch("/")
        .then(response => response.text())
        .then(html => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, 'text/html');
            document.getElementById("dynamic").innerText = doc.getElementById("dynamic").innerText;
        });
}, 2000);