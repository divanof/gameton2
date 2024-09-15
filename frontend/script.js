const BACK_URL = "http://127.0.0.1:8000/"
const canvas = document.getElementById('Canvas');
const ctx = canvas.getContext('2d');

async function readArrayFromFile(filePath) {
    const response = await fetch(filePath);
    const text = await response.text();
    return text.trim().split('\n').map(row => row.split(',').map(Number));
}

function drawArray(array) {
    const squareSize = 50;
    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].length; j++) {
            const color = getColor(array[i][j]);
            ctx.fillStyle = color;
            ctx.fillRect(j * squareSize, i * squareSize, squareSize, squareSize);
        }
    }
}


function fetchData(method, url, payload, headers, callback) {
    const xhr = new XMLHttpRequest();

    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(null, xhr.responseText);
            } else {
                callback(`Error: ${xhr.status}`, null);
            }
        }
    };

    xhr.onerror = function() {
        callback('Request failed', null);
    };

    xhr.send(payload);
}


async function getMap(callback) {
    fetchData('GET', BACK_URL + 'map', null, null, function(error, data) {
        if (error) {
            console.error(error);
        } else {
            data = JSON.parse(data);
            callback(data);
        }
    });
}


function getColor(type) {
    switch (type) {
        case 1:
            return 'red'; 
        case 2:
            return 'green'; 
        case 3:
            return 'blue'; 
        default:
            return 'white'; 
    }
}

function processKeyboard(event) {
    var key = event.key.toLowerCase();
    
    if (!['w', 'a', 's', 'd',  ' '].includes(key)) {
        console.log(key);
        return;
    }
    if (key === ' ')
        key = 'space';

    fetchData('POST', BACK_URL + key +'_key_action/', null, null, 
        (error, data)=>{
            if (error) {
                console.error(error);
            } else {
                alert(data);
            }
        }
    )
}

function setEvents() {
    document.addEventListener('keydown', (event) => {
        processKeyboard(event);
    });

    canvas.addEventListener('click', (event) => {
        const rect = canvas.getBoundingClientRect();
        var x = event.x - rect.left;
        var y = event.y;
        x = Math.floor(x / 50);
        y = Math.floor(y / 50);
        console.log(`Клик по клетке: (${x}, ${y})`);
        fetchData('POST', BACK_URL + 'action/', JSON.stringify({'x': x, 'y': y, 'action': 'move'}), null, 
            (error, data) => {
                if (error) {
                    console.error(error);
                } else {
                    alert(data);
                }
            }
        )
    })
}

async function main() {
    setEvents();

    getMap((data) => {
        console.log(data);
        drawArray(data['map']);
    });
}

main();
