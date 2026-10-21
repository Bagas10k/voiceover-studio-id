# 🎙️ VoiceOver Studio Indonesia (VoiceOver ID)

Generator Voice Over Bahasa Indonesia Natural HD berbasis Python & Microsoft Edge Neural WebSocket Engine.  
Dirancang khusus untuk kebutuhan produksi video YouTube, TikTok, presentasi web, dan narasi multimedia tanpa ketergantungan API berbayar.

---

## ⚡ Fitur Utama

- **100% Suara Alami Bahasa Indonesia:** Menggunakan model vokal Neural HD terdepan:
  - `gadis` (`id-ID-GadisNeural`): Suara wanita ramah, hangat, dan ekspresif (sangat cocok untuk video reels, tutorial, dan presentasi produk).
  - `ardi` (`id-ID-ArdiNeural`): Suara pria tegas, formal, dan berwibawa (cocok untuk video warta berita, dokumenter, dan panduan sistem).
- **Zero Cloud API Key:** Bekerja langsung via WebSocket aman tanpa perlu registrasi akun atau kuota berbayar.
- **Dukungan Naskah Panjang:** Mampu memproses naskah hingga 10.000 karakter per sesi dengan streaming chunk langsung ke MP3.
- **Kendali Prosodi:** Mendukung pengaturan kecepatan bicara (`--rate`) dan tinggi-rendah nada suara (`--pitch`).
- **Piping UNIX / Stdin:** Dapat menerima input dari file teks, file markdown, atau `cat naskah.txt | python3 voiceover.py`.

---

## 🛠️ Instalasi

Pastikan sistem Anda telah terpasang Python 3.9+ dan paket dependensi:

```bash
git clone https://github.com/Bagas10k/voiceover-studio-id.git
cd voiceover-studio-id

# Install dependensi
pip install edge-tts
```

---

## 🚀 Cara Penggunaan

### 1. Perintah Dasar
```bash
python3 voiceover.py "Halo semuanya, selamat datang di showcase aplikasi kasir toko bangunan!" -o intro.mp3
```

### 2. Memilih Karakter Suara
```bash
# Suara Pria Berwibawa (Ardi)
python3 voiceover.py "Laporan sistem harian telah selesai diperiksa." --voice ardi -o laporan.mp3

# Suara Wanita Ramah (Gadis)
python3 voiceover.py "Yuk simak tutorial lengkapnya di video berikut ini!" --voice gadis -o promo.mp3
```

### 3. Mengatur Tempo & Nada
```bash
# Berbicara 15% lebih cepat (cocok untuk video TikTok pendek)
python3 voiceover.py "Trik koding rahasia yang jarang diketahui orang." --rate 15 -o cepat.mp3

# Nada suara lebih rendah / berat (-10 Hz)
python3 voiceover.py "Pengumuman penting untuk seluruh anggota tim." --voice ardi --pitch -10 -o berat.mp3
```

### 4. Menggunakan File Naskah (Piping)
```bash
cat naskah_video.txt | python3 voiceover.py -o narasi_penuh.mp3 --voice gadis
```

---

## 📄 Hak Cipta & Lisensi

Diciptakan dan dikembangkan oleh **Bagas Cihuy** (Bagas Saputra).  
Didistribusikan di bawah lisensi MIT — bebas digunakan untuk proyek komersial maupun pribadi.
