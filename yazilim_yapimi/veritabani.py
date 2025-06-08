import sqlite3
import random
from datetime import datetime

def baglanti():
    return sqlite3.connect("veritabani.db") # aşağıda bahsettiğim şeyi bu satır yapıyor veritabanı oluşturuyor giriş, kayıt, doğru cevap yanlış cevap vb.. 

def tablo_olustur():
    conn = baglanti()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT UNIQUE,
            sifre TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS ayarlar (
            kullanici_id INTEGER PRIMARY KEY,
            gunluk_hedef INTEGER DEFAULT 5
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS kelimeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingilizce TEXT,
            turkce TEXT,
            ornek_cumle TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_word_status (
            kullanici_id INTEGER,
            kelime_id INTEGER,
            dogru INTEGER DEFAULT 0,
            yanlis INTEGER DEFAULT 0,
            son_guncelleme TEXT,
            PRIMARY KEY (kullanici_id, kelime_id)
        )
    ''')

    conn.commit()
    conn.close()

    if not kelime_var_mi():
        kelime_ekle_batch()

def kelime_var_mi():
    conn = baglanti()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM kelimeler")
    sonuc = c.fetchone()[0]
    conn.close()
    return sonuc > 0

def kelime_ekle(ing, tr, ornek):
    conn = baglanti()
    c = conn.cursor()
    c.execute("INSERT INTO kelimeler (ingilizce, turkce, ornek_cumle) VALUES (?, ?, ?)", (ing, tr, ornek))
    conn.commit()
    conn.close()

def kelime_ekle_batch(): 
    kelimeler = [ # aşkım buraya istediğin kelimeyi cümleyi yaz ben direkt bi siteden çektim ama zaten kelime ekle modülünüz var bi de veritabani.db diye bi dosya var onu arada bir sil hata veriyor sonra zaen sen maini her çalıştırdığında veritabanı oluşturuyor oto olarak 
        ("apple", "elma", "I ate an apple yesterday."),
        ("book", "kitap", "She read a book."),
        ("car", "araba", "They bought a new car."),
        ("dog", "köpek", "The dog barked loudly."),
        ("egg", "yumurta", "I had an egg for breakfast."),
        ("fish", "balık", "He caught a fish."),
        ("green", "yeşil", "Green is my favorite color."),
        ("house", "ev", "We live in a big house."),
        ("ice", "buz", "The ice is melting."),
        ("juice", "meyve suyu", "I drank orange juice."),
        ("key", "anahtar", "She lost her key."),
        ("lemon", "limon", "The tea has lemon in it."),
        ("moon", "ay", "The moon is bright tonight."),
        ("nose", "burun", "His nose is red."),
        ("orange", "portakal", "Do you want an orange?"),
        ("pen", "kalem", "Give me a pen."),
        ("queen", "kraliçe", "The queen arrived."),
        ("rain", "yağmur", "It will rain tomorrow."),
        ("sun", "güneş", "The sun is hot."),
        ("tree", "ağaç", "There is a tree in the garden."),
        ("umbrella", "şemsiye", "Take your umbrella."),
        ("violin", "keman", "She plays the violin."),
        ("window", "pencere", "Open the window."),
        ("xylophone", "ksilofon", "He plays the xylophone."),
        ("yogurt", "yoğurt", "Do you like yogurt?"),
        ("zebra", "zebra", "A zebra has black and white stripes."),
        ("ball", "top", "He kicked the ball."),
        ("chair", "sandalye", "Sit on the chair."),
        ("desk", "masa", "This is my desk."),
        ("elephant", "fil", "An elephant is huge."),
        ("flower", "çiçek", "She picked a flower."),
        ("glass", "bardak", "I need a glass of water."),
        ("hat", "şapka", "This hat is new."),
        ("island", "ada", "We visited the island."),
        ("jacket", "ceket", "Wear your jacket."),
        ("kite", "uçurtma", "The kite is flying."),
        ("lion", "aslan", "A lion is strong."),
        ("milk", "süt", "He drinks milk."),
        ("notebook", "defter", "I wrote in my notebook."),
        ("ocean", "okyanus", "The ocean is vast."),
        ("pizza", "pizza", "Let’s eat pizza."),
        ("queen", "kraliçe", "The queen waved."),
        ("rabbit", "tavşan", "The rabbit ran."),
        ("star", "yıldız", "Look at the star."),
        ("turtle", "kaplumbağa", "The turtle moves slowly."),
        ("uniform", "üniforma", "He wore a uniform."),
        ("vase", "vazo", "The vase broke."),
        ("watch", "saat", "This watch is old."),
        ("x-ray", "röntgen", "I had an x-ray."),
        ("yarn", "iplik", "She knits with yarn."),
        ("zoo", "hayvanat bahçesi", "We went to the zoo.")
    ]

    for ing, tr, ornek in kelimeler:
        kelime_ekle(ing, tr, ornek)

def kullanici_kayit(kullanici, sifre):
    conn = baglanti()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (kullanici, sifre))
        conn.commit()
        kullanici_id = c.lastrowid
        c.execute("INSERT INTO ayarlar (kullanici_id) VALUES (?)", (kullanici_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def kullanici_giris(kullanici, sifre):
    conn = baglanti()
    c = conn.cursor()
    c.execute("SELECT id FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici, sifre))
    sonuc = c.fetchone()
    conn.close()
    return sonuc[0] if sonuc else None

def kullanici_ayarlarini_getir(kullanici_id):
    conn = baglanti()
    c = conn.cursor()
    c.execute("SELECT gunluk_hedef FROM ayarlar WHERE kullanici_id=?", (kullanici_id,))
    sonuc = c.fetchone()
    conn.close()
    return sonuc[0] if sonuc else 5

def kullanici_ayarlarini_guncelle(kullanici_id, hedef):
    conn = baglanti()
    c = conn.cursor()
    c.execute("UPDATE ayarlar SET gunluk_hedef=? WHERE kullanici_id=?", (hedef, kullanici_id))
    conn.commit()
    conn.close()

def bugunku_sinav_kelimeleri_getir(kullanici_id, hedef):
    conn = baglanti()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM kelimeler WHERE id NOT IN (
            SELECT kelime_id FROM user_word_status WHERE kullanici_id=?
        ) LIMIT ?
    ''', (kullanici_id, hedef))
    kelimeler = c.fetchall()

    for kelime in kelimeler:
        c.execute("INSERT OR IGNORE INTO user_word_status (kullanici_id, kelime_id, son_guncelleme) VALUES (?, ?, ?)", (kullanici_id, kelime[0], datetime.now().date()))

    conn.commit()
    conn.close()
    return kelimeler

