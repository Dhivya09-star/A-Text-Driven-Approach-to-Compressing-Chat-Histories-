import re, time, json
from pathlib import Path

INPUT_PATH = Path("/Users/ayishasalmira/Downloads/emoji-compress-project /chat_preprocessed.txt")
OUTPUT_COMPRESSED = Path("compressed_seed.txt")
OUTPUT_DICT = Path("seed_dictionary.json")

text = INPUT_PATH.read_text(encoding="utf-8", errors="ignore")
SEED_MAP = { 

    "hi": "👋",
    "hello": "🤗",
    "good morning": "🌅",
    "good evening": "🌆",

    "please": "🙏🏼",
    "thank you": "🙏",
    "thanks": "🫶",
    "thank you very much": "🤝",
    "no problem": "😌",

    "sorry": "🙇",
    "sorry for the inconvenience": "🙇‍♂️",

    "lol": "😂",
    "haha": "😆",
    "lmao": "🤣",
    "rofl": "🤪",
    "omg": "😱",
    "idk": "🤷",
    "wtf": "😳",
    "brb": "🏃‍♂️",

    "i need help": "🚨",
    "let me know": "📩",
    "give me a moment": "⏲️",
    "just a moment": "⏱️",
    "please wait a moment": "⏳",
    "i will check": "🔎",
    "how can i help you": "💬",

    "order id": "🆔",
    "your order has been shipped": "📦",
    "delivery is delayed": "🚚💤",

    "have a great day": "🌞",
    "have a nice day": "🌼",
    "talk to you soon": "🕊️",

    "issue has been resolved": "✅"
}

def validate_unique(d):
    seen = {}
    for k, v in d.items():
        if v in seen:
            raise ValueError(f"Emoji conflict for '{k}' and '{seen[v]}' -> {v}")
        seen[v] = k

validate_unique(SEED_MAP)
def compress(text, dictionary):
    items = sorted(dictionary.items(), key=lambda x: len(x[0]), reverse=True)
    for phrase, emoji in items:
        text = re.sub(rf"\b{re.escape(phrase)}\b", emoji, text, flags=re.IGNORECASE)
    return text

def decompress(text, dictionary):
    reverse = {v: k for k, v in dictionary.items()}
    for emoji, phrase in reverse.items():
        text = text.replace(emoji, phrase)
    return text

t0 = time.time()
compressed = compress(text, SEED_MAP)
t1 = time.time()

orig_bytes = len(text.encode("utf-8"))
comp_bytes = len(compressed.encode("utf-8"))
saved_bytes = orig_bytes - comp_bytes
ratio = comp_bytes / orig_bytes
lossless = (decompress(compressed, SEED_MAP) == text)

print("\n=== SEED COMPRESSION METRICS ===")
print(json.dumps({
    "original_size_bytes": orig_bytes,
    "compressed_size_bytes": comp_bytes,
    "saved_bytes": saved_bytes,
    "compression_ratio": round(ratio, 4),
    "lossless_reversible": lossless,
    "time_ms": round((t1 - t0) * 1000, 2),
}, indent=2))

print("\n=== SAMPLE COMPRESSED OUTPUT ===")
print(compressed[:500])

OUTPUT_COMPRESSED.write_text(compressed, encoding="utf-8")
OUTPUT_DICT.write_text(json.dumps(SEED_MAP, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"\n[OK] Saved compressed output → {OUTPUT_COMPRESSED.resolve()}")
print(f"[OK] Saved seed dictionary → {OUTPUT_DICT.resolve()}")
