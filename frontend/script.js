const BACK_URL = "http://147.45.254.214:8000/"
const squareSize = 20;
const canvas = document.getElementById('mapCanvas');
const ctx = canvas.getContext('2d');

const originalMapSize = { x: 15000, y: 15000 };
const scaledWidth = canvas.width;
const scaledHeight = canvas.height;

const scaleX = scaledWidth / originalMapSize.x;
const scaleY = scaledHeight / originalMapSize.y;


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
    fetchData('GET', BACK_URL + 'map', null, null, (error, data) => {
        if (error) {
            console.error(error);
        } else {
            data = JSON.parse(data);
            console.log(data);

            callback(data);
        }
    });
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
    setInterval(() => {
        getMap((data) => {
            console.log(data);
            drawMap(data);
        });
    }, 200);
    // document.addEventListener('keydown', (event) => {
    //     processKeyboard(event);
    // });

    // canvas.addEventListener('click', (event) => {
    //     const rect = canvas.getBoundingClientRect();
    //     var x = event.x - rect.left;
    //     var y = event.y;
    //     x = Math.floor(x / squareSize);
    //     y = Math.floor(y / squareSize);
    //     console.log(`Клик по клетке: (${x}, ${y})`);
    //     const target = globalMap.find(cell => cell.x_draw === x && cell.y_draw === y);
    //     if (target)
    //         console.log('Найдено:', target);

    //     fetchData('POST', BACK_URL + 'action/', JSON.stringify({'x': x + min_x, 'y': y + min_y, 'action': 'move'}), null, 
    //         (error, data) => {
    //             if (error) {
    //                 console.error(error);
    //             } else {
    //                 alert(data);
    //             }
    //         }
    //     )
    // })
}

function drawAnomalies(data) {
    ctx.lineWidth = 5; // Толщина границы
    data.anomalies.forEach(anomaly => {
        if (anomaly.x >= -1000 && anomaly.x <= originalMapSize.x && anomaly.y >= -1000 && anomaly.y <= originalMapSize.y) {
            const radius = Math.round(anomaly.radius * scaleX); // Умножаем на 20 и масштабируем
            const effectiveRadius = Math.round(anomaly.effectiveRadius * scaleX); // Умножаем на 20 и масштабируем
         
            ctx.fillStyle = 'black';
            ctx.beginPath();
            ctx.arc(anomaly.x * scaleX, anomaly.y * scaleY, radius, 0, Math.PI * 2);
            ctx.fill();

            // Окружность для effectiveRadius (незакрашенная)
            ctx.strokeStyle = 'black'; // Цвет контура
            if (anomaly.strength < 0)
                ctx.fillStyle = 'rgba(255, 140, 0, 0.3)';
            else
                ctx.fillStyle = 'rgba(75, 0, 130, 0.3)';
            
            ctx.beginPath();
            ctx.arc(anomaly.x * scaleX, anomaly.y * scaleY, effectiveRadius, 0, Math.PI * 2);
            ctx.fill(); // Отрисовываем только контур
        }
    });
}

function drawTransports(data) {
    ctx.fillStyle = 'green';
    data.transports.forEach(transport => {
        if (transport.x >= -1000 && transport.x <= originalMapSize.x && transport.y >= -1000 && transport.y <= originalMapSize.y) {
            ctx.fillRect(transport.x * scaleX - 10, transport.y * scaleY - 10, 40 * scaleX, 40 * scaleY);
        }
    });
}

function drawEnemies(data) {
    ctx.fillStyle = 'red';
    data.enemies.forEach(enemy => {
        if (enemy.x >= -1000 && enemy.x <= originalMapSize.x && enemy.y >= -1000 && enemy.y <= originalMapSize.y) {
            ctx.fillRect(enemy.x * scaleX - 10, enemy.y * scaleY - 10, 40 * scaleX, 40 * scaleY);
        }
    });
}

function drawAnomalyLabels(data) {
    ctx.fillStyle = 'black'; // Цвет текста
    ctx.font = '12px Arial'; // Шрифт и размер текста
    data.anomalies.forEach(anomaly => {
        if (anomaly.x >= -1000 && anomaly.x <= originalMapSize.x && anomaly.y >= -1000 && anomaly.y <= originalMapSize.y) {
            const xPos = anomaly.x * scaleX;
            const yPos = anomaly.y * scaleY;
            ctx.fillText(anomaly.strength, xPos - 10, yPos + 20); // Печатаем ID немного ниже центра
        }
    });
}
function drawBounties(data) {
    ctx.strokeStyle = 'yellow'; // Цвет контура для bounty
    ctx.lineWidth = 3; // Толщина границы для bounty
    data.bounties.forEach(bounty => {
        if (bounty.x >= -1000 && bounty.x <= originalMapSize.x && bounty.y >= -1000 && bounty.y <= originalMapSize.y) {
            const bountyRadius = Math.round(bounty.radius * scaleX); // Умножаем на 20 и масштабируем
            ctx.beginPath();
            ctx.arc(bounty.x * scaleX, bounty.y * scaleY, bountyRadius, 0, Math.PI * 2);
            ctx.stroke(); // Отрисовываем только контур
        }
    });
}
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}


function drawMap(data) {
    clearCanvas();
    drawAnomalies(data);
    drawTransports(data);
    drawEnemies(data);
    drawBounties(data);
    drawAnomalyLabels(data);
}

async function main() {
    setEvents();
}

main();
