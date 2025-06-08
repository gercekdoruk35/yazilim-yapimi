# main.py

import tkinter as tk
from tkinter import messagebox
import veritabani as db
import random
import veritabani as db
db.tablo_olustur()
aktif_kullanici = None

def ekran_degistir(aktif_ekran, yeni_ekran):
    aktif_ekran.destroy()
    yeni_ekran()

def giris_ekrani():
    pencere = tk.Tk()
    pencere.title("Giriş Yap")
    pencere.geometry("400x300")
    pencere.configure(bg="#f0f4f8")

    tk.Label(pencere, text="Kullanıcı Adı", bg="#f0f4f8").pack(pady=5)
    kullanici_giris = tk.Entry(pencere)
    kullanici_giris.pack()

    tk.Label(pencere, text="Şifre", bg="#f0f4f8").pack(pady=5)
    sifre_giris = tk.Entry(pencere, show="*")
    sifre_giris.pack()

    def giris():
        global aktif_kullanici
        kullanici = kullanici_giris.get()
        sifre = sifre_giris.get()
        sonuc = db.kullanici_giris(kullanici, sifre)
        if sonuc:
            aktif_kullanici = sonuc
            pencere.destroy()
            ana_menu()
        else:
            messagebox.showerror("Hata", "Giriş başarısız.")

    def kayit():
        kullanici = kullanici_giris.get()
        sifre = sifre_giris.get()
        if db.kullanici_kayit(kullanici, sifre):
            messagebox.showinfo("Başarılı", "Kayıt tamamlandı.")
        else:
            messagebox.showerror("Hata", "Bu kullanıcı zaten var.")

    tk.Button(pencere, text="Giriş Yap", command=giris, bg="#87ceeb").pack(pady=10)
    tk.Button(pencere, text="Kayıt Ol", command=kayit, bg="#98fb98").pack()
    pencere.mainloop()

def ana_menu():
    pencere = tk.Tk()
    pencere.title("Ana Menü")
    pencere.geometry("400x400")
    pencere.configure(bg="#e6f7ff")

    tk.Label(pencere, text="Kelime Ezberleme Uygulaması", font=("Arial", 16), bg="#e6f7ff").pack(pady=20)

    tk.Button(pencere, text="Bugünkü Sınav", command=lambda: ekran_degistir(pencere, bugunku_sinav), width=25).pack(pady=5)
    tk.Button(pencere, text="İstatistik", command=lambda: ekran_degistir(pencere, istatistik_ekrani), width=25).pack(pady=5)
    tk.Button(pencere, text="Wordle Oyunu", command=lambda: ekran_degistir(pencere, wordle_ekrani), width=25).pack(pady=5)
    tk.Button(pencere, text="Ayarlar", command=lambda: ekran_degistir(pencere, ayar_ekrani), width=25).pack(pady=5)
    tk.Button(pencere, text="Kelime Ekle", command=lambda: ekran_degistir(pencere, kelime_ekle_ekrani), width=25).pack(pady=5)
    pencere.mainloop()

