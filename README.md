# Türkçe metinlerden duygu analizi ile bilgisayar destekli müzik üretme

Projede girilen cümle öncelikle **google_trans_new** kütüphanesiyle ingilizceye çevirilir çünü duygu analizini yapmak için **nltk** kütüphanesi kullanılır ki bu kütüphanede ingilizce dili ile çalışmaktadır.

Ve nltk kütüphanesinden gelen **Pozitif Nötr Negatif** sonucuna göre müzik üretilir.


## Prerequisites
Python 3.7 ve üzeri bilgisayarınızda kurulu olması gerekir eğer kurulu değilse [Python Kurulum](https://www.python.org) tıklayarak kurulumu yapabilirsiniz.


## İnstaling

**PyQt5**
```
pip install pyqt5
```

**Google_trans_new**
```
pip install google_trans_new
```

**Nltk**
```
pip install nltk
```

**Pyknon**
```
pip install pyknon
```

**Pygame**
```
pip install pygame
```

## Run
```
python main.py
```

## Suggestions

Projede belirlenen akorlar, notalar, duraklama süreleri belirli bir düzene göre verilmiştir.

Yapay zeka teknolojisi ile akorlar , notalar, duraklama süreleri ünlü bestecilerin bestelerinden faydalınarak belirlenebilir.

Ancak belirlenicek akor,nota ve duraklama süreleri girilen cümlenin alanına göre olşturrulmalıdır yani  girilen cümle pozitifse neşeli, oynak ve hareketli bestecilerin
müzikleri dinletilerek model eğitilmelidir

## Thanks

* **Turgay Tugay Bilgin**
