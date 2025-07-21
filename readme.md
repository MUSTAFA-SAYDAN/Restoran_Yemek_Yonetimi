# 🍽️ Yemek Takip Sistemi API

Bu proje, kullanıcıların yemek ekleyip, listeleyebileceği, güncelleyebileceği ve silebileceği basit bir RESTful API'dir.  
Flask, SQLite, SQLAlchemy, JWT ve bcrypt teknolojileri kullanılarak geliştirilmiştir.

---

## ✨ Özellikler

- 👤 Kullanıcı kayıt ve giriş işlemleri (JWT ile kimlik doğrulama)
- 🍛 Yemek CRUD (Oluşturma, Listeleme, Güncelleme, Silme)
- 🔒 Token tabanlı yetkilendirme ile güvenli API erişimi
- 🔐 Şifreler bcrypt ile güvenli şekilde saklanır
- 🧑‍💻 Kullanıcı sadece kendi yemeklerini düzenleyebilir

---

## ⚙️ Kurulum

### 1. Projeyi klonlayın:

```bash
git clone https://github.com/MUSTAFA-SAYDAN/Restoran_Yemek_Yonetimi.git
cd Restoran_Yemek_Yonetimi
2. Sanal ortam oluşturun ve etkinleştirin:
bash
Kopyala
Düzenle
python -m venv venv

# Windows için:
venv\Scripts\activate

# Linux/Mac için:
source venv/bin/activate
3. Gereksinimleri yükleyin:
bash
Kopyala
Düzenle
pip install -r requirements.txt
4. Uygulamayı başlatın:
bash
Kopyala
Düzenle
python app.py
API çalıştığında şu adrese giderek erişebilirsiniz:
📍 http://127.0.0.1:5001

📮 API Endpointleri
👤 Kullanıcı İşlemleri
Yöntem	URL	Açıklama
POST	/kayit	Kullanıcı kaydı
POST	/giris	Giriş yap ve token al

🍱 Yemek İşlemleri
Yöntem	URL	Açıklama
GET	/yemekler	Tüm yemekleri getir
POST	/yemekler	Yeni yemek ekle (token gerekir)
GET	/yemekler/<id>	Belirli yemeği getir
PUT	/yemekler/<id>	Yemeği güncelle (token gerekir)
DELETE	/yemekler/<id>	Yemeği sil (token gerekir)

🔐 Token Kullanımı (Postman için)
POSTMAN veya benzeri araçlarda, JWT token’ı şu şekilde gönder:

Headers kısmına:

makefile
Kopyala
Düzenle
Key: Authorization
Value: Bearer <token_buraya>
📁 Proje Dosya Yapısı
bash
Kopyala
Düzenle
yemek_api/
│
├── app.py               # Ana uygulama dosyası
├── models.py            # Veritabanı modelleri
├── requirements.txt     # Gerekli kütüphaneler
├── .gitignore           # Gereksiz dosyaları dışlar
└── README.md            # Proje açıklaması
👨‍💻 Geliştirici
Mustafa Saydan
Python ve Flask ile backend geliştirme yolculuğunda örnek projelerle ilerliyor.
Bu proje, JWT ve kullanıcı yönetimini içeren tam işlevli bir API örneğidir.

📝 Lisans
Bu proje eğitim ve portföy amaçlıdır. İsteyen herkes kullanabilir, geliştirebilir.