from models import Yemek
from extensions import db

def yemek_ekle(isim, kategori, fiyat, aciklama, kullanici_id):
    yeni_yemek = Yemek(
        isim=isim,
        kategori=kategori,
        fiyat=fiyat,
        aciklama=aciklama,
        kullanici_id=kullanici_id
    )
    db.session.add(yeni_yemek)
    db.session.commit()
    return yeni_yemek

def yemek_getir(yemek_id):
    return Yemek.query.get_or_404(yemek_id)

def yemek_guncelle(yemek, isim=None, kategori=None, fiyat=None, aciklama=None):
    if isim is not None:
        yemek.isim = isim
    if kategori is not None:
        yemek.kategori = kategori
    if fiyat is not None:
        yemek.fiyat = fiyat
    if aciklama is not None:
        yemek.aciklama = aciklama

    db.session.commit()
    return yemek

def yemek_sil(yemek):
    db.session.delete(yemek)
    db.session.commit()
