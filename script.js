var script = document.createElement('script');
script.src = 'https://html2canvas.hertzen.com/dist/html2canvas.min.js';
script.onload = function() {
    console.log('jQuery loaded!');
};
document.head.appendChild(script);


function sendKey(element, key) {
    var keyCode, code;

    // Determine keyCode and code based on key input
    if (key >= '0' && key <= '9') {
        // Number keys
        keyCode = key.charCodeAt(0);
        code = 'Digit' + key;
    } else {
        // Arrow keys
        switch (key) {
            case 'ArrowDown':
                keyCode = 40;
                code = 'ArrowDown';
                break;
            case 'ArrowUp':
                keyCode = 38;
                code = 'ArrowUp';
                break;
            case 'ArrowLeft':
                keyCode = 37;
                code = 'ArrowLeft';
                break;
            case 'ArrowRight':
                keyCode = 39;
                code = 'ArrowRight';
                break;
            default:
                console.error('Unsupported key: ' + key);
                return;
        }
    }

    // Create the keydown event
    var event = new KeyboardEvent('keydown', {
        key: key,
        keyCode: keyCode,
        code: code,
        which: keyCode,
        bubbles: true,
        cancelable: true
    });

    // Dispatch the event to the element
    element.dispatchEvent(event);
}

const upload = () => {
    html2canvas(document.querySelector("#game")).then(canvas => {
        // send the canvas to the server
        data = canvas.toDataURL("image/jpeg").split(';base64,')[1];
        // using fetch to send the image to the localhost server port 5000 endpoint /upload
        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: JSON.stringify({image: data}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())  // expecting a json response
        .then(data => {
            for (let i = 0; i < 9; i++) {
                if (i % 2 == 0)
                    for (let j = 0; j < 9; j++) {
                        if (data.data.origin[i][j] == 0) {
                            sendKey(document.body, data.data.board[i][j]+'')
                        }
                        sendKey(document.body, 'ArrowRight')
                    }
                else 
                    for (let j = 8; j >= 0; j--) {
                        if (data.data.origin[i][j] == 0) {
                            sendKey(document.body, data.data.board[i][j]+'')
                        }
                        sendKey(document.body, 'ArrowLeft')
                    }
                sendKey(document.body, 'ArrowDown')
            }
        });
    });    
};

