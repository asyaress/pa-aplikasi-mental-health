import json
import os
from .helpers import determine_kategori, get_dummy_patients
from ..config import (
    PASIEN_FILE,
    DOKTER_FILE,
    USERS_FILE,
    ITEM_FILE,
    SET_FILE,
    ROLE_FILE,
)


def _load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_patients_for_table():
    data = _load_json(PASIEN_FILE)
    if not data:
        return get_dummy_patients()

    patients = []
    for p in data:
        nama = p.get("nama", "Unknown")
        diagnosa = p.get("diagnosa", "Tidak ada diagnosa")
        pekerjaan = p.get("pekerjaan", p.get("pendidikan", "Tidak diketahui"))
        kategori = determine_kategori(diagnosa)
        patients.append([nama, diagnosa, pekerjaan, kategori, p])

    return patients or get_dummy_patients()


def load_doctors_for_table():
    data = _load_json(DOKTER_FILE)
    doctors = []
    for d in data:
        nama = d.get("nama", "Dokter")
        spesialis = d.get("spesialis", "-")
        tempat = d.get("tempat_praktik", d.get("tempat_kerja", "-"))
        status = "Aktif" if d.get("is_active", True) else "Nonaktif"
        doctors.append([nama, spesialis, tempat, status, d])
    return doctors


def load_question_sets():
    data = _load_json(SET_FILE)
    sets_by_id = {}
    for s in data:
        sid = s.get("id")
        if sid is not None:
            sets_by_id[sid] = s
    return sets_by_id


def load_questions_for_table(question_sets=None):
    if question_sets is None:
        question_sets = load_question_sets()
    items = _load_json(ITEM_FILE)
    rows = []
    for it in items:
        nomor = it.get("nomor_urut", 0)
        teks = it.get("teks_pertanyaan", "")
        id_set = it.get("id_set_pertanyaan")
        nama_set = question_sets.get(id_set, {}).get("nama_set", f"Set {id_set}")
        rows.append([nomor, teks, nama_set, it])
    rows.sort(key=lambda r: r[0])
    return rows


def load_roles_for_table():
    data = _load_json(ROLE_FILE)
    roles = []
    for r in data:
        rid = r.get("id")
        nama = r.get("nama_role", "")
        roles.append([rid, nama, r])
    roles.sort(key=lambda x: x[0] if x[0] is not None else 0)
    return roles


def get_all_patients():
    return _load_json(PASIEN_FILE)


def save_all_patients(data):
    _save_json(PASIEN_FILE, data)


def get_all_doctors():
    return _load_json(DOKTER_FILE)


def save_all_doctors(data):
    _save_json(DOKTER_FILE, data)


def get_all_users():
    return _load_json(USERS_FILE)


def save_all_users(data):
    _save_json(USERS_FILE, data)


def get_all_items():
    return _load_json(ITEM_FILE)


def save_all_items(data):
    _save_json(ITEM_FILE, data)


def get_all_roles():
    return _load_json(ROLE_FILE)


def save_all_roles(data):
    _save_json(ROLE_FILE, data)
