import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import heapq

#her bir dugumu temsil edecek
class HuffmanDugumu:
    def __init__(self, frekans, icerik):
        self.frekans = frekans
        self.icerik = icerik

    #2 dugumu kıyasalama yaparken kullanilacak
    def __lt__(self, diger):
        return self.frekans < diger.frekans  #kucuk olanı ilk alıyor

class AlgoritmaSimulasyonu:
    def __init__(self, root):
        self.root = root
        self.root.title("LZW ve HUFFMAN GÖRSELLEŞTİRME")
        self.root.geometry("1300x850")

        self.style = ttk.Style()
        self.style.theme_use("clam") #tema seçimi
        self.bg_color = "#f3f4f6" #tema rengi
        self.root.configure(bg=self.bg_color)

        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)
        self.style.configure("TNotebook", background=self.bg_color)

        giris_paneli = ttk.Frame(self.root)
        giris_paneli.pack(pady=20, fill="x", padx=20)
        ttk.Label(giris_paneli, text="Sıkıştırılmak istenen metin:", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT,padx=5)

        self.metin_giris = ttk.Entry(giris_paneli, width=50, font=("Segoe UI", 11))
        self.metin_giris.pack(side=tk.LEFT, padx=5, ipady=3)

        self.sifirla_degiskenler()

        self.notebook = ttk.Notebook(self.root) #sekmeler arası geçiş için notebook kullanılldı
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.lzw_cerceve = ttk.Frame(self.notebook)
        self.huffman_cerceve = ttk.Frame(self.notebook)

        self.notebook.add(self.lzw_cerceve, text=" LZW Algoritması ")
        self.notebook.add(self.huffman_cerceve, text=" Huffman Algoritması ")

        self.notebook.bind("<<NotebookTabChanged>>", self.sekme_degisti_olayi) #sekmeyi değiştirince sekmenin temizlenmesi için
        self.lzw_arayuzunu_hazirla()
        self.huffman_arayuzunu_hazirla()

    #sekmeyi değiştirdiğimizde mevcuttaki ekranı sıfırlamak için
    def sifirla_degiskenler(self):
        self.metin = ""
        self.p = "" #oncekinin tempi
        self.metin_indis = 0 #metin üzerindeki indeks
        self.adim_sayisi = 1
        self.indis = 1 #sozluk index
        self.sozluk = {} #lzw sozlugu
        self.frekanslar = {} #huffman icin frekans sozlugu
        self.dugumler = [] #dugumlerin oldugu liste buraya sıralanmş eklencekler
        self.huffman_kodlari = {} #karakter kodları yazılacak

    def sekme_degisti_olayi(self, event): #tabloları,değişkenleri temzileyecek sekme değiştirildiğinde
        self.metin_giris.delete(0, tk.END) #metin giriş yapılan kutucuğu temizler
        self.sifirla_degiskenler()
        for i in self.lzw_tablo_widget.get_children():
            self.lzw_tablo_widget.delete(i)
        for i in self.huffman_tablo.get_children():
            self.huffman_tablo.delete(i)
        for i in self.kod_tablo.get_children():
            self.kod_tablo.delete(i)
        if self.canvas is not None:
            self.canvas.delete("all")

    def lzw_arayuzunu_hazirla(self):
        ust_panel = ttk.Frame(self.lzw_cerceve)
        ust_panel.pack(pady=15)
        self.btn_adim = ttk.Button(ust_panel, text="Sonraki Adım", command=self.lzw)
        self.btn_adim.pack(side=tk.LEFT, padx=5)

        sutunlar = ("step", "input", "temp_char", "in_dict", "temp", "add_dict", "output")
        self.lzw_tablo_widget = ttk.Treeview(self.lzw_cerceve, columns=sutunlar, show="headings", height=20)
        tablo_basliklari = {"step": "Step", "input": "Input", "temp_char": "temp_char", "in_dict": "In_dict",
                            "temp": "Temp", "add_dict": "Add_dict", "output": "Output"}
        for s_id, b_metin in tablo_basliklari.items():
            self.lzw_tablo_widget.heading(s_id, text=b_metin)
            self.lzw_tablo_widget.column(s_id, width=110, anchor="center")
        self.lzw_tablo_widget.pack(pady=10, padx=20, fill="both", expand=True)

    def lzw(self):
        if self.metin == "":
            self.metin = self.metin_giris.get() #kutucuktaki metini alıyoruz
            if not self.metin:
                messagebox.showwarning("Uyarı", "Lütfen bir metin giriniz.")
                return
            benzersiz_karakterler = sorted(list(set(self.metin))) #ilk olarak metindeki karakterleri alıyor tek tek
            self.sozluk = {}
            for i,char in enumerate(benzersiz_karakterler):
                self.sozluk[char] = i+1  #her karaktere indeks veriyoruz
            self.indis = len(self.sozluk) + 1
            self.metin_indis = 0
            self.adim_sayisi = 1
            self.p = ""

        if self.metin_indis < len(self.metin):
            c = self.metin[self.metin_indis] #input
            pc = self.p + c #self.p : öncekinin tempi, temp_char

            if pc in self.sozluk: #temp_char durumunun sozlukte olması
                self.lzw_tablo_widget.insert("", "end", values=(self.adim_sayisi,c,pc,"Evet",pc,"-" ,"-"))
                self.p = pc #tempe temp_charı atıyrouz
            else:
                cikti_degeri = self.sozluk[self.p]
                eklenen_bilgi = f"{pc}({self.indis})" #sozluge ekleme işlemi yapıyrouz

                self.lzw_tablo_widget.insert("", "end", values=( self.adim_sayisi, c,pc,"Hayır",c, eklenen_bilgi,self.p))
                self.sozluk[pc] = self.indis
                self.indis += 1
                self.p = c

            self.lzw_tablo_widget.see(self.lzw_tablo_widget.get_children()[-1])
            self.metin_indis += 1
            self.adim_sayisi += 1

        elif self.p != "":
            # Metin bittiğinde kalan son karakterin (p) kodunu yazdır
            son_cikti = self.sozluk[self.p]
            self.lzw_tablo_widget.insert("", "end", values=(
                self.adim_sayisi, "BİTTİ", "-", "-", "-","-",self.p
            ))
            self.p = ""
            messagebox.showinfo("LZW", "Sıkıştırma Tamamlandı")
    def huffman_arayuzunu_hazirla(self):
        ana_huffman = ttk.Frame(self.huffman_cerceve)
        ana_huffman.pack(fill="both", expand=True)
        sol_panel = ttk.Frame(ana_huffman)
        sol_panel.pack(side=tk.LEFT, fill="y", padx=15, pady=10)

        self.btn_huffman_adim = ttk.Button(sol_panel, text="Ağaç Adımı / Oluştur", command=self.huffman)
        self.btn_huffman_adim.pack(pady=10, fill="x")

        ttk.Label(sol_panel, text="Karakter Frekansları", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.huffman_tablo = ttk.Treeview(sol_panel, columns=("karakter", "frekans"), show="headings", height=10)
        self.huffman_tablo.heading("karakter", text="Karakter")
        self.huffman_tablo.heading("frekans", text="Frekans")
        self.huffman_tablo.column("karakter", width=80, anchor="center")
        self.huffman_tablo.column("frekans", width=60, anchor="center")
        self.huffman_tablo.pack(pady=5, fill="x")

        ttk.Label(sol_panel, text="Karakter Kodları", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(15, 0))
        self.kod_tablo_frame = ttk.Frame(sol_panel)
        self.kod_tablo_frame.pack(pady=5, fill="both", expand=True)
        self.kod_tablo = ttk.Treeview(self.kod_tablo_frame, columns=("karakter", "kod"), show="headings", height=15)
        self.kod_tablo.heading("karakter", text="Karakter")
        self.kod_tablo.heading("kod", text="Kod")
        self.kod_tablo.column("karakter", width=80, anchor="center")
        self.kod_tablo.column("kod", width=140, anchor="center")
        self.kod_tablo.pack(side=tk.LEFT, fill="both", expand=True)

        self.canvas_cerceve = ttk.LabelFrame(ana_huffman, text=" Huffman Ağaç Görselleştirme ")
        self.canvas_cerceve.pack(side=tk.RIGHT, expand=True, fill="both", padx=10, pady=10)
        self.canvas = tk.Canvas(self.canvas_cerceve, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=5, pady=5)

    def huffman(self):
        if not self.dugumler:
            metin = self.metin_giris.get()
            if not metin:
                messagebox.showwarning("Uyarı", "Metin Girişi Yapınız")
                return

            self.frekanslar = {}
            for char in metin:
                self.frekanslar[char] = self.frekanslar.get(char, 0) + 1

            for i in self.huffman_tablo.get_children():
                self.huffman_tablo.delete(i)
            for i in self.kod_tablo.get_children():
                self.kod_tablo.delete(i)

            frekans_listesi = self.frekanslar.items()
            sirali_frekanslar = sorted(frekans_listesi, key=lambda x: x[1])

            for char, frek in sirali_frekanslar:
                if char == " ":
                    gorunur = "Boşluk"
                else:
                    gorunur = repr(char)
                self.huffman_tablo.insert("", "end", values=(gorunur, frek))
                yeni_dugum = HuffmanDugumu(frek, char)
                heapq.heappush(self.dugumler, yeni_dugum)
            self.huffman_agaci_ciz()
            return

        if len(self.dugumler) > 1:
            sol = heapq.heappop(self.dugumler)
            sag = heapq.heappop(self.dugumler)

            yeni_dugum = HuffmanDugumu(sol.frekans + sag.frekans, [sol, sag])
            heapq.heappush(self.dugumler, yeni_dugum)

            self.huffman_agaci_ciz()

            if len(self.dugumler) == 1:
                self.huffman_kodlari = {}
                self.kodlari_olustur(self.dugumler[0], "")
                self.kod_tablosunu_doldur()
        else:
            messagebox.showinfo("Bilgi", "Huffman Ağacı Tamamlandı!")

    def kodlari_olustur(self, dugum, mevcut_kod):
        if not isinstance(dugum.icerik, list):
            if mevcut_kod:
                final_kod = mevcut_kod
            else:
                final_kod = "0"
            self.huffman_kodlari[dugum.icerik] = final_kod
            return

        self.kodlari_olustur(dugum.icerik[0], mevcut_kod + "0")
        self.kodlari_olustur(dugum.icerik[1], mevcut_kod + "1")

    def kod_tablosunu_doldur(self):
        for i in self.kod_tablo.get_children(): #tablodaki tüm satırlar
            self.kod_tablo.delete(i)
        sirali_karakterler = sorted(self.huffman_kodlari.keys()) #karakterleri sıralama
        for char in sirali_karakterler:
            if char == " ":
                gorunur = "Boşluk"
            else:
                gorunur = f"'{char}'"
            kod_degeri = self.huffman_kodlari[char] #sozlukten gelen huffman kodu
            self.kod_tablo.insert("","end",values=(gorunur,kod_degeri))

    def ekran_genislik(self, node):
        if not isinstance(node.icerik, list):
            return 1
        return self.ekran_genislik(node.icerik[0]) + self.ekran_genislik(node.icerik[1])

    def huffman_agaci_ciz(self):
        self.canvas.delete("all")
        if not self.dugumler:
            return
        self.canvas.update()
        sirali_dugumler = sorted(self.dugumler)
        W = self.canvas.winfo_width()
        bolge_w = W / len(sirali_dugumler)
        for i, dugum in enumerate(sirali_dugumler):
            x0 = i * bolge_w
            x1 = (i + 1) * bolge_w
            self.dugum_ciz_dinamik(dugum, x0, x1, 50, 80)

    def dugum_ciz_dinamik(self, node, x_start, x_end, y, dy):
        x_mid = (x_start + x_end) / 2
        self.canvas.create_oval(x_mid - 18, y - 18, x_mid + 18, y + 18, fill="#3b82f6", outline="#1d4ed8", width=2)
        self.canvas.create_text(x_mid, y, text=str(node.frekans), fill="white", font=("Segoe UI", 10, "bold"))

        if isinstance(node.icerik, list): #içerik listeyse
            sol_alt, sag_alt = node.icerik[0], node.icerik[1]
            sol_yaprak, sag_yaprak = self.ekran_genislik(sol_alt), self.ekran_genislik(sag_alt)
            oran = sol_yaprak / (sol_yaprak + sag_yaprak)
            ayrac = x_start + (x_end - x_start) * oran

            sol_x_mid = (x_start + ayrac) / 2
            self.canvas.create_line(x_mid, y + 18, sol_x_mid, y + dy - 18, fill="#9ca3af", width=2)
            self.canvas.create_text((x_mid + sol_x_mid) / 2 - 12, (y + y + dy) / 2, text="0", fill="#dc2626")
            self.dugum_ciz_dinamik(sol_alt, x_start, ayrac, y + dy, dy)

            sag_x_mid = (ayrac + x_end) / 2
            self.canvas.create_line(x_mid, y + 18, sag_x_mid, y + dy - 18, fill="#9ca3af", width=2)
            self.canvas.create_text((x_mid + sag_x_mid) / 2 + 12, (y + y + dy) / 2, text="1", fill="#059669")
            self.dugum_ciz_dinamik(sag_alt, ayrac, x_end, y + dy, dy)
        else:
            if node.icerik == " ":
                metin = "Bosluk"
            else:
                metin = f"'{node.icerik}'"
            self.canvas.create_text(x_mid, y + 35, text=metin, fill="#111827", font=("Segoe UI", 11, "bold"))

if __name__ == '__main__':
    pencere = tk.Tk()
    uygulama = AlgoritmaSimulasyonu(pencere)
    pencere.mainloop()
