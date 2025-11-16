import re, json, time
from collections import Counter
from itertools import islice
from pathlib import Path

PRE_PATH = Path("chat_preprocessed.txt")
SEED_DICT_PATH = Path("seed_dictionary.json")
OUT_DICT_PATH = Path("full_dictionary.json")
OUT_COMP_PATH = Path("compressed_full.txt")

text = PRE_PATH.read_text(encoding="utf-8", errors="ignore")
seed_map = json.loads(SEED_DICT_PATH.read_text(encoding="utf-8"))

EMOJI_POOL = list("😀😁😂🤣😅😊😍🤩🤔🙃😴🥳💡⭐🔥⚡🎯✨☀️🌙💬📨📦🔔🔍🧭🧩💾📌📍")

def tokenize(t):
    return re.findall(r"[a-zA-Z0-9@.\-+']+|[\u0900-\u097F]+|[\u00C0-\u024F]+", t.lower())

def find_phrases(tokens, n):
    for i in range(len(tokens)-n+1):
        yield " ".join(tokens[i:i+n])

tokens = tokenize(text)
freq = Counter()

for n in (2,3,4):
    freq.update(find_phrases(tokens, n))
filtered = [(p,c) for p,c in freq.items()
            if c >= 3 and len(p) > 5 and not p.isdigit()]

filtered.sort(key=lambda x: (len(x[0]), x[1]), reverse=True)

def pick_non_overlapping(candidates):
    chosen = []
    for phrase, count in candidates:
        if any(phrase in c or c in phrase for c,_ in chosen):
            continue
        chosen.append((phrase,count))
        if len(chosen) == 10:
            break
    return chosen

selected = pick_non_overlapping(filtered)
used_emojis = set(seed_map.values())
emoji_iter = (e for e in EMOJI_POOL if e not in used_emojis)

dyn_map = {}
for phrase, _count in selected:
    try:
        dyn_map[phrase] = next(emoji_iter)
    except StopIteration:
        break

full_map = {**seed_map, **dyn_map}

def compress(text, d):
    items = sorted(d.items(), key=lambda x: len(x[0]), reverse=True)
    for phrase, emoji in items:
        text = text.replace(phrase, emoji)
    return text

t0 = time.time()
compressed = compress(text, full_map)
t1 = time.time()

orig = len(text.encode("utf-8"))
comp = len(compressed.encode("utf-8"))
saved = orig - compgit init



print("=== NEW PHRASES LEARNED ===")
print(json.dumps(dyn_map, ensure_ascii=False, indent=2))

print("\n=== METRICS (SEED + DYNAMIC) ===")
print(json.dumps({
    "original_bytes": orig,
    "compressed_bytes": comp,
    "saved_bytes": saved,
    "compression_ratio": round(comp/orig, 4),
    "time_ms": round((t1 - t0) * 1000, 2)
}, indent=2))

OUT_DICT_PATH.write_text(json.dumps(full_map, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_COMP_PATH.write_text(compressed, encoding="utf-8")

print(f"\n[OK] Saved full dictionary → {OUT_DICT_PATH.resolve()}")
print(f"[OK] Saved improved compression → {OUT_COMP_PATH.resolve()}")
