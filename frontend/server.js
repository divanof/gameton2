const http = require('http');
const fs = require('fs');
const path = require('path');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
    // Определяем путь к файлу на основе URL запроса
    let filePath = './frontend' + req.url;
    if (filePath === './frontend/') {
        filePath = './frontend/index.html';
    }
    
    // Определяем расширение файла
    const extname = String(path.extname(filePath)).toLowerCase();

    // Устанавливаем MIME-тип в зависимости от расширения файла
    let contentType = 'text/html; charset=utf-8';
    switch (extname) {
        case '.js':
            contentType = 'text/javascript; charset=utf-8';
            break;
        case '.css':
            contentType = 'text/css; charset=utf-8';
            break;
        case '.json':
            contentType = 'application/json; charset=utf-8';
            break;
        case '.png':
            contentType = 'image/png';
            break;
        case '.jpg':
            contentType = 'image/jpg';
            break;
        case '.wav':
            contentType = 'audio/wav';
            break;
    }
    console.log(filePath);
    fs.readFile(filePath, function(err, content) {
        if (err) {
            if (err.code === 'ENOENT') {
                // Файл не найден
                res.writeHead(404, {'Content-Type': 'text/plain; charset=utf-8'});
                res.end('404 Not Found');
            } else {
                // Другая ошибка
                res.writeHead(500, {'Content-Type': 'text/plain; charset=utf-8'});
                res.end('Ошибка при загрузке файла.');
                console.log(err.message);
            }
        } else {
            // Файл найден, отправляем его с правильным MIME-типом
            res.writeHead(200, {'Content-Type': contentType});
            res.end(content, 'utf-8');
        }
    });
});

server.listen(port, hostname, () => {
    console.log(`Сервер запущен по адресу http://${hostname}:${port}/`);
});
