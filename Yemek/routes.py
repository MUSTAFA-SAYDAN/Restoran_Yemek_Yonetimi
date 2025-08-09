from flask import Blueprint, request, jsonify
from decorators import token_dogrula
from Yemek.services import yemek_ekle, yemek_getir, yemek_guncelle, yemek_sil
from Yemek.validators import eksik_alan_kontrol
from models import Yemek

yemek_bp = Blueprint("yemekler", __name__)

@yemek_bp.route("/", methods=["POST"])
@token_dogrula
def yemek_ekle_route():
    veri = request.get_json()
    eksik = eksik_alan_kontrol(veri, ["isim", "kategori", "fiyat", "aciklama"])
    if eksik:
        return jsonify({"hata": f"{eksik} alanı eksik"}), 400

    yeni_yemek = yemek_ekle(
        veri["isim"],
        veri["kategori"],
        veri["fiyat"],
        veri["aciklama"],
        request.kullanici_id
    )
    return jsonify({"mesaj": "Yemek eklendi", "yemek_id": yeni_yemek.id}), 201

@yemek_bp.route("/", methods=["GET"])
@token_dogrula
def yemekleri_getir():
    yemekler = Yemek.query.filter_by(kullanici_id=request.kullanici_id).all()
    sonuc = [y.to_dict() for y in yemekler]
    return jsonify(sonuc), 200

@yemek_bp.route("/<int:yemek_id>", methods=["GET"])
@token_dogrula
def yemek_getir_route(yemek_id):
    yemek = Yemek.query.filter_by(id=yemek_id, kullanici_id=request.kullanici_id).first()
    return jsonify(yemek.to_dict()), 200

@yemek_bp.route("/<int:yemek_id>", methods=["PUT"])
@token_dogrula
def yemek_guncelle_route(yemek_id):
    veri = request.get_json()
    yemek = Yemek.query.filter_by(id=yemek_id, kullanici_id=request.kullanici_id).first()
    yemek_guncelle(
        yemek,
        veri.get("isim"),
        veri.get("kategori"),
        veri.get("fiyat"),
        veri.get("aciklama")
    )
    return jsonify({"mesaj": "Yemek güncellendi"}), 200

@yemek_bp.route("/<int:yemek_id>", methods=["DELETE"])
@token_dogrula
def yemek_sil_route(yemek_id):
    yemek = Yemek.query.filter_by(id=yemek_id, kullanici_id=request.kullanici_id).first()
    yemek_sil(yemek)
    return jsonify({"mesaj": "Yemek silindi"}), 200
