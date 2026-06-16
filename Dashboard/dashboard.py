import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -- 1. KONFIGURASI HALAMAN --
st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set gaya visual Seaborn
sns.set_theme(style="darkgrid")

# -- 2. DATA LOADING --
@st.cache_data
def load_data():
    # Pastikan struktur path Anda sesuai. Jika error, periksa kembali posisi file csv.
    df = pd.read_csv('./Data/hour.csv') 
    return df

try:
    df_hour = load_data()
except FileNotFoundError:
    st.error("File dataset 'hour.csv' tidak ditemukan. Pastikan file berada di dalam folder 'Data/' pada direktori proyek Anda.")
    st.stop()

# -- 3. HEADER & METRIKS --
st.title('🚲 Bike Sharing Data Dashboard')
st.markdown("Dashboard ini menyajikan analisis data penyewaan sepeda (Bike Sharing Dataset), mengeksplorasi pengaruh cuaca, suhu, hari, dan klaster waktu.")
st.divider()

# Menampilkan metrik utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan Terdata", f"{df_hour['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan per Jam", f"{round(df_hour['cnt'].mean(), 2)}")
with col3:
    st.metric("Penyewa Terdaftar (Registered)", f"{df_hour['registered'].sum():,}")

st.divider()

# -- 4. ORGANISASI TAB --
tab1, tab2 = st.tabs(["📊 Exploratory Data Analysis (EDA)", "⏳ Clustering Time Analysis"])

# ==========================================
# TAB 1: Exploratory Data Analysis (EDA)
# ==========================================
with tab1:
    st.header('Exploratory Data Analysis (EDA)')
    
    # --- Row 1: Cuaca dan Hari ---
    col_kiri, col_kanan = st.columns(2)

    with col_kiri:
        st.subheader('Kondisi Cuaca vs Rata-rata Penyewaan')
        weather_agg = df_hour.groupby(by=['weathersit', 'season']).agg(avg_rentals=('cnt', 'mean')).reset_index()
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='weathersit', y='avg_rentals', data=weather_agg, hue='season', palette='RdBu', ax=ax1)
        ax1.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Berawan, 3: Hujan Ringan, 4: Hujan Berat)')
        ax1.set_ylabel('Rata-rata Penyewaan')
        ax1.set_xticklabels(['Cerah', 'Berawan', 'Hujan Rgn', 'Hujan Brt'])
        ax1.legend(title='Musim', loc='upper right')
        st.pyplot(fig1)

    with col_kanan:
        st.subheader('Hari Kerja vs Akhir Pekan/Libur')
        working_day = df_hour.groupby(by='workingday').agg(
            avg_rentals=('cnt', 'mean')
        ).reset_index()
        
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='workingday', y='avg_rentals', data=working_day, palette='cividis', ax=ax2)
        ax2.set_xlabel('Tipe Hari')
        ax2.set_ylabel('Rata-rata Penyewaan')
        ax2.set_xticklabels(['Akhir Pekan/Libur', 'Hari Kerja'])
        st.pyplot(fig2)

    # --- Row 2: Jam & Hari (Line Plot) ---
    st.divider()
    st.subheader('Tren Penyewaan Berdasarkan Jam dalam Seminggu')
    weekday_hour = df_hour.groupby(by=['weekday', 'hr']).agg(
        avg_rentals=('cnt', 'mean')
    ).reset_index()

    fig3, ax3 = plt.subplots(figsize=(14, 6))
    sns.lineplot(x='hr', y='avg_rentals', hue='weekday', data=weekday_hour, marker='o', palette='tab10', ax=ax3, linewidth=2)
    ax3.set_xlabel('Jam (00:00 - 23:00)')
    ax3.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax3.set_xticks(range(0, 24, 1))
    
    # Custom Legend Labels
    handles, labels = ax3.get_legend_handles_labels()
    # Asumsi 0=Minggu berdasarkan dataset asli, jika 0=Senin, sesuaikan.
    hari_labels = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'] 
    ax3.legend(handles=handles, title='Hari', labels=hari_labels)
    
    st.pyplot(fig3)
    st.info("💡 **Insight Tren:** Pada hari kerja, terlihat lonjakan penyewaan di pagi (jam 8) dan sore hari (jam 17-18). Sementara pada akhir pekan, tren lebih melandai dengan puncaknya pada siang hari (jam 12-15).")

    # --- Row 3: Suhu ---
    st.divider()
    st.subheader('Dampak Suhu Terhadap Penyewaan')
    # Normalisasi Binning Suhu agar lebih rapi
    temperature = df_hour.groupby(pd.cut(df_hour['temp'], bins=10)).agg(avg_rentals=('cnt', 'mean')).reset_index()

    fig4, ax4 = plt.subplots(figsize=(14, 5))
    sns.barplot(x='temp', y='avg_rentals', data=temperature, palette='YlOrRd', ax=ax4)
    ax4.set_xlabel('Rentang Suhu (Nilai Normalisasi Dataset)')
    ax4.set_ylabel('Rata-rata Penyewaan Sepeda')
    
    # Menggunakan string representasi rentang yang lebih mudah dibaca
    xtick_labels = [f'{round(b.left, 2)} - {round(b.right, 2)}' for b in temperature['temp'].cat.categories]
    ax4.set_xticklabels(xtick_labels, rotation=45)
    st.pyplot(fig4)


