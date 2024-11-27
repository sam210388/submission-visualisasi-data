# Dashboard Data Analysis

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis data transaksi, produk, dan pelanggan. Aplikasi ini menyediakan visualisasi data yang interaktif dan informatif, seperti jumlah pesanan harian, jumlah produk terjual per kategori, dan jumlah pelanggan per negara bagian.

## 🚀 Fitur Utama
1. **Visualisasi Jumlah Pesanan Harian**
   - Menampilkan jumlah pesanan per hari dalam bentuk diagram garis.

2. **Jumlah Produk Terjual Per Kategori**
   - Menghitung dan menampilkan jumlah produk terjual per kategori dalam bentuk bar chart.

3. **Jumlah Produk Terjual Per Negara Bagian**
   - Menghitung jumlah Produk Terjuan berdasarkan negara bagian.

4. **Filter Rentang Waktu**
   - Menyediakan filter berdasarkan rentang waktu untuk menyesuaikan data analisis.

---

## 🛠️ Cara Instalasi dan Menjalankan

### 1. **Persyaratan Sistem**
Pastikan Anda telah menginstal:
- Python >= 3.8
- pip

### 2. **Clone Repository**
Clone project ini ke komputer Anda:
```bash
git clone https://github.com/sam210388/submission-visualisasi-data.git
cd submission-visualisasi-data

```

### 3. **Instalasi**

Install semua library yang dibutuhkan menggunakan requirements.txt:

```bash

pip install -r requirements.txt

```

### 4. **Menjalankan Aplikasi**
Gunakan perintah berikut untuk menjalankan aplikasi Streamlit:

```bash

streamlit run lokasi_folder_anda/dashboard.py

```

ganti lokasi_folder_anda sesuai lokasi anda meletakan folder project

### 4. **Struktur FIle**
```bash
├──submission-visualisasi-data/
   ├── dashboard
      ├── dashboard.py                   # Funtuk menjalankan Streamlit
      ├── customer_dataset.csv           # Dataset pelanggan
      ├── order_items_dataset_df.csv     # Dataset detail item
      ├── products_dataset.csv           # Dataset produk
      ├── order_dataset.csv              # Dataset detail item
   ├── data-project-visualisasi
      ├── customer_dataset.csv           # Dataset pelanggan
      ├── geolocation_dataset.csv        # Dataset geolokasi
      ├── order_items_dataset.csv        # Dataset detail item
      ├── order_payments_dataset.csv     # Dataset Pembayaran
      ├── order_reviews_dataset.csv      # Dataset Review
      ├── order_dataset.csv              # Dataset Orders
      ├── product_category_name.csv      # Dataset Kategori Produk
      ├── products_dataset.csv           # Dataset Produk
      ├── sellers_dataset.csv            # Dataset Penjual
   ├── requirements.txt                  # Dependencies
   ├── README.md                         # Dokumentasi ini
   ├── LICENSE                           # Lisensi Aplikasi
   ├── Proyek_Analisis_data_SAM.ipynb    # Lisensi Aplikasi

```

### 5. **📧 Kontak**
Jika ada pertanyaan, Anda dapat menghubungi:

Nama: Nama Anda
Email: emailanda@example.com

