from flask import Flask,request,jsonify
from models import db,bcrypt,Kullanici,Yemek
from functools import wraps
import jwt
import datetime

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///yemekler.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="gizli_anahtar"

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

def token_gerekli(f):
    @wraps(f)
    def sarici(*args,**kwargs):
        token=request.headers.get("Authorization")
        if not token:
            return jsonify({"hata":"Token gerekli"}),401
        try:
            token=token.replace("Bearer ","")
            data=jwt.decode(token,app.config["SECRET_KEY"],algorithms="HS256")
            kullanici_id=data["kullanici_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"hata":"Tokenin süresi bitmiş"}),401
        except jwt.InvalidTokenError:
            return jsonify({"hata":"Geçersiz token"}),401
        
        return f(kullanici_id,*args,**kwargs)
    return sarici

@app.route("/kayit",methods=["POST"])
def kayit():
    data=request.json
    kullanici_adi=data.get("kullanici_adi")
    sifre=data.get("sifre")

    if Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first():
        return jsonify({"hata":"Bu kullanici adi zaten alinmis"}),400
    
    sifre_hash=bcrypt.generate_password_hash(sifre).decode("utf-8")
    yeni_kisi=Kullanici(kullanici_adi=kullanici_adi,sifre_hash=sifre_hash)
    db.session.add(yeni_kisi)
    db.session.commit()

    return jsonify({"mesaj":"Kayit basarili"}),201

@app.route("/giris",methods=["POST"])
def giris():
    data=request.json
    kullanici_adi=data.get("kullanici_adi")
    sifre=data.get("sifre")

    kullanici=Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
    if not kullanici or not kullanici.sifre_kontrol(sifre):
        return jsonify({"hata":"Kullanici adi veya sifre geçersiz"}),401
    
    token=jwt.encode(
        {
            "kullanici_id":kullanici.id,
            "exp":datetime.datetime.utcnow() +datetime.timedelta(hours=3)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token":token})


@app.route("/yemekler",methods=["POST"])
@token_gerekli
def yemek_ekle(kullanici_id):
    data=request.json
    isim=data.get("isim")
    kategori=data.get("kategori")
    fiyat=data.get("fiyat")
    aciklama=data.get("aciklama")

    if not isim or not kategori or not fiyat or not aciklama:
        return jsonify({"hata":"Eksik bilgi var"}),400
    
    yeni_yemek=Yemek(isim=isim,kategori=kategori,fiyat=fiyat,aciklama=aciklama,kullanici_id=kullanici_id)
    db.session.add(yeni_yemek)
    db.session.commit()

    return jsonify({"mesaj":"Yemek eklendi"}),201

@app.route("/yemekler",methods=["GET"])
def yemekleri_getir():
    yemekler=Yemek.query.all()
    return jsonify([k.to_dict() for k in yemekler])

@app.route("/yemekler/<int:id>",methods=["GET"])
def yemegi_getir(id):
    yemek=Yemek.query.get(id)
    if not yemek:
        return jsonify({"hata":"yemek bulunamadi"}),404
    return jsonify(yemek.to_dict())

@app.route("/yemekler/<int:id>",methods=["PUT"])
@token_gerekli
def yemegi_guncelle(id,kullanici_id):
    yemek=Yemek.query.filter_by(id=id,kullanici_id=kullanici_id).first()
    if not yemek:
        return jsonify({"hata":"Yemek bulunamadi"}),404
    
    data=request.json
    yemek.isim=data.get("isim",yemek.isim)
    yemek.kategori=data.get("kategori",yemek.kategori)
    yemek.fiyat=data.get("fiyat",yemek.fiyat)
    yemek.aciklama=data.get("aciklama",yemek.aciklama)

    db.session.commit()
    return jsonify({"mesaj":"Yemek güncellendi","Yemek":yemek.to_dict()})

@app.route("/yemekler/<int:id>",methods=["DELETE"])
@token_gerekli
def yemegi_sil(id,kullanici_id):
    yemek=Yemek.query.filter_by(id=id,kullanici_id=kullanici_id).first()
    if not yemek:
        return jsonify({"hata":"Yemek bulunamadi"}),404
    
    db.session.delete(yemek)
    db.session.commit()
    return jsonify({"mesaj":"Yemek silindi"})

if __name__=="__main__":
    app.run(debug=True,port=5001)

