# GaenCore,
EYC, EYPEL ve Gaen Studio'yu bir araya getiren bir pakettir.

# 🚀 Gaen Studio & EYC Kullanım Kılavuzu

Bu rehber; **Gaen Studio** editörü, **EYC** (JavaScript kolaylaştırıcı) ve **EYPEL** kütüphanesinin kurulumu ile temel komutlarını içermektedir.

---

## 🛠 1. Gaen Studio
EYC ile programlamayı kolaylaştıran ve yerel kaynakları hızlıca kullanmanızı sağlayan özel bir metin editörüdür.

### **Nasıl Hazır Hale Getirilir?**
Gaen Studio'yu başlatmak için iki yönteminiz vardır:
1.  **Kısayol Oluşturma:** Ana dizinde bulunan `Gaen Studio.lnk` dosyasının bir kısayolunu oluşturup kullanabilirsiniz.
2.  **Hızlı Arama:** Windows arama çubuğuna direkt olarak **"Gaen Studio"** yazarak uygulamayı aratıp başlatabilirsiniz.

---

## ⚙️ 2. EYC
EYPEL sistemleri ile JavaScript kullanımını optimize eden bir araçtır. Belirli komutlar aracılığıyla derleme ve yapılandırma işlemlerini yürütür.

### **Kurulum ve PATH Ayarları**
EYC'yi komut satırından her an çağırabilmek için şu adımları izleyin:

1.  **Dosya Yolu:** `source -> EYC -> dist -> eyc` klasör yolunu takip ederek `eyc.exe` dosyasını bulun.
2.  **Yolu Kopyalayın:** Bu klasörün tam adresini (Path) kopyalayın.
3.  **Sistem Ayarları:** Windows arama çubuğuna **"Sistem ortam değişkenlerini düzenleyin"** yazın ve uygulamayı açın.
4.  **Değişken Ekleme:**
    * **"Ortam Değişkenleri"** butonuna tıklayın.
    * Listeden **"Path"** satırını bulup çift tıklayın.
    * **"Yeni"** butonuna basarak kopyaladığınız yolu buraya yapıştırın.
5.  **Tamamla:** Tüm pencereleri "Tamam" diyerek kapatın. Kurulum tamamlandı!



### **Temel Komutlar**

| Komut | İşlev | Notlar |
| :--- | :--- | :--- |
| `eyc -c dosya.eyc` | `.eyc` dosyasını derler. | Çıktı otomatik `.js` olur. Dosya halihazırda varsa mevcut dosyanın üzerine yazar! |
| `eyc built -i derlenmis.js cikis.html` | Minimalist bir `.html` index dosyası oluşturur. İçerisinde EYC'teki "@root" ortamını kurar.

---

## 📦 3. EYPEL Kütüphanesi
Basit, minimal ve küçük kodlardan oluşan; Graphics ve Web gibi temel araçları barındıran bir kütüphane klasörüdür.

### **Nasıl Kurulur?**
Çalıştığınız Python dosyası ile aynı klasöre, ana dizindeki **"EYPEL"** klasörünü kopyalayıp yapıştırmanız yeterlidir.

### **Önemli Modüller**

#### **🔹 Graphic Modülü (`graphic.py`)**
EYC ile oluşturulan `.html` dosyalarını kullanarak ekran açmanıza yarar.
* **İçe Aktarma:** `from EYPEL import graphic`
* **Kullanım:** `graphic.startScreen(başlık, dosya)`

#### **🔹 Web Modülü (`web.py`)**
İstediğiniz URL'den dosya indirmenizi sağlayan, basit setup yazılımları için ideal bir modüldür.
* **İçe Aktarma:** `from EYPEL import web`
* **Kullanım:** `web.download(url, dosya_adi)`
* *Örnek:* Bir `.png` linki verip hedef ismi `.png` yaparsanız, dosyayı otomatik indirip kaydeder.

---

> [!CAUTION]
> **Önemli Not:** `eyc -c` komutu, çıktı klasöründe aynı isimde bir `.js` dosyası bulursa onu kalıcı olarak siler ve yenisini yazar. Veri kaybı yaşamamak için dosya isimlerinize dikkat edin.
