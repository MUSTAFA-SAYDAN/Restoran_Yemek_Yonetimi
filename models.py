from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db=SQLAlchemy()
bcrypt=Bcrypt()


class Kullanici(db.Model):
    __tablename__="kullanicilar"
    id=db.Column(db.Integer,primary_key=True)
    kullanici_adi=db.Column(db.String(100),unique=True,nullable=False)
    sifre_hash=db.Column(db.String(100),nullable=False)

    def sifre_kontrol(self,sifre):
        return bcrypt.check_password_hash(self.sifre_hash,sifre)
    

class Yemek(db.Model):
    __tablename__="yemekler"

    id=db.Column(db.Integer,primary_key=True)
    isim=db.Column(db.String(100),nullable=False)
    kategori=db.Column(db.String(100),nullable=False)
    fiyat=db.Column(db.Integer,nullable=False)
    aciklama=db.Column(db.String(100),nullable=False)
    kullanici_id=db.Column(db.Integer,db.ForeignKey("kullanicilar.id"),nullable=False)


    def to_dict(self):
        return{
            "id":self.id,
            "isim":self.isim,
            "kategori":self.kategori,
            "fiyat":self.fiyat,
            "aciklama":self.aciklama,
            "kullanici_id":self.kullanici_id
        }
 