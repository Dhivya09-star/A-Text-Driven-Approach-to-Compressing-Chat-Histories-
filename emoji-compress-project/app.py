import streamlit as st
import json
from pathlib import Path

DICT_PATH = Path("full_dictionary.json")

if not DICT_PATH.exists():
    st.error("⚠️ full_dictionary.json not found. Please run dynamic_dictionary.py first.")
    st.stop()

full_dict = json.loads(DICT_PATH.read_text(encoding="utf-8"))
reverse_dict = {v: k for k, v in full_dict.items()}

def compress_text(text):
    out = text
    for phrase, emoji in sorted(full_dict.items(), key=lambda x: len(x[0]), reverse=True):
        out = out.replace(phrase, emoji)
    return out

def decompress_text(text):
    out = text
    for emoji, phrase in reverse_dict.items():
        out = out.replace(emoji, phrase)
    return out

def compute_metrics(original, compressed):
    orig = len(original.encode("utf-8"))
    comp = len(compressed.encode("utf-8"))
    saved = orig - comp
    ratio = comp / orig if orig else 1
    return orig, comp, saved, ratio


st.title("✨ Emoji-Based Text Compression App")
st.write("Compress conversational text using learned emoji dictionary.")

tab1, tab2 = st.tabs(["🔻 Compress Text", "🔺 Decompress Text"])

with tab1:
    st.subheader("Enter Text to Compress:")
    input_text = st.text_area("Input Text", height=200, placeholder="Paste chat/message text here...")

    if st.button("Compress"):
        if input_text.strip() == "":
            st.warning("Please enter some text.")
        else:
            compressed = compress_text(input_text)
            orig, comp, saved, ratio = compute_metrics(input_text, compressed)

            st.success("✅ Compression Completed")
            st.write(f"**Original Size:** {orig} bytes")
            st.write(f"**Compressed Size:** {comp} bytes")
            st.write(f"**Saved:** {saved} bytes")
            st.write(f"**Compression Ratio:** {ratio:.3f}")

            st.text_area("Compressed Output:", value=compressed, height=200)

with tab2:
    st.subheader("Enter Text to Decompress:")
    compressed_text = st.text_area("Compressed Text", height=200, placeholder="Paste compressed text with emojis...")

    if st.button("Decompress"):
        if compressed_text.strip() == "":
            st.warning("Please enter compressed text.")
        else:
            decompressed = decompress_text(compressed_text)
            st.success("✅ Successfully Returned to Original Text")
            st.text_area("Decompressed Output:", value=decompressed, height=200)
