import requests
import time
import re

TELEGRAM_TOKEN = "8536751491:AAGL-tHAopsb_4P1-DjFFau2F6bYkRKccSQ"
CHAT_ID = "7419789130"

URL = "https://skinport.com/api/items"

PARAMS = {
    "sort": "percent",
    "order": "desc",
    "pricegt": 0,
    "pricelt": 5000,
    "wearlt": 0.1,
    "exterior": "2,4,3,5,1"
}

seen_ids = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_items():
    global seen_ids
    
    response = requests.get(URL, params=PARAMS)
    data = response.json()
    
    for item in data:
        item_id = item.get("saleId")
        float_value = str(item.get("wear", ""))
        
        if item_id not in seen_ids:
            seen_ids.add(item_id)
            
            if float_value.endswith("000") or float_value.endswith("001"):
                msg = f"🔥 ÚJ FLOAT!\n\n{item['marketName']}\nFloat: {float_value}\nÁr: {item['salePrice']/100}€"
                send_telegram(msg)

while True:
    try:
        check_items()
        time.sleep(60)
    except:
        time.sleep(60)
