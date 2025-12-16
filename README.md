# SPK Status Gizi Anak - Fuzzy Sugeno Orde-Nol 👶

Aplikasi web Sistem Pendukung Keputusan (SPK) untuk menentukan status gizi dan risiko obesitas pada anak menggunakan metode **Fuzzy Sugeno Orde-Nol**.

Project ini dibangun sebagai implementasi tugas akhir mata kuliah untuk melakukan komputasi cerdas dalam diagnosa gizi anak, merujuk pada penelitian Mohamad Imam Gozali (2020).

## 👥 Tim Pengembang

1. **Muhamad Marseal Purwo Syah Putra**
2. **Muhamad Syaid Husein**
3. **Muhamad Widad Gusfyananda**
4. **Muhammad Fikri Rezandi**
5. **Naufal Alfi Rabani**

## 🚀 Fitur Utama

- **Metode Fuzzy Sugeno Orde-Nol:** Implementasi algoritma logika fuzzy dengan output konstanta tegas (Crisp Constant).
- **Batch Processing (CSV):** Fitur upload file CSV untuk memproses data banyak anak sekaligus secara otomatis.
- **Smart Logic Conversion:** Fitur cerdas yang mengonversi satuan tahun ke bulan secara otomatis untuk akurasi perhitungan.
- **Edukasi User (Panduan Ibu):** Antarmuka ramah pengguna dengan visualisasi "Meteran Gizi" dan bahasa yang mudah dipahami orang tua.
- **Analisis Kritis:** Sistem dirancang untuk menguji validitas variabel Golongan Darah dalam penentuan status gizi.

## 🛠️ Tech Stack

- **Bahasa Pemrograman:** Python 3.x
- **Framework Web:** Flask
- **Frontend:** HTML5, Tailwind CSS (CDN), Alpine.js
- **Format Data:** CSV

## 📦 Cara Menjalankan Aplikasi

1. **Clone Repository**

   ```bash
   git clone https://github.com/NaufalAlfiR/spk-gizi-sugeno.git
   cd spk-gizi-sugeno

   ```

2. **Install Library** Pastikan Python sudah terinstall, lalu jalankan

   ```bash
   pip install -r requirements.txt

   ```

3. **Jalankan Aplikasi**

   ```bash
   python app.py

   Tunggu sampai muncul tulisan Running on http://127.0.0.1:5000, lalu buka link tersebut di browser.
   ```

## 📄 Lisensi & Referensi

Aplikasi ini dikembangkan untuk tujuan edukasi dan penelitian akademis. Logika perhitungan didasarkan pada jurnal: Gozali, M. I. (2020). Sistem Pengambil Keputusan Menggunakan Fuzzy Sugeno untuk Menentukan Penyakit Obesitas Anak Usia 0 sampai 16 Tahun.
