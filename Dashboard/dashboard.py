import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset
df_hour = pd.read_csv('./Data/hour.csv')  # Pastikan jalur file CSV sesuai dengan struktur folder Anda

st.title('Bike Sharing Dashboard')

with st.sidebar:
    st.header('Dashboard Sidebar')
    st.text('Pilih Tampilan')
    pilihan = st.selectbox(
        label="Pilih tampilan",
        options=('Exploratory Data Analysis (EDA)', 'Advanced Analysis')
    )

# Tampilan untuk EDA
if pilihan == 'Exploratory Data Analysis (EDA)':
    st.header('Exploratory Data Analysis (EDA)')

    # Visualisasi Rata-rata Penyewaan Berdasarkan Kondisi Cuaca
    weather_agg = df_hour.groupby(by=['weathersit', 'season']).agg(avg_rentals=('cnt', 'mean')).reset_index()

    fig, ax = plt.subplots()
    sns.barplot(x='weathersit', y='avg_rentals', data=weather_agg, hue='season', palette='coolwarm', ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Berawan, 3: Hujan Ringan, 4: Hujan Berat)')
    ax.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax.set_xticklabels(['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Berat'])
    st.pyplot(fig)

    # Visualisasi Penyewaan pada Hari Kerja vs Akhir Pekan
    working_day = df_hour.groupby(by='workingday').agg(
        avg_rentals=('cnt', 'mean'),
        total_rentals=('cnt', 'sum')
    ).reset_index()

    fig2, ax2 = plt.subplots()
    sns.barplot(x='workingday', y='avg_rentals', data=working_day, hue='workingday', palette='Blues_d', ax=ax2)
    ax2.set_title('Rata-rata Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan')
    ax2.set_xlabel('Hari Kerja (0: Akhir Pekan, 1: Hari Kerja)')
    ax2.set_ylabel('Rata-rata Penyewaan')
    ax2.set_xticklabels(['Akhir Pekan', 'Hari Kerja'])
    st.pyplot(fig2)

    weekday_hour = df_hour.groupby(by=['weekday', 'hr']).agg(
        avg_rentals=('cnt', 'mean'),
        total_rentals=('cnt', 'sum')
    ).reset_index()

    # Membuat figure untuk visualisasi rata-rata penyewaan
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hr', y='avg_rentals', hue='weekday', data=weekday_hour, marker='o', ax=ax3)
    ax3.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Jam dan Hari dalam Seminggu')
    ax3.set_xlabel('Jam dalam Sehari')
    ax3.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax3.set_xticks(range(0, 24, 1))  # Menampilkan jam 0-23
    ax3.set_xticklabels(range(0, 24, 1))
    ax3.legend(title='Hari dalam Seminggu', labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    st.pyplot(fig3)

    temperature = df_hour.groupby(pd.cut(df_hour['temp'], bins=10)).agg(avg_rentals=('cnt', 'mean')).reset_index()

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='temp', y='avg_rentals', data=temperature, hue='temp', palette='Reds', ax=ax4)
    ax4.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Suhu')
    ax4.set_xlabel('Rentang Suhu')
    ax4.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax4.set_xticklabels([f'{round(b.left * 41, 2)}°C - {round(b.right * 41, 2)}°C' for b in temperature['temp'].cat.categories], rotation=45)
    st.pyplot(fig4)




# Tampilan untuk Advanced Analysis
elif pilihan == 'Advanced Analysis':
    st.header('Advanced Analysis')

    
    st.subheader('Clustering Berbasis Waktu')
    df_hour['time_cluster'] = pd.cut(df_hour['hr'], 
                                      bins=[-1, 6, 12, 15, 18, 24], 
                                      labels=['Dini hari', 'Pagi', 'Siang', 'Sore', 'Malam'])

    
    cluster = df_hour.groupby(by=['time_cluster', 'workingday']).agg(
    avg_rentals=('cnt', 'mean'),
    total_rentals=('cnt', 'sum')
    ).reset_index()

    
    fig3, ax3 = plt.subplots()
    sns.barplot(x='time_cluster', y='avg_rentals', data=cluster, hue='workingday',palette='Set2', ax=ax3)
    ax3.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Waktu')
    ax3.set_xlabel('Waktu (Malam, Pagi, Siang, Sore)')
    ax3.set_ylabel('Rata-rata Penyewaan Sepeda')
    st.pyplot(fig3)

    
    st.write("Total Penyewaan berdasarkan Waktu Cluster:")
    st.write(cluster)
