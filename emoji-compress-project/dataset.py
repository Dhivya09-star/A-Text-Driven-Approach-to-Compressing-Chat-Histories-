from pathlib import Path
from datetime import datetime, timedelta
import random
import csv

OUT_CSV = Path("conversations_ec_support.csv")

random.seed(42)

CUSTOMER_FIRST = ["Aarav","Diya","Ishaan","Meera","Arjun","Anaya","Kabir","Sara","Rohan","Nisha",
                  "Liam","Emma","Noah","Olivia","Ethan","Ava","Mia","Lucas","Sofia","Amelia"]
AGENT_FIRST    = ["Alex","Jordan","Taylor","Casey","Morgan","Riley","Sam","Drew","Jamie","Devin"]

PRODUCTS = ["wireless earbuds","smartwatch","phone case","gaming mouse","laptop stand",
            "USB-C charger","Bluetooth speaker","LED light strip","fitness band","power bank"]

ISSUES = [
    "delayed delivery", "wrong item received", "defective product", "return status",
    "refund not processed", "cancellation request", "exchange request", "payment failed",
    "coupon not applied", "warranty claim"
]
PHRASES = {
    "en": {
        "greet_cust": ["Hi", "Hello", "Hey"],
        "greet_agent": ["Hi there!", "Hello! Thanks for contacting support.", "Hello! How can I help you today?"],
        "ask_help": ["I need help with my order", "I have a question about my order", "Can you help me with my order?"],
        "thanks": ["thank you", "thanks", "thank you very much"],
        "closing": ["Have a great day!", "Is there anything else I can help with?", "Take care!"],
        "hold": ["please wait a moment", "one moment please", "let me check that for you"],
        "confirm": ["Sure, I can help with that", "I can assist you with that", "I’ll be glad to help"],
        "ask_id": ["please share your order id", "could you provide the order id", "may I have your order id"],
        "provide_id": ["my order id is", "the order id is", "order id"],
        "resolve": ["issue has been resolved", "your refund has been initiated", "your replacement is arranged"],
        "apology": ["sorry for the inconvenience", "I apologize for the trouble", "we’re sorry about that"]
    },
    "hi": {
        "greet_agent": ["नमस्ते! मैं कैसे मदद कर सकता हूँ?", "नमस्ते! मैं आपकी सहायता करूंगा।"],
        "thanks": ["धन्यवाद", "बहुत धन्यवाद"],
        "ask_id": ["कृपया अपना ऑर्डर आईडी साझा करें"],
        "apology": ["असुविधा के लिए क्षमा करें"]
    },
    "es": {
        "greet_agent": ["¡Hola! ¿En qué puedo ayudarte?", "¡Hola! Gracias por contactar al soporte."],
        "thanks": ["gracias", "muchas gracias"],
        "ask_id": ["por favor comparte tu id de pedido"],
        "apology": ["disculpa las molestias"]
    }
}

def rand_time(start_dt: datetime, idx: int) -> str:
    return (start_dt + timedelta(minutes=idx*random.randint(1,3))).strftime("%Y-%m-%d %H:%M")

def pick(seq): return random.choice(seq)

def make_conversation(conv_id: int) -> list[dict]:
    rows = []
    start = datetime(2025, 1, 15, 10, 0) + timedelta(days=random.randint(0, 40))
    cust = pick(CUSTOMER_FIRST)
    agent = pick(AGENT_FIRST)
    lang = random.choices(["en","en","en","hi","es"], weights=[70,0,0,15,15], k=1)[0]  
    product = pick(PRODUCTS)
    issue = pick(ISSUES)
    order_id = f"ORD{random.randint(100000,999999)}"

    t = 1
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"customer","sender":cust,"language":lang,"message": pick(PHRASES["en"]["greet_cust"]) + ","})
    t+=1
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"agent","sender":agent,"language":lang,
                 "message": pick(PHRASES.get(lang,PHRASES["en"])["greet_agent"])})
    t+=1
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"customer","sender":cust,"language":"en",
                 "message": f"{pick(PHRASES['en']['ask_help'])} — {issue} with my {product}."})
    t+=1
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"agent","sender":agent,"language":lang,
                 "message": f"{pick(PHRASES['en']['confirm'])}, {pick(PHRASES.get(lang,PHRASES['en'])['ask_id'])}."})
    t+=1
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"customer","sender":cust,"language":"en",
                 "message": f"{pick(PHRASES['en']['provide_id'])} {order_id}."})
    t+=1
    
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"agent","sender":agent,"language":"en",
                 "message": f"{pick(PHRASES['en']['hold'])}… {pick(PHRASES.get(lang,PHRASES['en'])['apology'])}."})
    t+=1
  
    res_msg = random.choice([
        f"Your {product} {pick(['replacement is arranged','refund has been initiated','will arrive tomorrow'])}.",
        f"We have verified {issue}; {pick(PHRASES['en']['resolve'])}."
    ])
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"agent","sender":agent,"language":"en","message": res_msg})
    t+=1
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"customer","sender":cust,"language":lang,"message": pick(PHRASES.get(lang,PHRASES['en'])['thanks'])})
    t+=1
    rows.append({"conv_id": conv_id, "turn": t, "timestamp": rand_time(start,t),
                 "role":"agent","sender":agent,"language":"en","message": pick(PHRASES['en']['closing'])})

    return rows

def generate_dataset(n_conversations=60):
    all_rows = []
    for cid in range(1, n_conversations+1):
        all_rows.extend(make_conversation(cid))
    return all_rows

def write_csv(rows, out_path: Path):
    fields = ["conv_id","turn","timestamp","role","sender","language","message"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

if __name__ == "__main__":
    rows = generate_dataset(n_conversations=60)  
    write_csv(rows, OUT_CSV)
    print(f"[OK] Wrote {len(rows)} rows to {OUT_CSV.resolve()}")
