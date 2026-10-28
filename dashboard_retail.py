"""
RETAIL DASHBOARD (Streamlit)

Cara menjalankan:
    streamlit run dashboard_retail.py

Data: letakkan cleaned_retail_with_flags.csv di folder yang sama dengan file ini.
(Kalau file tidak ditemukan, dashboard akan menampilkan tombol untuk mengunggahnya.)

Definisi:
- Pendapatan = kolom Active_Gross_Revenue (Quantity x UnitPrice, transaksi dibatalkan = 0,
  sudah termasuk biaya kirim / postage).
- Pesanan = jumlah InvoiceNo unik yang tidak dibatalkan.
- Analisis produk dan jumlah unit tidak menghitung baris biaya kirim.
"""

import inspect
import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PENGATURAN (boleh diubah)
# ============================================================
MATA_UANG = "£"  # dataset retail ini umumnya dalam poundsterling; ganti jika berbeda
FILE_DATA = ["cleaned_retail_with_flags.csv", "cleaned_retail_active.csv"]

NAVY, BLUE, TEAL, ORANGE, GRAY, SOFT = "#172554", "#3B82F6", "#10B981", "#F59E0B", "#64748B", "#CBD5E1"
PURPLE, PINK, SKY, PALE = "#8B5CF6", "#EC4899", "#38BDF8", "#F5F8FF"
PALETTE = [BLUE, TEAL, ORANGE, PURPLE, PINK, SKY]

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
BULAN_SINGKAT = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