def bugunku_sinav():
    pencere = tk.Tk()
    pencere.title("Bugünkü Sınav")
    pencere.geometry("500x300")
    pencere.configure(bg="#fffaf0")

    kelimeler = db.bugunku_sinav_kelimeleri_getir(aktif_kullanici, db.kullanici_ayarlarini_getir(aktif_kullanici))
    index = 0

    if not kelimeler:
        tk.Label(pencere, text="Bugünkü sınavı tamamladınız!", bg="#fffaf0", font=("Arial", 12)).pack(pady=20)
        tk.Button(pencere, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack(pady=5)
        pencere.mainloop()
        return

    def goster():
        kelime = kelimeler[index]
        for widget in pencere.winfo_children():
            widget.destroy()

        ingilizce = kelime[1]
        turkce = kelime[2]
        ornek = kelime[3]
        bosluklu_cumle = ornek.replace(ingilizce, "_____")

        tk.Label(pencere, text=bosluklu_cumle, wraplength=450, bg="#fffaf0", font=("Arial", 12)).pack(pady=10)
        tk.Label(pencere, text=f"{ingilizce} kelimesinin Türkçesi nedir?", bg="#fffaf0").pack()
        cevap_entry = tk.Entry(pencere)
        cevap_entry.pack()

        def kontrol():
            cevap = cevap_entry.get().strip().lower()
            dogru = turkce.lower()
            db.kelime_durumunu_guncelle(aktif_kullanici, kelime[0], cevap == dogru)
            ileri()

        buton_cerceve = tk.Frame(pencere, bg="#fffaf0")
        buton_cerceve.pack(pady=10)
        tk.Button(buton_cerceve, text="Devam", command=kontrol).pack(side="left", padx=5)
        tk.Button(buton_cerceve, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack(side="left", padx=5)

    def ileri():
        nonlocal index
        index += 1
        if index < len(kelimeler):
            goster()
        else:
            for widget in pencere.winfo_children():
                widget.destroy()
            tk.Label(pencere, text="Sınav tamamlandı!", bg="#fffaf0").pack(pady=10)
            tk.Button(pencere, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack(pady=5)

    goster()
    pencere.mainloop()

def istatistik_ekrani():
    pencere = tk.Tk()
    pencere.title("İstatistik")
    pencere.geometry("500x400")
    pencere.configure(bg="#f0f8ff")

    veriler = db.secilen_kelimelerle_istatistik_getir(aktif_kullanici)

    tk.Label(pencere, text=f"Genel Başarı: %{veriler['Genel Başarı']}", font=("Arial", 14), bg="#f0f8ff").pack(pady=10)

    for detay in veriler["Detaylar"]:
        tk.Label(
            pencere,
            text=f"{detay['ingilizce']} ({detay['turkce']}) - Doğru: {detay['dogru']} Yanlış: {detay['yanlis']}",
            bg="#f0f8ff"
        ).pack()

    tk.Button(pencere, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack(pady=10)
    pencere.mainloop()

def wordle_ekrani():
    pencere = tk.Tk()
    pencere.title("Wordle Oyunu")
    pencere.geometry("400x300")
    pencere.configure(bg="#fff5ee")

    kelimeler = db.wordle_kelime_listesi(aktif_kullanici)
    if not kelimeler:
        tk.Label(pencere, text="Yeterli öğrenilmiş kelime yok.", bg="#fff5ee").pack(pady=20)
        tk.Button(pencere, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack()
        return

    hedef = random.choice(kelimeler).lower()

    def tahmin_kontrol():
        tahmin = giris.get().lower()
        sonuc = ""
        for i in range(len(tahmin)):
            if i < len(hedef) and tahmin[i] == hedef[i]:
                sonuc += tahmin[i].upper()
            elif tahmin[i] in hedef:
                sonuc += tahmin[i]
            else:
                sonuc += "_"
        sonuc_label.config(text=sonuc)
        if tahmin == hedef:
            messagebox.showinfo("Tebrikler", "Doğru tahmin!")
            ekran_degistir(pencere, ana_menu)

    giris = tk.Entry(pencere)
    giris.pack(pady=10)
    sonuc_label = tk.Label(pencere, text="", bg="#fff5ee", font=("Courier", 18))
    sonuc_label.pack(pady=10)
    tk.Button(pencere, text="Kontrol Et", command=tahmin_kontrol).pack()
    tk.Button(pencere, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack(pady=10)
    pencere.mainloop()

def ayar_ekrani():
    pencere = tk.Tk()
    pencere.title("Ayarlar")
    pencere.geometry("300x200")
    pencere.configure(bg="#f5fffa")

    tk.Label(pencere, text="Günlük Hedef Kelime Sayısı", bg="#f5fffa").pack(pady=5)
    hedef_entry = tk.Entry(pencere)
    hedef_entry.insert(0, str(db.kullanici_ayarlarini_getir(aktif_kullanici)))
    hedef_entry.pack()

    def guncelle():
        try:
            yeni = int(hedef_entry.get())
            db.kullanici_ayarlarini_guncelle(aktif_kullanici, yeni)
            messagebox.showinfo("Başarılı", "Ayar güncellendi.")
        except:
            messagebox.showerror("Hata", "Geçerli bir sayı girin.")

    tk.Button(pencere, text="Güncelle", command=guncelle).pack(pady=10)
    tk.Button(pencere, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack()
    pencere.mainloop()

def kelime_ekle_ekrani():
    pencere = tk.Tk()
    pencere.title("Kelime Ekle")
    pencere.geometry("400x300")
    pencere.configure(bg="#f5f5dc")

    tk.Label(pencere, text="İngilizce", bg="#f5f5dc").pack()
    ing = tk.Entry(pencere)
    ing.pack()
    tk.Label(pencere, text="Türkçe", bg="#f5f5dc").pack()
    tr = tk.Entry(pencere)
    tr.pack()
    tk.Label(pencere, text="Örnek Cümle", bg="#f5f5dc").pack()
    ornek = tk.Entry(pencere)
    ornek.pack()

    def ekle():
        db.kelime_ekle(ing.get(), tr.get(), ornek.get())
        messagebox.showinfo("Başarılı", "Kelime eklendi.")
        ing.delete(0, "end")
        tr.delete(0, "end")
        ornek.delete(0, "end")

    tk.Button(pencere, text="Ekle", command=ekle).pack(pady=10)
    tk.Button(pencere, text="Geri", command=lambda: ekran_degistir(pencere, ana_menu)).pack()
    pencere.mainloop()

if __name__ == "__main__":
    db.tablo_olustur()
    giris_ekrani()
