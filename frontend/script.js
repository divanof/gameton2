const BACK_URL = "http://127.0.0.1:8000/"
const canvas = document.getElementById('Canvas');
const ctx = canvas.getContext('2d');
const squareSize = 20;
let globalMap = null;


function drawArray(array) {
    console.log('bbb', array);
    
    array.forEach(cell => {
        ctx.fillStyle = getColor(cell["type"]);
        console.log(cell["x_draw"], cell["y_draw"])
        ctx.fillRect(cell["x_draw"] * squareSize, cell["y_draw"] * squareSize, squareSize, squareSize);
    })
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


function transformData2Map(data) {
    let units = data["units"];
    let world = data["world"];
    
    units_keys = ["base", "enemyBlocks", "zombies"];

    let coords = Array();
    world["zpots"].forEach(element => {
        coords.push({"x": element["x"], "y": element["y"]});
    });
    units_keys.forEach(key => {
        units[key].forEach(element => {
            coords.push({"x": element["x"], "y": element["y"]});
        })
    });
    
    let min_x = Math.min(...coords.map(coord => coord.x));
    let min_y = Math.min(...coords.map(coord => coord.y));
    let returnArray = Array();
    console.log(min_x, min_y, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');

    world["zpots"].forEach(element => {
        element["x_draw"] = element["x"] - min_x;
        element["y_draw"] = element["y"] - min_y;
        element["type"] = 1
        returnArray.push(element);
    });
    units_keys.forEach(key => {
        units[key].forEach(element => {
            element["x_draw"] = element["x"] - min_x;
            element["y_draw"] = element["y"] - min_y;
            console.log(element["x_draw"], element["y_draw"]);
            let value = 0;
            switch (key) {
                case "base":
                    value = 2;
                    break;
                case "enemyBlocks":
                    value = 3;
                    break;
                case "zombies":
                    value = 4;
                    break;
            }
            element["type"] = value;
            returnArray.push(element);
        })
    });
    globalMap = returnArray;

    return returnArray;
}


async function getMap(callback) {
    fetchData('GET', BACK_URL + 'map', null, null, (error, data) => {
        if (error) {
            console.error(error);
        } else {
            data = JSON.parse(data);
            console.log(data);

            const map_data = transformData2Map(data);

            console.log('aaa', map_data);

            callback(map_data);
        }
    });
}


function getColor(type) {
    switch (type) {
        case 1:
            return 'gray'; 
        case 2:
            return 'blue'; 
        case 3:
            return 'red'; 
        case 4:
            return 'green'
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
        x = Math.floor(x / squareSize);
        y = Math.floor(y / squareSize);
        console.log(`Клик по клетке: (${x}, ${y})`);
        const target = globalMap.find(cell => cell.x_draw === x && cell.y_draw === y);
        if (!target) return;
        console.log('Найдено:', target);

        fetchData('POST', BACK_URL + 'action/', JSON.stringify({'x': target["x"], 'y': target["y"], 'action': 'move'}), null, 
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
        drawArray(data);
    });
}

main();