st.set_page_config(
    page_title="Retail Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
      :root {{ color-scheme: light; }}
      .stApp {{ background: linear-gradient(180deg, #F4F7FF 0%, #F8FAFC 48%, #F4F8FC 100%); }}
      [data-testid="stHeader"] {{ background: rgba(244,247,255,.88); }}
      [data-testid="stSidebar"] {{
          background: linear-gradient(180deg, #EAF1FF 0%, #F2F7FC 55%, #EAFBF7 100%);
          border-right: 1px solid #DCE6F4;
      }}
      [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
      [data-testid="stSidebar"] h3 {{ color: {NAVY}; }}
      .block-container {{ padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1500px; }}
      h1, h2, h3 {{ color: {NAVY}; letter-spacing: -0.025em; }}
      h1 {{ font-weight: 800 !important; }}
      h2 {{ font-weight: 750 !important; }}
      .hero {{
          background: linear-gradient(115deg, #172554 0%, #1D4ED8 58%, #0F9F8F 100%);
          border-radius: 20px; padding: 25px 30px; margin: .2rem 0 1.2rem 0;
          box-shadow: 0 12px 30px rgba(37, 99, 235, .16); color: white;
          position: relative; overflow: hidden;
      }}
      .hero:after {{ content: ""; position: absolute; width: 220px; height: 220px; border-radius: 50%;
          right: -45px; top: -100px; background: rgba(255,255,255,.09); }}
      .hero-title {{ color: #FFFFFF; font-size: 2rem; font-weight: 800; line-height: 1.15; margin: 0; }}
      .hero-subtitle {{ color: #E0F2FE; font-size: .98rem; margin-top: .55rem; margin-bottom: 0; }}
      .hero-period {{ display: inline-block; margin-top: 1rem; padding: 5px 11px; border-radius: 999px;
          background: rgba(255,255,255,.16); color: #FFFFFF; font-size: .82rem; }}
      div[data-testid="stMetric"] {{
          background: #FFFFFF; border: 1px solid #E3EAF5; border-radius: 16px;
          padding: 16px 17px 15px 17px; box-shadow: 0 5px 16px rgba(23,37,84,.055);
          border-top: 4px solid {BLUE}; transition: transform .15s ease, box-shadow .15s ease;
      }}
      div[data-testid="stHorizontalBlock"] div[data-testid="stMetric"]:nth-child(1) {{ border-top-color: {BLUE}; }}
      div[data-testid="stMetric"]:hover {{ box-shadow: 0 8px 22px rgba(23,37,84,.10); }}
      div[data-testid="stMetricLabel"] p {{ color: #64748B; font-size: .82rem; font-weight: 600; }}
      div[data-testid="stMetricValue"] {{ color: {NAVY}; font-weight: 800; font-size: 1.55rem; }}
      div[data-testid="stMetricDelta"] {{ font-size: .8rem; }}
      div[data-testid="stPlotlyChart"] {{
          background: #FFFFFF; border: 1px solid #E4EAF4; border-radius: 16px;
          padding: 7px 7px 2px 7px; box-shadow: 0 4px 14px rgba(23,37,84,.035);
      }}
      [data-testid="stDataFrame"] {{ background: white; border: 1px solid #E4EAF4; border-radius: 14px; overflow: hidden; }}
      [data-testid="stMultiSelect"] [data-baseweb="tag"] {{
          background: #DDEAFE !important; border: 1px solid #C5D9FB !important; border-radius: 8px !important;
      }}
      [data-testid="stMultiSelect"] [data-baseweb="tag"] span {{ color: #1E40AF !important; font-weight: 600; }}
      [data-testid="stMultiSelect"] [data-baseweb="tag"] svg {{ fill: #3B82F6 !important; }}
      div[data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 1px solid #DCE6F4; }}
      button[data-baseweb="tab"] {{ background: transparent; border-radius: 10px 10px 0 0; padding: 10px 15px; }}
      button[data-baseweb="tab"][aria-selected="true"] {{ background: #E8F0FF; }}
      button[data-baseweb="tab"][aria-selected="true"] p {{ color: {BLUE}; font-weight: 750; }}
      div[data-baseweb="tab-highlight"] {{ background-color: {BLUE} !important; height: 3px; }}
      .insight {{
          background: linear-gradient(100deg, #E9F1FF 0%, #E7FAF5 100%);
          border: 1px solid #D5E7F8; border-left: 5px solid {TEAL}; border-radius: 13px;
          padding: 14px 18px; color: #243B53; font-size: .94rem; line-height: 1.75; margin: 1rem 0 1.3rem 0;
          box-shadow: 0 4px 12px rgba(23,37,84,.035);
      }}
      .section-note {{ color: #64748B; font-size: .88rem; margin-top: -.4rem; }}
      .subtitle {{ color: #E0F2FE; }}
      [data-testid="stExpander"] {{ background: #FFFFFF; border: 1px solid #E3EAF5; border-radius: 12px; }}
      .stButton > button {{ border-radius: 10px; }}
      @media (max-width: 768px) {{
          .block-container {{ padding-top: 1rem; }}
          .hero {{ padding: 20px; border-radius: 15px; }}
          .hero-title {{ font-size: 1.55rem; }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNGSI BANTU: format angka dan tampilan
# ============================================================
def angka(nilai, desimal=0):
    """Format Indonesia: 1.234,56"""
    teks = f"{nilai:,.{desimal}f}"
    return teks.replace(",", "X").replace(".", ",").replace("X", ".")


def uang(nilai, desimal=0):
    return f"{MATA_UANG}{angka(nilai, desimal)}"


def uang_ringkas(nilai):
    """Angka besar dibuat ringkas, misalnya £1,25 juta."""
    for batas, satuan in [(1e9, "miliar"), (1e6, "juta")]:
        if abs(nilai) >= batas:
            return f"{MATA_UANG}{angka(nilai / batas, 2)} {satuan}"
    return uang(nilai)


def persen(nilai):
    return f"{nilai:.1f}%".replace(".", ",")


def nama_bulan(tanggal):
    return f"{BULAN[tanggal.month - 1]} {tanggal.year}"


def label_bulan(tanggal):
    return f"{BULAN_SINGKAT[tanggal.month - 1]} {tanggal.year}"


def tanggal_id(tanggal):
    return f"{tanggal.day} {BULAN_SINGKAT[tanggal.month - 1]} {tanggal.year}"


def gaya(fig, tinggi=340):
    fig.update_layout(
        height=tinggi,
        margin=dict(l=10, r=10, t=50, b=10),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#24364B", family="Arial, sans-serif", size=12),
        title_font=dict(color=NAVY, size=16),
        title_font_size=16,
        coloraxis_showscale=False,
        separators=",.",  # pemisah desimal koma, ribuan titik
    )
    fig.update_xaxes(gridcolor="#E8EEF5", zerolinecolor="#DCE5F0")
    fig.update_yaxes(gridcolor="#E8EEF5", zerolinecolor="#DCE5F0")
    return fig


# Streamlit versi baru memakai width="stretch", versi lama use_container_width=True.
_PLOTLY_PUNYA_WIDTH = "width" in inspect.signature(st.plotly_chart).parameters


def tampil_grafik(fig):
    if _PLOTLY_PUNYA_WIDTH:
        st.plotly_chart(fig, width="stretch")
    else:
        st.plotly_chart(fig, use_container_width=True)


def tampil_tabel(tabel):
    try:
        st.dataframe(tabel, width="stretch", hide_index=True)
    except Exception:
        st.dataframe(tabel, use_container_width=True, hide_index=True)


def batang_horizontal(tabel, x, y, judul, judul_x, warna=BLUE, format_uang=True):
    fig = px.bar(tabel, x=x, y=y, orientation="h", title=judul, labels={x: judul_x, y: ""},
                 color=x, color_continuous_scale=["#DCEAFE", warna, NAVY])
    fig.update_layout(coloraxis_showscale=False)
    fig.update_traces(marker_line_color="rgba(255,255,255,.85)", marker_line_width=0.6)
    if format_uang:
        fig.update_xaxes(tickprefix=MATA_UANG, tickformat=",.0f")
        fig.update_traces(hovertemplate="%{y}<br>" + MATA_UANG + "%{x:,.0f}<extra></extra>")
    else:
        fig.update_traces(hovertemplate="%{y}<br>%{x:,.0f}<extra></extra>")
    fig.update_yaxes(automargin=True)
    return gaya(fig, 380)


def donat(tabel, nama, nilai, judul, warna=None):
    fig = px.pie(tabel, names=nama, values=nilai, hole=0.6, title=judul,
                 color_discrete_sequence=warna or [BLUE, TEAL, ORANGE, PURPLE, PINK, SKY, SOFT])
    fig.update_traces(textinfo="percent+label", textposition="inside", marker_line_color="white", marker_line_width=2, insidetextfont=dict(color="white", size=11))
    fig.update_layout(showlegend=False)
    return gaya(fig, 380)


# ============================================================
# MEMUAT DAN MEMBERSIHKAN DATA
# ============================================================
def cari_file():
    folder_script = Path(__file__).resolve().parent
    # 1) di folder yang sama dengan file ini, atau di folder kerja terminal
    for folder in (folder_script, Path.cwd()):
        for nama in FILE_DATA:
            path = folder / nama
            if path.exists():
                return path
    # 2) di subfolder mana pun di bawahnya (misalnya "Output Retail")
    for nama in FILE_DATA:
        hasil = sorted(folder_script.rglob(nama))
        if hasil:
            return hasil[0]
    return None


@st.cache_data(show_spinner="Memuat data...")
def muat_data(nama_sumber, versi, isi):
    """nama_sumber dan versi hanya dipakai agar cache diperbarui saat file berubah."""
    sumber = io.BytesIO(isi) if isi is not None else nama_sumber
    df = pd.read_csv(sumber, dtype={"InvoiceNo": "string", "StockCode": "string"})

    wajib = {"InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice", "CustomerID",
             "Country", "Source", "is_cancelled", "tx_type", "InvoiceDate_dt"}
    hilang = wajib - set(df.columns)
    if hilang:
        raise ValueError(f"Kolom wajib tidak ditemukan: {sorted(hilang)}")

    df["InvoiceDate_dt"] = pd.to_datetime(df["InvoiceDate_dt"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate_dt"]).copy()

    df["is_cancelled"] = df["is_cancelled"].astype(str).str.strip().str.lower().eq("true")
    if "is_postage" in df.columns:
        df["is_postage"] = df["is_postage"].astype(str).str.strip().str.lower().eq("true")
    else:
        df["is_postage"] = df["StockCode"].astype(str).str.upper().eq("POST")

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["Nilai"] = df["Quantity"] * df["UnitPrice"]
    if "Active_Gross_Revenue" in df.columns:
        df["Active_Gross_Revenue"] = pd.to_numeric(df["Active_Gross_Revenue"], errors="coerce").fillna(0)
    else:
        df["Active_Gross_Revenue"] = np.where(df["is_cancelled"], 0.0, df["Nilai"])

    for kolom in ["Description", "Country", "Source", "tx_type"]:
        df[kolom] = df[kolom].astype("string").str.strip().replace("", pd.NA).fillna("Tidak diketahui").astype(str)
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
    df["Bulan"] = df["InvoiceDate_dt"].dt.to_period("M").dt.to_timestamp()
    return df


path_data = cari_file()
unggahan = None
if path_data is None:
    st.title("Retail Dashboard")
    st.warning("File data belum ditemukan di folder ini. Letakkan cleaned_retail_with_flags.csv di folder "
               "yang sama dengan dashboard_retail.py, atau unggah file-nya di bawah.")
    unggahan = st.file_uploader("Unggah cleaned_retail_with_flags.csv", type="csv")
    if unggahan is None:
        st.stop()

try:
    if unggahan is not None:
        df = muat_data(unggahan.name, 0.0, unggahan.getvalue())
    else:
        df = muat_data(str(path_data), path_data.stat().st_mtime, None)
except Exception as exc:
    st.error(f"Data gagal dibaca: {exc}")
    st.stop()

if df.empty:
    st.error("Data kosong atau kolom tanggal tidak valid.")
    st.stop()

ADA_PEMBATALAN = bool(df["is_cancelled"].any())  # False jika yang dimuat hanya file "active"

# ============================================================
# FILTER
# ============================================================
st.sidebar.title("Filter")
tgl_min, tgl_max = df["InvoiceDate_dt"].min().date(), df["InvoiceDate_dt"].max().date()
rentang = st.sidebar.date_input("Periode", value=(tgl_min, tgl_max), min_value=tgl_min, max_value=tgl_max)
if isinstance(rentang, (tuple, list)):
    awal, akhir = (rentang[0], rentang[1]) if len(rentang) == 2 else (rentang[0], rentang[0])
else:
    awal = akhir = rentang

sel_negara = st.sidebar.multiselect("Negara", sorted(df["Country"].unique()), placeholder="Semua negara")
sel_channel = st.sidebar.multiselect("Channel pemasaran", sorted(df["Source"].unique()), placeholder="Semua channel")

mask = df["InvoiceDate_dt"].dt.date.between(awal, akhir)
if sel_negara:
    mask &= df["Country"].isin(sel_negara)
if sel_channel:
    mask &= df["Source"].isin(sel_channel)

data = df[mask]
aktif = data[~data["is_cancelled"]]   # transaksi yang tidak dibatalkan
batal = data[data["is_cancelled"]]    # transaksi yang dibatalkan
produk = aktif[~aktif["is_postage"]]  # baris produk saja (tanpa biaya kirim)

# ============================================================
# HEADER
# ============================================================
st.markdown(
    f'<div class="hero"><p class="hero-title">Retail Performance</p>'
    '<p class="hero-subtitle">Ringkasan penjualan, produk, pasar, channel pemasaran, dan pelanggan.</p>'
    f'<span class="hero-period">Periode {tanggal_id(awal)} – {tanggal_id(akhir)}</span></div>',
    unsafe_allow_html=True,
)

if data.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Ubah pilihan di sidebar.")
    st.stop()
if aktif.empty:
    st.warning("Pada filter ini hanya ada transaksi yang dibatalkan, sehingga tidak ada pendapatan untuk ditampilkan.")
    st.stop()

# ============================================================
# AGREGASI
# ============================================================
total_pendapatan = aktif["Active_Gross_Revenue"].sum()
n_pesanan = aktif["InvoiceNo"].nunique()
n_pelanggan = aktif["CustomerID"].nunique()
rata_pesanan = total_pendapatan / n_pesanan if n_pesanan else 0
n_invoice_semua = data["InvoiceNo"].nunique()
n_invoice_batal = batal["InvoiceNo"].nunique()
tingkat_batal = n_invoice_batal / n_invoice_semua * 100 if n_invoice_semua else 0
nilai_batal = batal["Nilai"].sum()

bulanan = (
    aktif.groupby("Bulan")
    .agg(pendapatan=("Active_Gross_Revenue", "sum"), pesanan=("InvoiceNo", "nunique"),
         pelanggan=("CustomerID", "nunique"))
    .reset_index()
)
unit_bulanan = produk.groupby("Bulan")["Quantity"].sum().rename("unit").reset_index()
bulanan = bulanan.merge(unit_bulanan, on="Bulan", how="left").fillna({"unit": 0}).sort_values("Bulan")
bulanan["Label"] = bulanan["Bulan"].map(label_bulan)

per_produk = (
    produk.groupby("Description")
    .agg(pendapatan=("Active_Gross_Revenue", "sum"), unit=("Quantity", "sum"))
    .reset_index()
)
per_produk["Produk"] = per_produk["Description"].str.capitalize()

per_negara = (
    aktif.groupby("Country")
    .agg(pesanan=("InvoiceNo", "nunique"), pelanggan=("CustomerID", "nunique"),
         pendapatan=("Active_Gross_Revenue", "sum"))
    .reset_index().sort_values("pendapatan", ascending=False)
)

per_channel = (
    aktif.groupby("Source")
    .agg(pesanan=("InvoiceNo", "nunique"), pelanggan=("CustomerID", "nunique"),
         pendapatan=("Active_Gross_Revenue", "sum"))
    .reset_index().sort_values("pendapatan", ascending=False)
)
per_channel["rata2"] = per_channel["pendapatan"] / per_channel["pesanan"]

per_pelanggan = (
    aktif.dropna(subset=["CustomerID"]).groupby("CustomerID")
    .agg(pesanan=("InvoiceNo", "nunique"), pendapatan=("Active_Gross_Revenue", "sum"),
         negara=("Country", "first"))
    .reset_index()
)

# ============================================================
# KPI
# ============================================================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total pendapatan", uang_ringkas(total_pendapatan),
          help=f"Nilai transaksi tidak dibatalkan, termasuk biaya kirim. Nilai lengkap: {uang(total_pendapatan, 2)}")
k2.metric("Jumlah pesanan", angka(n_pesanan), help="Jumlah nomor invoice unik yang tidak dibatalkan.")
k3.metric("Pelanggan aktif", angka(n_pelanggan), help="Pelanggan unik dengan transaksi tidak dibatalkan.")
k4.metric("Rata-rata per pesanan", uang(rata_pesanan, 2), help="Total pendapatan dibagi jumlah pesanan.")
if ADA_PEMBATALAN:
    k5.metric("Tingkat pembatalan", persen(tingkat_batal),
              help=f"{angka(n_invoice_batal)} dari {angka(n_invoice_semua)} invoice dibatalkan "
                   f"(nilai {uang(nilai_batal, 2)}).")
else:
    k5.metric("Tingkat pembatalan", "–", help="Data pembatalan tidak tersedia pada file yang dimuat.")

# ============================================================
# SOROTAN OTOMATIS
# ============================================================
poin = []
terbaik = bulanan.loc[bulanan["pendapatan"].idxmax()]
poin.append(f"Pendapatan tertinggi terjadi pada <b>{nama_bulan(terbaik['Bulan'])}</b> "
            f"({uang_ringkas(terbaik['pendapatan'])}).")
negara_utama = per_negara.iloc[0]
poin.append(f"<b>{negara_utama['Country']}</b> menyumbang "
            f"{persen(negara_utama['pendapatan'] / total_pendapatan * 100)} pendapatan.")
channel_utama = per_channel.iloc[0]
poin.append(f"Channel dengan pendapatan terbesar: <b>{channel_utama['Source']}</b>.")
if not per_produk.empty:
    poin.append(f"Produk dengan pendapatan terbesar: <b>{per_produk.loc[per_produk['pendapatan'].idxmax(), 'Produk']}</b>.")
st.markdown('<div class="insight"><b>Sorotan:</b> ' + " ".join(poin) + "</div>", unsafe_allow_html=True)

# ============================================================
# TAB
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(["Tren Penjualan", "Produk", "Negara & Channel", "Pelanggan"])

with tab1:
    pilihan = {
        "Pendapatan": ("pendapatan", True),
        "Jumlah pesanan": ("pesanan", False),
        "Pelanggan aktif": ("pelanggan", False),
        "Unit terjual": ("unit", False),
    }
    label = st.selectbox("Metrik", list(pilihan))
    kolom, format_uang = pilihan[label]
    kiri, kanan = st.columns([2, 1])
    with kiri:
        fig = px.bar(bulanan, x="Label", y=kolom, title=f"{label} per bulan", labels={"Label": "Bulan", kolom: label},
                     color=kolom, color_continuous_scale=["#DCEAFE", "#60A5FA", "#2563EB", "#172554"])
        fig.update_layout(coloraxis_showscale=False)
        fig.update_traces(marker_line_color="rgba(255,255,255,.85)", marker_line_width=0.7)
        fig.update_xaxes(type="category", categoryorder="array", categoryarray=bulanan["Label"].tolist())
        if format_uang:
            fig.update_yaxes(tickprefix=MATA_UANG, tickformat=",.0f")
            fig.update_traces(hovertemplate="%{x}<br>" + MATA_UANG + "%{y:,.0f}<extra></extra>")
        else:
            fig.update_traces(hovertemplate="%{x}<br>%{y:,.0f}<extra></extra>")
        tampil_grafik(gaya(fig, 380))
    with kanan:
        jenis = data["tx_type"].replace({"Product Sale": "Penjualan produk", "Postage Fee": "Biaya kirim",
                                         "Cancelled": "Dibatalkan"})
        jenis = jenis.value_counts().rename_axis("jenis").reset_index(name="baris")
        tampil_grafik(donat(jenis, "jenis", "baris", "Komposisi jenis transaksi",
                             [TEAL, BLUE, ORANGE, PURPLE, PINK]))

    with st.expander("Lihat tabel ringkasan bulanan"):
        tabel = bulanan[["Bulan", "pesanan", "pelanggan", "unit", "pendapatan"]].copy()
        tabel["Bulan"] = tabel["Bulan"].map(nama_bulan)
        tabel.columns = ["Bulan", "Pesanan", "Pelanggan aktif", "Unit terjual", "Pendapatan"]
        tampil_tabel(tabel.style.format({"Pesanan": angka, "Pelanggan aktif": angka,
                                         "Unit terjual": angka, "Pendapatan": lambda x: uang(x, 2)}))

with tab2:
    if per_produk.empty:
        st.info("Tidak ada penjualan produk pada filter ini.")
    else:
        kiri, kanan = st.columns(2)
        with kiri:
            top = per_produk.nlargest(10, "pendapatan").sort_values("pendapatan")
            tampil_grafik(batang_horizontal(top, "pendapatan", "Produk", "10 produk dengan pendapatan terbesar",
                                            "Pendapatan"))
        with kanan:
            top = per_produk.nlargest(10, "unit").sort_values("unit")
            tampil_grafik(batang_horizontal(top, "unit", "Produk", "10 produk dengan unit terjual terbanyak",
                                            "Unit terjual", TEAL, False))

with tab3:
    kiri, kanan = st.columns(2)
    with kiri:
        top = per_negara.head(8).sort_values("pendapatan")
        tampil_grafik(batang_horizontal(top, "pendapatan", "Country", "8 negara dengan pendapatan terbesar",
                                        "Pendapatan"))
    with kanan:
        top = per_channel.sort_values("pendapatan")
        tampil_grafik(batang_horizontal(top, "pendapatan", "Source", "Pendapatan per channel pemasaran",
                                        "Pendapatan", TEAL))

    st.subheader("Kinerja channel pemasaran")
    tabel = per_channel[["Source", "pesanan", "pelanggan", "pendapatan", "rata2"]].copy()
    tabel.columns = ["Channel", "Pesanan", "Pelanggan", "Pendapatan", "Rata-rata per pesanan"]
    tampil_tabel(tabel.style.format({"Pesanan": angka, "Pelanggan": angka, "Pendapatan": lambda x: uang(x, 2),
                                     "Rata-rata per pesanan": lambda x: uang(x, 2)}))

    with st.expander("Lihat semua negara"):
        tabel = per_negara.copy()
        tabel.columns = ["Negara", "Pesanan", "Pelanggan", "Pendapatan"]
        tampil_tabel(tabel.style.format({"Pesanan": angka, "Pelanggan": angka,
                                         "Pendapatan": lambda x: uang(x, 2)}))

with tab4:
    if per_pelanggan.empty:
        st.info("Tidak ada data pelanggan pada filter ini.")
    else:
        per_pelanggan["Segmen"] = np.where(per_pelanggan["pesanan"] >= 2, "Pelanggan berulang", "Sekali beli")
        n_berulang = int((per_pelanggan["pesanan"] >= 2).sum())
        kiri, kanan = st.columns([1, 2])
        with kiri:
            segmen = per_pelanggan["Segmen"].value_counts().rename_axis("Segmen").reset_index(name="pelanggan")
            tampil_grafik(donat(segmen, "Segmen", "pelanggan", "Sekali beli vs berulang", [SOFT, BLUE]))
            st.caption(f"{angka(n_berulang)} dari {angka(len(per_pelanggan))} pelanggan "
                       f"({persen(n_berulang / len(per_pelanggan) * 100)}) membeli lebih dari satu kali.")
        with kanan:
            st.subheader("10 pelanggan dengan pendapatan tertinggi")
            top = per_pelanggan.nlargest(10, "pendapatan")[["CustomerID", "negara", "pesanan", "pendapatan"]].copy()
            top["CustomerID"] = top["CustomerID"].astype("Int64").astype(str)
            top.columns = ["ID pelanggan", "Negara", "Pesanan", "Pendapatan"]
            tampil_tabel(top.style.format({"Pesanan": angka, "Pendapatan": lambda x: uang(x, 2)}))

st.caption("Pendapatan = Quantity × UnitPrice untuk transaksi yang tidak dibatalkan (termasuk biaya kirim). "
           "Analisis produk dan unit tidak menghitung biaya kirim.")