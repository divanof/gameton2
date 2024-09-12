// script.js
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');

async function readArrayFromFile(filePath) {
    const response = await fetch(filePath);
    const text = await response.text();
    return text.trim().split('\n').map(row => row.split(',').map(Number));
}

function drawArray(array) {
    const squareSize = 50; // Size of each square
    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array[i].length; j++) {
            const color = getColor(array[i][j]);
            ctx.fillStyle = color;
            ctx.fillRect(j * squareSize, i * squareSize, squareSize, squareSize);
        }
    }
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
    try {
        const array = [
            [1, 2, 3, 3, 2],
            [2, 2, 2, 1, 3],
            [2, 1, 2, 1, 3],
            [1, 2, 3, 1, 3]
        ];
        drawArray(array);
    } catch (error) {
        console.error('Error reading file:', error);
    }
}

main();
