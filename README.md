# Retail Sales Dashboard

Dashboard interaktif berbasis Streamlit untuk menganalisis kinerja penjualan retail, tren pendapatan, produk terlaris, distribusi penjualan berdasarkan negara, kanal pemasaran, dan perilaku pelanggan.

## Tujuan

Dashboard ini bertujuan untuk menjawab pertanyaan berikut:

1. Bagaimana tren pendapatan, jumlah pesanan, pelanggan aktif, dan unit terjual dari bulan ke bulan?
2. Produk apa yang menghasilkan pendapatan terbesar dan produk apa yang paling banyak terjual?
3. Negara mana yang memberikan kontribusi pendapatan terbesar?
4. Kanal pemasaran mana yang menghasilkan pendapatan dan rata-rata pendapatan per pesanan tertinggi?
5. Seberapa besar transaksi yang dibatalkan dalam keseluruhan data transaksi?

## Data

- **Sumber:** Dataset transaksi retail yang telah melalui proses pembersihan dan pengolahan.
- **Format:** CSV.
- **Informasi utama:** nomor invoice, kode dan nama produk, kuantitas, tanggal transaksi, harga satuan, ID pelanggan, negara, serta kanal pemasaran.
- **Filter:** periode tanggal, negara, dan kanal pemasaran.

### Definisi metrik

| Metrik | Definisi |
|---|---|
| Total pendapatan | Jumlah `Active_Gross_Revenue` dari transaksi yang tidak dibatalkan. |
| Jumlah pesanan | Jumlah `InvoiceNo` unik dari transaksi yang tidak dibatalkan. |
| Pelanggan aktif | Jumlah `CustomerID` unik pada transaksi yang tidak dibatalkan. |
| Rata-rata pendapatan per pesanan | Total pendapatan ÷ jumlah pesanan. |
| Unit terjual | Jumlah `Quantity` pada baris produk, tanpa memasukkan baris biaya kirim. |
| Tingkat pembatalan | Jumlah invoice yang dibatalkan ÷ seluruh invoice unik pada data yang difilter × 100%. |
| Pendapatan per produk | Jumlah `Active_Gross_Revenue` yang dikelompokkan berdasarkan nama produk, tanpa baris biaya kirim dalam analisis produk. |
| Pelanggan berulang | Pelanggan dengan minimal dua nomor invoice unik yang tidak dibatalkan. |

**Catatan pengolahan:** Pendapatan dihitung menggunakan kolom `Active_Gross_Revenue`, yang didasarkan pada `Quantity × UnitPrice`, dengan pendapatan dari transaksi yang dibatalkan bernilai nol. Metrik ini mencakup biaya kirim sesuai definisi dalam kode dashboard. Pendapatan tidak sama dengan laba karena biaya operasional dan biaya lainnya tidak diperhitungkan.

## Ringkasan Hasil

Dashboard menyediakan ringkasan indikator utama yang nilainya berubah mengikuti filter periode, negara, dan kanal pemasaran yang dipilih.

| Indikator | Informasi yang ditampilkan |
|---|---|
| Total pendapatan | Total nilai pendapatan dari transaksi yang tidak dibatalkan. |
| Jumlah pesanan | Jumlah invoice unik yang tidak dibatalkan. |
| Pelanggan aktif | Jumlah pelanggan unik pada transaksi yang tidak dibatalkan. |
| Rata-rata pendapatan per pesanan | Rata-rata pendapatan untuk setiap invoice yang tidak dibatalkan. |
| Tingkat pembatalan | Persentase invoice yang dibatalkan terhadap seluruh invoice dalam filter. |

Nilai numerik ringkasan perlu dibaca langsung dari dashboard sesuai periode dan filter yang digunakan. Oleh karena itu, README ini tidak mencantumkan angka agregat yang belum diverifikasi.

## Temuan Utama

### 1. Tren penjualan bulanan

- **Fakta yang dapat dianalisis:** Grafik bulanan menampilkan perubahan pendapatan, jumlah pesanan, pelanggan aktif, dan unit terjual.
- **Analisis:** Perbandingan antarbulan dapat digunakan untuk mengidentifikasi periode dengan pendapatan tertinggi maupun perubahan volume transaksi.
- **Saran:** Evaluasi periode dengan penjualan tertinggi dan terendah untuk mengetahui pola permintaan serta menentukan strategi penjualan berikutnya.

