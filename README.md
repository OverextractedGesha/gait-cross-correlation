# 🚶 Gait Signal Cross-Correlation Analysis

Aplikasi web interaktif berbasis **Python & Streamlit** untuk menentukan fungsi *Cross-Correlation* dan *Normalisasi* pada sinyal pola berjalan (*Gait Analysis*: `Heel123.txt` dan `Toe123.txt`).

Proyek ini disusun untuk memenuhi tugas mata kuliah **Biomodeling** — Departemen Teknik Biomedik, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC), Institut Teknologi Sepuluh Nopember (ITS).

**Penulis:** Nicolas Aryadhanaputra Paruntu (`5023241039`)

---

## ✨ Fitur Utama
- **Pure Python Calculation Engine:** Seluruh perhitungan matematis (*cross-correlation* $r_{xy}(l)$, normalisasi $\rho_{xy}(l)$, pergeseran sinyal $y_{\text{shifted}}[n]$, serta deteksi puncak lokal) diimplementasikan **murni menggunakan Python standar tanpa pustaka kalkulasi eksternal** (tanpa `NumPy` atau `SciPy`), merujuk langsung pada algoritma modul ajar Delphi ITS.
- **Interaktif & Cepat:** Dilengkapi *slider* Time-Lag ($L = 0 \dots 6580$) dan tombol pintas menuju titik puncak korelasi (**Lag 0**, **Peak 1: Lag 716**, **Peak 2: Lag 1740**).
- **4 Tab Visualisasi Lengkap:**
  1. **Sinyal Gait (Shifted):** Pembuktian visual keterhimpitan sinyal *Heel* dan *Toe* saat digeser sebesar nilai *time-lag*.
  2. **Grafik Cross-Correlation ($R_{xy}$):** Kurva korelasi silang lengkap dengan penanda puncak tertinggi.
  3. **Grafik Normalisasi ($\rho_{xy}$):** Kurva korelasi ternormalisasi terhadap jumlah sampel yang bertumpang-tindih.
  4. **Tabel Inspeksi Data:** Replikasi *ListBox* Delphi untuk melihat nilai numerik $x[L]$, $y[L]$, dan $r_{xy}[L]$ di sekitar *lag* aktif.

---

## 📐 Formulasi Matematis

1. **Cross-Correlation Diskrit:**
   $$r_{xy}(l) = \sum_{n=l}^{N-1} x[n] \cdot y[n - l], \quad l = 0, 1, 2, \dots, N - 1$$

2. **Normalisasi Cross-Correlation:**
   $$\rho_{xy}(l) = \frac{r_{xy}(l)}{(N - 1) - l}, \quad l = 0, 1, 2, \dots, N - 2$$

3. **Pergeseran Sinyal (*Signal Shifting*):**
   $$y_{\text{shifted}}[n] = \begin{cases} 0, & n < L \\ y[n - L], & n \ge L \end{cases}$$

---

## 📊 Ringkasan Hasil Utama

| Peringkat Puncak | Time-Lag ($L$) | Nilai $R_{xy}[L]$ | Nilai Normalisasi $\rho_{xy}[L]$ |
| :---: | :---: | :---: | :---: |
| **Puncak 1 (Global)** | **716** | **2462.208** | **0.4199** |
| **Puncak 2** | **1740** | **1838.050** | **0.3798** |
| **Puncak 3** | **2779** | **1370.890** | **0.3607** |

> Selisih antar puncak $\Delta L = 1740 - 716 = 1024\text{ sampel}$ merepresentasikan durasi satu siklus gaya berjalan penuh (*one complete stride period*).

---

## 📂 Struktur Repositori

- `app.py` — Kode program utama (*Core Calculation Engine* Pure Python & GUI Streamlit).
- `Heel123.txt` — Dataset sinyal sensor tumit ($6.581$ sampel).
- `Toe123.txt` — Dataset sinyal sensor ujung jari kaki ($6.581$ sampel).
- `requirements.txt` — Daftar pustaka antarmuka & visualisasi (`streamlit`, `matplotlib`).
- `README.md` — Dokumentasi proyek.

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/OverextractedGesha/gait-cross-correlation.git
   cd gait-cross-correlation
   ```

2. **Instal pustaka antarmuka & visualisasi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi Streamlit:**
   ```bash
   streamlit run app.py
   ```

4. Buka browser pada alamat `http://localhost:8501`.
