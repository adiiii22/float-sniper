import requests
import time
import os

TELEGRAM_TOKEN = os.getenv("8536751491:AAGL-tHAopsb_4P1-DjFFau2F6bYkRKccSQ")
CHAT_ID = os.getenv("7419789130")

URL = "https://skinport.com/api/items"

PARAMS = {
    "sort": "percent",
    "order": "desc",
    "pricegt": 0,
    "pricelt": 5000,
    "wearlt": 0.002,
    "exterior": "2,4,3,5,1"
}

seen_ids = set()

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Connection": "keep-alive"
})


def send_telegram(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram token vagy chat_id nincs beállítva!")
        return

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = session.post(
            telegram_url,
            data={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )
        print("Telegram status:", response.status_code)
    except Exception as e:
        print("Telegram hiba:", e)


def check_items():
    global seen_ids

    try:
        response = session.get(URL, params=PARAMS, timeout=20)
        print("Skinport status:", response.status_code)

        if response.status_code != 200:
            print("Nem 200-as válasz, várunk...")
            return

        items = response.json()
        print("Lekért itemek száma:", len(items))

    except Exception as e:
        print("API hiba:", e)
        return

    for item in items:
        item_id = item.get("saleId")
        float_value = item.get("wear")

        if not item_id or float_value is None:
            continue

        if item_id in seen_ids:
            continue

        if float_value < 0.002:
            seen_ids.add(item_id)

            price_eur = item.get("salePrice", 0) / 100
            market_name = item.get("marketName", "Ismeretlen item")

            message = (
                f"🔥 ULTRA LOW FLOAT!\n\n"
                f"{market_name}\n"
                f"Float: {float_value:.8f}\n"
                f"Ár: {price_eur:.2f} €\n"
                f"https://skinport.com/item/{item_id}"
            )

            print("Találat:", market_name, float_value)
            send_telegram(message)


if __name__ == "__main__":
    print("Low float figyelő elindult Railway-en...")

    while True:
        check_items()
        time.sleep(60)
