
from flask import Flask
import threading
import requests
import random
import time
from bs4 import BeautifulSoup
import urllib3

app = Flask(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# جلب بروكسيات جديدة
def fetch_proxies():
    print("جاري تحميل البروكسيات...")
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxies = []
    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        ip = cols[0].text.strip()
        port = cols[1].text.strip()
        https = cols[6].text.strip()
        if https == "yes":
            proxy = f"http://{ip}:{port}"
            proxies.append(proxy)
        if len(proxies) >= 500:
            break
    print(f"تم تحميل {len(proxies)} بروكسي")
    return proxies

# تنفيذ زيارة واحدة
def send_visit(session, proxy):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/15.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/96.0.4664.45 Safari/537.36"
        ])
    }
    session.headers.update(headers)
    session.proxies = {"http": proxy, "https": proxy}
    try:
        response = session.get("https://nibras-ai.netlify.app", timeout=10, verify=False)
        if response.status_code == 200:
            print(f"زيارة ناجحة من {proxy}")
        else:
            print(f"زيارة فاشلة ({response.status_code}) من {proxy}")
    except Exception as e:
        print(f"فشل الوصول من {proxy}: {e}")

# حلقة التكرار اليومية
def bot_loop():
    total_visits = 500000
    while True:
        print("\n=== بدء دورة زيارات جديدة ===")
        proxies_list = fetch_proxies()
        for i in range(total_visits):
            proxy = random.choice(proxies_list)
            session = requests.Session()
            send_visit(session, proxy)
            time.sleep(0.5)
            if i % 100 == 0:
                print(f"تم تنفيذ {i} زيارة")
        print("اكتملت 500,000 زيارة. انتظار 24 ساعة للدورة القادمة...")
        time.sleep(86400)

# تشغيل البوت في الخلفية
threading.Thread(target=bot_loop).start()

# صفحة رئيسية لإبقاء Glitch شغال
@app.route("/")
def home():
    return "البوت شغال حالياً!"

if __name__ == "__main__":
    app.run()
