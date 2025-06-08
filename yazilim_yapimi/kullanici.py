import sqlite3
from veritabani import veritabani_baglan

def kayit_ol(username, password):
    try:
        conn = veritabani_baglan()
        c = conn.cursor()

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        user_id = c.lastrowid
        c.execute("INSERT INTO user_settings (user_id, daily_word_limit) VALUES (?, ?)", (user_id, 10))

        # Varsayılan kelimeleri ekle (isteğe bağlı)
        c.execute("SELECT id FROM words")
        word_ids = c.fetchall()

        
        for (word_id,) in word_ids:
            c.execute("INSERT OR IGNORE INTO user_word_status (user_id, word_id) VALUES (?, ?)", (user_id, word_id))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def giris_yap(username, password):
    conn = veritabani_baglan()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    sonuc = c.fetchone()
    conn.close()
    return sonuc is not None
