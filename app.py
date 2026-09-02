import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, static_folder='static')
app.secret_key = 'alumni-komunitas-hendra-media-tech-2026'

DATA_FILE = '/tmp/alumni_data.json'

DATA_DEFAULT = {
    "info_komunitas": {
        "nama": "Ikatan Alumni & Komunitas Hendra",
        "tagline": "Connecting People, Building Network, Creating Impact",
        "total_anggota": 150
    },
    "agenda": [
        {
            "id": 1,
            "judul": "Reuni Akbar & Silaturahmi Lintas Angkatan 2026",
            "tanggal": "Sabtu, 14 November 2026",
            "lokasi": "Grand Hall Hendra Center",
            "keterangan": "Acara ramah tamah, makan bersama, santunan, dan pemilihan pengurus baru."
        }
    ],
    "galeri": [
        {"judul": "Malam Keakraban Reuni 2024", "gambar": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=500"},
        {"judul": "Bakti Sosial & Donor Darah", "gambar": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=500"},
        {"judul": "Gathering & Outbound Anggota", "gambar": "https://images.unsplash.com/photo-1528605248644-14dd04022da1?w=500"}
    ],
    "alumni": [
        {"id": 1, "nama": "Dede Suhendra", "angkatan": "2020", "pekerjaan": "Software Engineer & IT Consultant", "kota": "Bandung", "wa": "6282122900593"},
        {"id": 2, "nama": "Budi Santoso", "angkatan": "2019", "pekerjaan": "Entrepreneur / Pemilik Cafe", "kota": "Jakarta", "wa": "6281234567890"},
        {"id": 3, "nama": "Siti Rahmawati", "angkatan": "2021", "pekerjaan": "UI/UX Designer", "kota": "Surabaya", "wa": "6289876543210"}
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(DATA_DEFAULT, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return DATA_DEFAULT
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DATA_DEFAULT

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

@app.route('/')
def home():
    data = load_data()
    q = request.args.get('q', '').lower()
    
    alumni_list = data['alumni']
    if q:
        alumni_list = [a for a in alumni_list if q in a['nama'].lower() or q in a['angkatan'].lower() or q in a['pekerjaan'].lower() or q in a['kota'].lower()]

    return render_template('index.html', d=data, alumni=alumni_list, q=q)

@app.route('/tambah_alumni', methods=['POST'])
def tambah_alumni():
    data = load_data()
    nama = request.form.get('nama', '').strip()
    angkatan = request.form.get('angkatan', '').strip()
    pekerjaan = request.form.get('pekerjaan', '').strip()
    kota = request.form.get('kota', '').strip()
    wa = request.form.get('wa', '').strip()

    if nama and angkatan:
        new_alumni = {
            "id": len(data['alumni']) + 1,
            "nama": nama,
            "angkatan": angkatan,
            "pekerjaan": pekerjaan or "Lainnya",
            "kota": kota or "Indonesia",
            "wa": wa or "6282122900593"
        }
        data['alumni'].insert(0, new_alumni)
        save_data(data)
        flash('Data Anda berhasil didaftarkan ke Database Alumni!', 'success')

    return redirect(url_for('home') + '#direktori')

if __name__ == '__main__':
    app.run(debug=True)
