LZW ve Huffman Görselleştirme

Python (Tkinter) ile geliştirilmiş, LZW ve Huffman sıkıştırma algoritmalarını adım adım görselleştiren eğitim amaçlı bir masaüstü uygulaması. Kullanıcının girdiği bir metin üzerinden, algoritmaların her adımda ürettiği ara değerleri tablo halinde ve Huffman ağacını canvas üzerinde çizerek gösterir.
Özellikler
LZW Algoritması
Girilen metindeki benzersiz karakterlerin sözlüğe atanması
"Sonraki Adım" butonuyla algoritmanın adım adım ilerletilmesi
Her adımda Input, Temp_char, In_dict, Temp, Add_dict, Output değerlerinin tablo halinde gösterilmesi
Sıkıştırma tamamlandığında bilgi mesajı
<img width="1622" height="616" alt="image" src="https://github.com/user-attachments/assets/d021fb30-623e-435f-a5c7-fdecbb384bfd" />

Huffman Algoritması
Metindeki karakter frekanslarının hesaplanıp listelenmesi
Min-heap (heapq) kullanılarak düğümlerin birleştirilmesi
Huffman ağacının canvas üzerinde dinamik olarak çizilmesi (dallara 0/1 etiketleri ile)
Oluşan karakter kodlarının tablo halinde gösterilmesi
<img width="1617" height="936" alt="image" src="https://github.com/user-attachments/assets/730624c3-1e5d-4567-aeee-f311000833ae" />

Genel
Sekmeler arasında (LZW ↔ Huffman) geçiş yapıldığında ekranın otomatik sıfırlanması
Kullanılan teknolojiler
Python 3
Tkinter / ttk (arayüz ve sekme yönetimi)
heapq (öncelik kuyruğu ile Huffman ağacı kurulumu)
Canvas (Huffman ağacının çizimi)

