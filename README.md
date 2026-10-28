# Retail Sales Dashboard

## Overview

Retail Sales Dashboard merupakan dashboard visualisasi data yang interaktif yang dikembangkan menggunakan Python dan Streamlit untuk membantu menganalisis data transaksi penjualan retail. Dashboard ini menyajikan informasi penjualan dalam bentuk ringkasan metrik, grafik tren penjualan, serta peringkat produk dan negara berdasarkan kinerja penjualan.

Dashboard dirancang untuk mempermudah pengguna dalam memahami pola penjualan, mengidentifikasi produk dengan kontribusi penjualan tertinggi, dan melihat distribusi penjualan berdasarkan negara serta kanal pemasaran. Informasi yang ditampilkan dapat digunakan sebagai bahan evaluasi dan pendukung pengambilan keputusan bisnis berbasis data.

## Dashboard Preview

Akses dashboard secara langsung melalui tautan berikut:

**Dashboard Retail: https://dashboard-retail-8rbmvmfhceqrqjpe3jqb5a.streamlit.app/**

## Features

### 1. Key Performance Indicators (KPIs)
Menampilkan ringkasan metrik utama untuk memberikan gambaran umum mengenai kinerja penjualan retail.

### 2. Monthly Sales Trend
Menyajikan tren penjualan bulanan untuk membantu mengidentifikasi perubahan nilai penjualan dari waktu ke waktu.

### 3. Top 10 Products
Menampilkan 10 produk teratas berdasarkan nilai penjualan untuk mengetahui produk yang memberikan kontribusi penjualan terbesar.

### 4. Sales by Country
Menyajikan informasi penjualan berdasarkan negara untuk melihat distribusi penjualan di berbagai wilayah pasar.

### 5. Marketing Channel Analysis
Menyajikan visualisasi penjualan berdasarkan kanal pemasaran untuk membantu memahami kontribusi masing-masing kanal terhadap aktivitas penjualan.

### 6. Interactive Filters
Menyediakan filter interaktif melalui sidebar agar pengguna dapat menyesuaikan data yang ditampilkan berdasarkan pilihan yang tersedia.

### 7. Business Insights and Recommendations
Menyajikan ringkasan insight dan rekomendasi bisnis berdasarkan pola yang terlihat pada data dan hasil visualisasi dashboard.

## Data Processing and Metric Definitions

Dashboard menggunakan data transaksi yang telah melalui proses pembersihan dan pengolahan sebelum divisualisasikan.

Beberapa ketentuan pengolahan data yang digunakan meliputi:

- **Gross Revenue:** dihitung berdasarkan perkalian kuantitas barang dengan harga satuan (*Quantity × UnitPrice*).
- **Cancelled Transactions:** transaksi yang dibatalkan dikecualikan dari data yang digunakan untuk analisis penjualan.
- **Product Analysis:** biaya pengiriman (*Postage Fee*) tidak dimasukkan sebagai produk dalam analisis peringkat produk.
- **Returns:** kuantitas negatif tetap dipertahankan untuk merepresentasikan transaksi pengembalian barang sesuai dengan aturan pengolahan data.

**Note:** Gross Revenue pada dashboard merupakan nilai penjualan yang dihitung berdasarkan aturan pengolahan data proyek. Metrik ini tidak secara otomatis merepresentasikan laba bersih atau pendapatan bersih akuntansi.

## Tech Stack

Teknologi dan library yang digunakan dalam pengembangan dashboard meliputi:

- **Python** — bahasa pemrograman utama.
- **Streamlit** — membangun aplikasi dashboard interaktif.
- **Pandas** — pengolahan dan analisis data.
- **NumPy** — operasi numerik.
- **Plotly Express** — membuat visualisasi data interaktif.

## Project Structure

```text
Dashboard-Retail/
├── dashboard_retail.py
├── requirements.txt
└── data/
    └── dashboard.csv
```

*Catatan: Struktur folder di atas merupakan ilustrasi. Sesuaikan nama folder dan file data dengan struktur repository yang sebenarnya.*

## Run Locally

Untuk menjalankan dashboard di lingkungan lokal, ikuti langkah berikut.

### 1. Clone Repository

```bash
git clone https://github.com/Auliakartika150/Dashboard-Retail.git
```

### 2. Navigate to Project Directory

```bash
cd Dashboard-Retail
```

### 3. Install Dependencies

Pastikan Python sudah terpasang, kemudian jalankan:

```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard

```bash
streamlit run dashboard_retail.py
```

Setelah aplikasi berjalan, buka alamat lokal yang ditampilkan di terminal untuk mengakses dashboard melalui browser.

## Deployment

Dashboard telah dipublikasikan menggunakan Streamlit Community Cloud dan dapat diakses melalui tautan berikut:

https://dashboard-retail-8rbmvmfhceqrqjpe3jqb5a.streamlit.app/

## Objectives

Proyek ini bertujuan untuk:

- Menyajikan informasi transaksi retail dalam bentuk visualisasi yang mudah dipahami.
- Mengidentifikasi tren penjualan bulanan dan produk dengan nilai penjualan tertinggi.
- Memahami distribusi penjualan berdasarkan negara dan kanal pemasaran.
- Mendukung proses evaluasi kinerja penjualan melalui eksplorasi data interaktif.
- Menghasilkan insight yang dapat digunakan sebagai bahan pertimbangan dalam pengambilan keputusan bisnis.
