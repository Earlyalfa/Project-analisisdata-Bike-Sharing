import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# 1. SET PAGE CONFIG
st.set_page_config(
    page_title="Bike Sharing Insight Pro",
    page_icon="🚲",
    layout="wide",
)

# 2. CUSTOM CSS (Mempercantik Header & Sidebar)
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        background: linear-gradient(to right, #2c3e50, #4ca1af);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    [data-testid="stMetricValue"] {
        color: #2e7d32; /* Warna hijau untuk angka utama */
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LOAD DATA
@st.cache_data
def load_data():
    try:
        # Mencari lokasi folder tempat file dashboard.py ini berada
        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, "main_data.csv")
        
        df = pd.read_csv(path)
        df['dteday'] = pd.to_datetime(df['dteday'])
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

df = load_data()

if df is not None:
    # 4. SIDEBAR
    with st.sidebar:
        st.markdown("### 🗓️ Periode Laporan")
        start_date, end_date = st.date_input(
            label='Rentang Waktu Analisis',
            min_value=df['dteday'].min(),
            max_value=df['dteday'].max(),
            value=[df['dteday'].min(), df['dteday'].max()]
        )
        st.markdown("---")
        st.markdown("### 👤 Data Analyst")
        st.success("**Early Alfa Sheilawati**")
        st.caption("ID: CDCC525D6X0093")

    main_df = df[(df['dteday'] >= str(start_date)) & (df['dteday'] <= str(end_date))]

    # 5. HEADER
    st.markdown("""
        <div class="main-header">
            <h1>🚲 BIKE SHARING DASHBOARD</h1>
            <p>Analisis Performa Berdasarkan Waktu, Cuaca, dan Hari Kerja</p>
        </div>
        """, unsafe_allow_html=True)

    # 6. METRIC CARDS
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rental", value=f"{main_df['cnt'].sum():,}")
    m2.metric("Rata-rata", value=f"{int(main_df['cnt'].mean()):,}")
    m3.metric("Max Rental", value=f"{main_df['cnt'].max():,}")
    m4.metric("Total Hari", value=len(main_df))

    st.markdown("---")

    # 7. TABS ANALISIS
    tab1, tab2 = st.tabs(["📈 Analisis Lingkungan", "🏢 Analisis Aktivitas"])

    with tab1:
        # PERTANYAAN 1: TREN (Warna Biru)
        st.subheader("Tren Sewa Sepeda Harian")
        fig, ax = plt.subplots(figsize=(16, 6))
        ax.plot(main_df['dteday'], main_df['cnt'], color='#3498db', linewidth=2)
        ax.fill_between(main_df['dteday'], main_df['cnt'], color='#3498db', alpha=0.2)
        ax.set_ylabel("Jumlah Sewa")
        st.pyplot(fig)

        col_a, col_b = st.columns(2)
        with col_a:
            # PERTANYAAN 2: CUACA (Warna Hijau-Kuning-Biru)
            st.subheader("Sewa Berdasarkan Cuaca")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="weathersit", y="cnt", data=main_df, palette="viridis", ax=ax, ci=None)
            ax.set_xlabel("Kondisi Cuaca (1:Cerah, 2:Mendung, 3:Hujan)")
            st.pyplot(fig)

        with col_b:
            # PERTANYAAN 2: MUSIM (Warna Oranye-Merah)
            st.subheader("Sewa Berdasarkan Musim")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="season", y="cnt", data=main_df, palette="YlOrRd", ax=ax, ci=None)
            ax.set_xlabel("Musim (1:Semi, 2:Panas, 3:Gugur, 4:Dingin)")
            st.pyplot(fig)

    with tab2:
        # PERTANYAAN 3: WORKING DAY (Warna Kontras Pink & Ungu)
        st.subheader("Perbandingan Hari Kerja vs Hari Libur")
        
        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown("#### Distribusi Sewa")
            fig, ax = plt.subplots(figsize=(10, 8))
            # Pakai warna kontras: Deep Pink dan Dark Slate Blue
            sns.boxplot(x="workingday", y="cnt", data=main_df, palette=["#FF69B4", "#483D8B"], ax=ax)
            ax.set_xticklabels(["Holiday/Weekend", "Working Day"])
            st.pyplot(fig)

        with col_d:
            st.markdown("#### Rata-rata Jumlah Sewa")
            fig, ax = plt.subplots(figsize=(10, 8))
            # Pakai warna kontras lainnya: Gold dan Teal
            sns.barplot(x="workingday", y="cnt", data=main_df, palette=["#FFD700", "#008080"], ax=ax, ci=None)
            ax.set_xticklabels(["Holiday/Weekend", "Working Day"])
            st.pyplot(fig)
            
        st.markdown("---")
        st.markdown("### 📝 Kesimpulan Akhir & Saran")
        c1, c2 = st.columns(2)
        with c1:
            st.success("""
            **Hasil Analisis:**
            1. Pengguna paling suka bersepeda saat **Cuaca Cerah**.
            2. Penyewaan memuncak pada **Musim Gugur**.
            3. Hari kerja memiliki total penyewa paling tinggi.
            """)
        with c2:
            st.warning("""
            **Saran untuk Bisnis:**
            - Siapkan stok sepeda lebih banyak di **Hari Kerja** jam berangkat kantor.
            - Berikan promo khusus di **Hari Libur** untuk menarik pengguna rekreasi.
            """)

    # 8. FOOTER
    st.markdown("---")
    st.caption('2026 | Early Alfa Sheilawati')

else:
    st.error("Data tidak ditemukan! Cek file main_data.csv.")