# ==========================================
# TAB 2: Advanced Analysis (Clustering Waktu)
# ==========================================
with tab2:
    st.header('Clustering (Binning) Berbasis Waktu')
    st.markdown("Pada analisis ini, waktu (Jam) disegmentasikan ke dalam **5 Klaster/Grup Waktu** untuk melihat perbedaan sebaran dan total jumlah penyewaan.")
    
    # 1. Proses Binning
    df_hour['time_cluster'] = pd.cut(
        df_hour['hr'], 
        bins=[-1, 6, 12, 15, 18, 24], 
        labels=['Dini hari (0-6)', 'Pagi (7-12)', 'Siang (13-15)', 'Sore (16-18)', 'Malam (19-23)']
    )

    # 2. Visualisasi Boxplot & Barplot
    col_clus1, col_clus2 = st.columns(2)

    with col_clus1:
        st.subheader("Distribusi Penyewaan per Klaster (Boxplot)")
        fig5, ax5 = plt.subplots(figsize=(8, 6))
        # Menggunakan Boxplot sesuai rekomendasi sebelumnya untuk sebaran data
        sns.boxplot(x='time_cluster', y='cnt', data=df_hour, palette='Set2', ax=ax5)
        ax5.set_xlabel('Klaster Waktu')
        ax5.set_ylabel('Sebaran Jumlah Penyewaan')
        plt.xticks(rotation=45)
        st.pyplot(fig5)
        
    with col_clus2:
        st.subheader("Total Penyewaan per Klaster (Barplot)")
        # Hitung Total per Klaster
        cluster_total = df_hour.groupby('time_cluster')['cnt'].sum().reset_index()
        fig6, ax6 = plt.subplots(figsize=(8, 6))
        sns.barplot(x='time_cluster', y='cnt', data=cluster_total, palette='Set2', ax=ax6)
        ax6.set_xlabel('Klaster Waktu')
        ax6.set_ylabel('Total Penyewaan (Akumulasi)')
        
        # Tambahkan anotasi angka di atas bar
        for p in ax6.patches:
            ax6.annotate(f"{int(p.get_height()):,}", 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points')
        plt.xticks(rotation=45)
        st.pyplot(fig6)
        
    st.info("💡 **Insight Clustering:** Boxplot menunjukkan bahwa klaster **Sore (16-18)** memiliki median dan nilai maksimal tertinggi. Sementara klaster **Pagi (7-12)** memiliki sebaran data paling luas (banyak outlier ke atas). Secara akumulasi (Barplot), waktu Pagi dan Malam menyumbang total angka penyewaan terbesar.")

# Sidebar untuk Informasi Tambahan / Profil
with st.sidebar:
    st.markdown("### Tentang Dashboard")
    st.markdown("Dibuat untuk menganalisis dan memvisualisasikan insight dari **Bike Sharing Dataset**.")
    st.markdown("---")
    st.markdown("**Pembuat:** Abednego Baharaja Silalahi")
    st.markdown("**Email:** abednego9123@gmail.com")
    st.markdown("**ID Dicoding:** abednego99")