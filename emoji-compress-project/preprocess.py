import pandas as pd
import re
from pathlib import Path

CSV_PATH = Path("conversations_ec_support.csv")
RAW_OUT  = Path("chat_raw.txt")
PRE_OUT  = Path("chat_preprocessed.txt")

df = pd.read_csv(CSV_PATH)

messages = df["message"].fillna("").astype(str)

raw_text = "\n".join(messages)
RAW_OUT.write_text(raw_text, encoding="utf-8")
print(f"[OK] Saved raw chat to: {RAW_OUT.resolve()}")

def clean_line(line: str) -> str:
    l = line.strip()
    l = re.sub(r"^[A-Za-z]+:\s*", "", l)
    l = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", l)
    l = l.replace("…", " ")
    l = re.sub(r"\s{2,}", " ", l)

    return l.strip()

def privacy_mask(text: str) -> str:
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "🔒EMAIL", text)
    text = re.sub(r"(?:\+?\d[\s\-()]*){8,}", "🔒PHONE", text)
    return text

cleaned_lines = [clean_line(l) for l in messages]
cleaned_lines = [l for l in cleaned_lines if l and l.lower() not in ["nan", "null"]]

pre_text = privacy_mask("\n".join(cleaned_lines))

PRE_OUT.write_text(pre_text, encoding="utf-8")
print(f"[OK] Saved preprocessed chat to: {PRE_OUT.resolve()}")
print("\nPreview:\n", pre_text[:400])
