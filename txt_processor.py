import bz2, re, os
from xml.etree import ElementTree as ET

DUMP_PATH = r"C:\Users\hhfis\Documents\VSCode\GeniusBot3000\simplewiki-latest-pages-articles-multistream.xml.bz2"
OUT_PATH  = r"C:\Users\hhfis\Documents\VSCode\GeniusBot3000\wiki_sentences.txt"

print("Reading:", DUMP_PATH)
with bz2.open(DUMP_PATH, "rt", encoding="utf8", errors="ignore") as f, \
     open(OUT_PATH, "w", encoding="utf8") as out:
    text = ""
    for line in f:
        text += line
        if "</page>" in line:
            try:
                root = ET.fromstring(text)
                body = root.find(".//text")
                if body is not None and body.text:
                    cleaned = re.sub(r"[\[\]\{\}\|=]+", " ", body.text)
                    for sentence in re.split(r"[.!?]", cleaned):
                        sentence = sentence.strip()
                        if len(sentence.split()) > 6:
                            out.write(sentence + "\n")
            except Exception:
                pass
            text = ""
print("Wrote:", OUT_PATH)
