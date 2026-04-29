import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# CONFIG
# ========================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# ========================
# LOAD DATA
# ========================
@st.cache_data
def load_data():
    df_day = pd.read_csv('day_clean.csv')
    df_hour = pd.read_csv('hour_clean.csv')
    return df_day, df_hour

df_day, df_hour = load_data()

# ========================
# PREPROCESSING
# ========================
df_day['year'] = df_day['yr'].map({0: 2011, 1: 2012})
df_hour['year'] = df_hour['yr'].map({0: 2011, 1: 2012})

weather_map = {
    1: 'Clear',
    2: 'Mist',
    3: 'Light Rain/Snow',
    4: 'Heavy Rain/Snow'
}
df_day['weather_label'] = df_day['weathersit'].map(weather_map)

# ========================
# SIDEBAR
# ========================
st.sidebar.header("🔎 Filter")

year_option = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua", 2011, 2012]
)

if year_option == "Semua":
    df_day_filter = df_day.copy()
    df_hour_filter = df_hour.copy()
else:
    df_day_filter = df_day[df_day['year'] == year_option]
    df_hour_filter = df_hour[df_hour['year'] == year_option]

month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

df_day_filter['mnth'] = pd.Categorical(
    df_day_filter['mnth'],
    categories=month_order,
    ordered=True
)

df_hour_filter['mnth'] = pd.Categorical(
    df_hour_filter['mnth'],
    categories=month_order,
    ordered=True
)

# ========================
# TITLE
# ========================
st.title("🚴 Bike Sharing Dashboard")
st.caption("Analisis Penyewaan Sepeda Tahun 2011–2012")

# ========================
# KPI (RINGKASAN)
# ========================
col1, col2, col3 = st.columns(3)

total = df_day_filter['cnt'].sum()
avg = df_day_filter['cnt'].mean()
max_val = df_day_filter['cnt'].max()

col1.metric("Total Penyewaan", f"{total:,.0f}")
col2.metric("Rata-rata Harian", f"{avg:,.0f}")
col3.metric("Penyewaan Tertinggi", f"{max_val:,.0f}")

st.markdown("---")

# ========================
# 1. PENYEWAAN PER BULAN
# ========================
st.subheader("📈 Penyewaan per Bulan")

monthly_avg = df_day_filter.groupby('mnth')['cnt'].mean().sort_index()

if not monthly_avg.empty:
    peak_month = monthly_avg.idxmax()
    peak_value = monthly_avg.max()

    fig1, ax1 = plt.subplots(figsize=(8,5))
    ax1.plot(monthly_avg.index, monthly_avg.values, marker='o')

    ax1.scatter(peak_month, peak_value, s=120)

    ax1.text(peak_month, peak_value * 0.92,
             f'{peak_value:.0f}', ha='center', fontsize=9)

    ax1.set_ylim(0, monthly_avg.max()*1.15)

    ax1.set_title("Rata-rata Penyewaan per Bulan")
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("cnt")

    st.pyplot(fig1)
    st.success(f"Bulan tertinggi: {peak_month}")

st.markdown("---")

# ========================
# 2. WORKDAY VS WEEKEND
# ========================
st.subheader("📊 Working Day vs Weekend")

# pastikan kolom aman
df_day_filter = df_day_filter.copy()

# mapping kategori hari
df_day_filter['day_type'] = df_day_filter['workingday'].replace({
    'Working Day': 'Working Day',
    'Holiday': 'Weekend/Holiday'
})

# agregasi
grouped = df_day_filter.groupby(['season','day_type'])['cnt'].mean().unstack()

if grouped.empty:
    st.warning("Data tidak tersedia.")
else:
    fig2, ax2 = plt.subplots(figsize=(8,5))
    grouped.plot(kind='bar', colormap='coolwarm', ax=ax2)

    ax2.set_ylim(0, grouped.values.max()*1.1)

    # label nilai
    for c in ax2.containers:
        ax2.bar_label(c, fmt='%.0f', fontsize=8)

    ax2.set_title("Rata-rata Penyewaan: Working Day vs Weekend")
    ax2.set_xlabel("Season")
    ax2.set_ylabel("Rata-rata cnt")

    ax2.legend(title="Kategori Hari", fontsize=8)

    st.pyplot(fig2)
   
# ========================
# 3. CASUAL vs REGISTERED
# ========================
st.subheader("👥 Proporsi Pengguna")

grouped_user = df_day_filter.groupby('season')[['casual','registered']].sum()

if grouped_user.empty:
    st.warning("Data tidak tersedia.")
else:
    prop = grouped_user.div(grouped_user.sum(axis=1), axis=0)

    fig4, ax4 = plt.subplots(figsize=(8,5))
    prop.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax4)

    # label proporsi
    for c in ax4.containers:
        ax4.bar_label(c, fmt='%.2f', label_type='center', fontsize=8)

    ax4.set_title("Proporsi Casual vs Registered")
    ax4.set_xlabel("Season")
    ax4.set_ylabel("Proporsi")

    ax4.legend(title="User Type", fontsize=8)

    st.pyplot(fig4)

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("Dashboard by Hasna ✨")