import requests
import time

TELEGRAM_TOKEN = "8536751491:AAGL-tHAopsb_4P1-DjFFau2F6bYkRKccSQ"
CHAT_ID = "7419789130"

URL = "https://skinport.com/api/items"

PARAMS = {
    "sort": "percent",
    "order": "desc",
    "pricegt": 0,
    "pricelt": 5000,
    "wearlt": 0.002,  # API oldali szűrés is
    "exterior": "2,4,3,5,1"
}

seen_ids = set()


def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(telegram_url, data={
            "chat_id": CHAT_ID,
            "text": message
        }, timeout=10)
    except Exception as e:
        print("Telegram hiba:", e)


def check_items():
    global seen_ids

    try:
        response = requests.get(URL, params=PARAMS, timeout=15)
        response.raise_for_status()
        items = response.json()
    except Exception as e:
        print("API hiba:", e)
        return

    for item in items:
        item_id = item.get("saleId")
        float_value = item.get("wear")

        if item_id is None or float_value is None:
            continue

        # Csak új item
        if item_id in seen_ids:
            continue

        # FLOAT SZŰRÉS
        if float_value < 0.002:
            seen_ids.add(item_id)

            price_eur = item.get("salePrice", 0) / 100
            market_name = item.get("marketName", "Ismeretlen item")

            message = (
                f"🔥 ULTRA LOW FLOAT!\n\n"
                f"{market_name}\n"
                f"Float: {float_value:.8f}\n"
                f"Ár: {price_eur:.2f} €\n\n"
                f"https://skinport.com/item/{item_id}"
            )

            print("Találat:", market_name, float_value)
            send_telegram(message)


if __name__ == "__main__":
    print("Low float figyelő elindult...")

    while True:
        check_items()
        time.sleep(60)  # 60 másodpercenként ellenőriz