def kelime_durumunu_guncelle(kullanici_id, kelime_id, dogru_mu):
    conn = baglanti()
    c = conn.cursor()
    if dogru_mu:
        c.execute("UPDATE user_word_status SET dogru = dogru + 1, son_guncelleme=? WHERE kullanici_id=? AND kelime_id=?", (datetime.now().date(), kullanici_id, kelime_id))
    else:
        c.execute("UPDATE user_word_status SET yanlis = yanlis + 1, son_guncelleme=? WHERE kullanici_id=? AND kelime_id=?", (datetime.now().date(), kullanici_id, kelime_id))
    conn.commit()
    conn.close()

def secilen_kelimelerle_istatistik_getir(kullanici_id):
    conn = baglanti()
    c = conn.cursor()
    c.execute('''
        SELECT k.ingilizce, k.turkce, u.dogru, u.yanlis FROM kelimeler k
        JOIN user_word_status u ON k.id = u.kelime_id
        WHERE u.kullanici_id=?
    ''', (kullanici_id,))
    rows = c.fetchall()
    conn.close()

    detaylar = []
    toplam_dogru = 0
    toplam_soru = 0
    for ing, tr, d, y in rows:
        detaylar.append({"ingilizce": ing, "turkce": tr, "dogru": d, "yanlis": y})
        toplam_dogru += d
        toplam_soru += d + y

    oran = round((toplam_dogru / toplam_soru) * 100, 2) if toplam_soru else 0
    return {"Genel Başarı": oran, "Detaylar": detaylar}

def wordle_kelime_listesi(kullanici_id):
    conn = baglanti()
    c = conn.cursor()
    c.execute('''
        SELECT k.ingilizce FROM kelimeler k
        JOIN user_word_status u ON k.id = u.kelime_id
        WHERE u.kullanici_id=? AND u.dogru >= 1
    ''', (kullanici_id,))
    sonuc = [row[0] for row in c.fetchall()]
    conn.close()
    return sonuc