### 2. Produk dengan kontribusi penjualan terbesar

- **Fakta yang dapat dianalisis:** Dashboard menampilkan 10 produk dengan pendapatan terbesar dan 10 produk dengan jumlah unit terjual terbanyak.
- **Analisis:** Produk dengan pendapatan tertinggi belum tentu merupakan produk dengan volume penjualan tertinggi. Kedua indikator perlu dibandingkan untuk memahami kontribusi produk terhadap penjualan.
- **Saran:** Prioritaskan evaluasi stok dan ketersediaan produk dengan volume penjualan tinggi. Tinjau juga produk dengan pendapatan besar untuk mempertahankan kontribusinya terhadap bisnis.

### 3. Distribusi pendapatan berdasarkan negara

- **Fakta yang dapat dianalisis:** Dashboard menampilkan delapan negara dengan pendapatan terbesar serta tabel yang memuat seluruh negara.
- **Analisis:** Perbedaan pendapatan antarnegara dapat menunjukkan distribusi penjualan pada pasar yang berbeda.
- **Saran:** Evaluasi negara dengan kontribusi pendapatan tinggi untuk mempertahankan pasar utama dan telaah negara dengan pendapatan rendah untuk mengetahui peluang pengembangan pasar.

### 4. Kinerja kanal pemasaran

- **Fakta yang dapat dianalisis:** Dashboard membandingkan pendapatan, jumlah pesanan, jumlah pelanggan, dan rata-rata pendapatan per pesanan berdasarkan kanal pemasaran.
- **Analisis:** Kanal dengan pendapatan tertinggi belum tentu memiliki rata-rata pendapatan per pesanan tertinggi. Perbandingan beberapa metrik diperlukan untuk memahami kinerja masing-masing kanal.
- **Saran:** Bandingkan kontribusi pendapatan dan rata-rata pendapatan per pesanan sebelum menentukan prioritas kanal pemasaran. Data pendapatan saja belum cukup untuk menyimpulkan efektivitas atau keuntungan kanal karena biaya pemasaran tidak diperhitungkan.

### 5. Perilaku dan pembelian berulang pelanggan

- **Fakta yang dapat dianalisis:** Dashboard membagi pelanggan menjadi dua segmen, yaitu pelanggan yang hanya melakukan satu pembelian dan pelanggan yang melakukan pembelian berulang. Dashboard juga menampilkan 10 pelanggan dengan pendapatan tertinggi.
- **Analisis:** Perbandingan kedua segmen dapat membantu memahami pola pembelian pelanggan. Konsentrasi pendapatan pada pelanggan tertentu juga dapat menunjukkan tingkat ketergantungan penjualan terhadap pelanggan tersebut.
- **Saran:** Evaluasi pelanggan berulang untuk memahami pola pembelian dan peluang retensi. Pelanggan dengan kontribusi pendapatan tinggi dapat dianalisis lebih lanjut untuk mengetahui kebutuhan dan karakteristik pembeliannya.

### 6. Transaksi yang dibatalkan

- **Fakta yang dapat dianalisis:** Dashboard menghitung jumlah invoice yang dibatalkan dan menampilkan komposisi jenis transaksi.
- **Analisis:** Tingkat pembatalan dapat digunakan untuk memantau proporsi pesanan yang tidak menghasilkan pendapatan dalam perhitungan dashboard.
- **Saran:** Jika tingkat pembatalan tinggi pada periode atau negara tertentu, lakukan pemeriksaan lebih lanjut terhadap penyebab pembatalan. Data yang tersedia perlu dilengkapi dengan informasi alasan pembatalan agar penyebabnya dapat diidentifikasi.

## Teknologi
- Python
- Pandas
- NumPy
- Plotly Express
- Streamlit

## Menjalankan Dashboard Secara Lokal
### 1. Clone repository
```bash
git clone https://github.com/Auliakartika150/Dashboard-Retail.git
```
### 2. Masuk ke direktori project
```bash
cd Dashboard-Retail
```
### 3. Instal dependensi
```bash
pip install -r requirements.txt
```
### 4. Jalankan aplikasi
```bash
streamlit run dashboard_retail.py
```
## Deployment

Dashboard telah dipublikasikan melalui Streamlit Community Cloud.

**Link Dashboard: https://dashboard-retail-8rbmvmfhceqrqjpe3jqb5a.streamlit.app/**
