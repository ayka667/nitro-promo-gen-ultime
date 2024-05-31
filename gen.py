import requests, time
import concurrent.futures
import os, uuid, ctypes
import datetime
import hashlib
import sys
from random import choice
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def clearConsole():
    return os.system("cls" if os.name in ("nt", "dos") else "clear")

class Counter:
     count = 0

class PromoGenerator:
    red = '\x1b[31m(-)\x1b[0m'
    blue = '\x1b[34m(+)\x1b[0m'
    green = '\x1b[32m(+)\x1b[0m'
    yellow = '\x1b[33m(!)\x1b[0m'

    def __init__(self, proxy=None):
        self.proxy = proxy
        self.session = self.create_session()

    def create_session(self):
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def generate_promo(self):
        url = "https://api.discord.gx.games/v1/direct-fulfillment"
        headers = {
            "Content-Type": "application/json",
            "Sec-Ch-Ua": '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
        }

        data = {
            "partnerUserId": str(uuid.uuid4())
        }

        try:
            if self.proxy:
                formatted_proxy = f"http://{self.proxy}"
                response = self.session.post(url, json=data, headers=headers, proxies={'http': formatted_proxy, 'https': formatted_proxy}, timeout=5)
            else:
                response = self.session.post(url, json=data, headers=headers, timeout=5)

            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    Counter.count += 1
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Opera Gx Promo Gen | Made By Jsuispashumain | Generated : {Counter.count}")
                    link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
                    with open("promos.txt", "a+") as f:
                        f.write(f"{link}\n")
                    print(f"{self.get_timestamp()} {self.green} Generated Promo Link : {link}")
            elif response.status_code == 429:
                print(f"{self.get_timestamp()} {self.yellow} You Are Being Rate-limited!")
            else:
                print(f"{self.get_timestamp()} {self.red} Request failed : {response.status_code}")
        except Exception as e:
            print(f"{self.get_timestamp()} {self.red} Request Failed : {e}")

    @staticmethod
    def get_timestamp():
        time_idk = time.strftime('%H:%M:%S')
        return f'[\x1b[90m{time_idk}\x1b[0m]'

class Password:
    def __init__(self, password, expiry_date):
        self.password = password
        self.expiry_date = expiry_date

    def check_password(self, entered_password):
        return self.get_hash(entered_password) == self.get_hash(self.password)

    def check_expiry(self):
        return datetime.datetime.now() < self.expiry_date

    def get_hash(self, password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

d1 = datetime.datetime(2054, 1, 23, 23, 59)
password = Password('KEY', d1)

clearConsole()
entered_password = input("Enter your key: ")
clearConsole()

if password.check_password(entered_password):
    if password.check_expiry():
        print("Connected successfully")
        time.sleep(3)
        clearConsole()

    else:
        print("Your key has expired")
        time.sleep(3)
        sys.exit()

else:
    print("Invalid key")
    time.sleep(3)
    sys.exit()


class PromoManager:
    def __init__(self):
        self.num_threads = int(input(f"{PromoGenerator.get_timestamp()} {PromoGenerator.blue} This key will expire on {d1}\n{PromoGenerator.get_timestamp()} {PromoGenerator.blue} Enter Number Of Threads : "))
        with open("proxies.txt") as f:
            self.proxies = f.read().splitlines()

    def start_gen(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = {executor.submit(self.generate_promo): i for i in range(self.num_threads)}
            try:
                concurrent.futures.wait(futures)
            except KeyboardInterrupt:
                for future in concurrent.futures.as_completed(futures):
                    future.result()

    def generate_promo(self):
        proxy = choice(self.proxies) if self.proxies else None
        generator = PromoGenerator(proxy)
        while True:
            generator.generate_promo()

if __name__ == "__main__":
    manager = PromoManager()
    manager.start_gen()