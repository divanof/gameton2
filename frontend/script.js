const BACK_URL = "http://127.0.0.1:8000/"
const canvas = document.getElementById('myCanvas');
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

    xhr.send();
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

async function main() {
    document.addEventListener('keydown', (event) => {
        const key = event.key;
        const outputDiv = document.getElementById('output');
        outputDiv.textContent = `Нажата клавиша: ${key}`;
    });

    try {
        getMap(function(data) {
            console.log(data);
            drawArray(data['map']);
        });
    } catch (error) {
        console.error('Error reading file:', error);
    }
}

main();
