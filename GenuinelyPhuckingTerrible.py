import sqlite3, random, time, sys, time, os, random, string, re, sys

DB_PATH = r"C:\Users\hhfis\Documents\VSCode\GeniusBot3000\wiki.db"
TXT_PATH = r"C:\Users\hhfis\Documents\VSCode\GeniusBot3000\wiki_sentences.txt"

def sprint(*args, delay=0.02):
    text = " ".join(map(str, args))
    burst = 0
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()

        # --- base delay ---
        if c in ".!?":
            delay = random.uniform(0.18, 0.28)
        elif c in ",;:":
            delay = random.uniform(0.07, 0.12)
        elif c in " ":
            delay = random.uniform(0.05, 0.15)
        else:
            delay = random.uniform(0.015, 0.045)

        if burst > 0:
            delay *= random.uniform(0.7, 0.9)   
            burst -= 1
        elif random.random() < 0.5:            
            burst = random.randint(6, 20)       

        delay *= random.uniform(0.9, 1.1)

        time.sleep(delay)
    print()

# make db
if not os.path.exists(DB_PATH):
    sprint("Training advanced AI model... beep.... boop.... beep.")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE VIRTUAL TABLE wiki USING fts5(sentence);")
    with open(TXT_PATH, encoding="utf8") as f:
        for line in f:
            c.execute("INSERT INTO wiki(sentence) VALUES (?);", (line.strip(),))
    conn.commit()
    conn.close()
    print("Database ready:", DB_PATH)

def wrong_answer(question):
    # print("Input after regex:", question)  # Debug print
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = lambda cur, row: row[0]
    c = conn.cursor()
    try:
        qand = " AND ".join(question.lower().split())
        #print("Trying AND query:", q)  # Debug print
        rows = c.execute("SELECT sentence FROM wiki WHERE sentence MATCH ? LIMIT 100;", (qand,)).fetchall()
        # print("AND query matches found:", len(rows))  # Debug print
        
        # If AND finds nothing, try OR
        if len(rows) == 0:
            qor = " OR ".join(question.lower().split())
           # print("Falling back to OR query:", q)  # Debug print
            rows = c.execute("SELECT sentence FROM wiki WHERE sentence MATCH ? LIMIT 100;", (qor,)).fetchall()
           # print("OR query matches found:", len(rows))  # Debug print
    except sqlite3.OperationalError as e:
        # print("SQLite error:", str(e))  # Debug print

        conn.close()
    random.seed(hash(question) + int(time.time())) 
    if rows:
        return random.choice(rows)
    else:
        return "Not even god himself knows the answer, and I checked with him."


if __name__ == "__main__":
    print("Hi I'm ChatGPT (Genuinely Phucking Terrible) ask me anything!")
    while True:
        qb = input("❓ > ")
        q = re.sub(r'[^a-zA-Z0-9\s]', '', qb)
        qand = q
        qor = q
        if not q: 
            sprint("Goodbye! Beep Boop")
            break
        sprint("Beep Boop: ", wrong_answer(q))