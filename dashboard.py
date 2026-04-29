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
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

df_day['year'] = df_day['dteday'].dt.year
df_hour['year'] = df_hour['dteday'].dt.year

df_day['month'] = df_day['dteday'].dt.month_name()
df_hour['month'] = df_hour['dteday'].dt.month_name()

df_day['day_name'] = df_day['dteday'].dt.day_name()
df_hour['day_name'] = df_hour['dteday'].dt.day_name()

# ========================
# SIDEBAR FILTER
# ========================
st.sidebar.header("🔎 Filter")

# tanggal
min_date = df_day['dteday'].min()
max_date = df_day['dteday'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# bulan
month_order = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
]

month_option = st.sidebar.multiselect(
    "Pilih Bulan",
    month_order,
    default=month_order
)

# hari
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

day_option = st.sidebar.multiselect(
    "Pilih Hari",
    day_order,
    default=day_order
)

# tahun
year_option = st.sidebar.multiselect(
    "Pilih Tahun",
    sorted(df_day['year'].unique()),
    default=sorted(df_day['year'].unique())
)

# ========================
# APPLY FILTER
# ========================
df_day_filter = df_day.copy()
df_hour_filter = df_hour.copy()

# filter tanggal
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range)
    df_day_filter = df_day_filter[
        (df_day_filter['dteday'] >= start_date) &
        (df_day_filter['dteday'] <= end_date)
    ]
    df_hour_filter = df_hour_filter[
        (df_hour_filter['dteday'] >= start_date) &
        (df_hour_filter['dteday'] <= end_date)
    ]

# filter tahun
df_day_filter = df_day_filter[df_day_filter['year'].isin(year_option)]
df_hour_filter = df_hour_filter[df_hour_filter['year'].isin(year_option)]

# filter bulan
df_day_filter = df_day_filter[df_day_filter['month'].isin(month_option)]
df_hour_filter = df_hour_filter[df_hour_filter['month'].isin(month_option)]

# filter hari
df_day_filter = df_day_filter[df_day_filter['day_name'].isin(day_option)]
df_hour_filter = df_hour_filter[df_hour_filter['day_name'].isin(day_option)]

# urutan bulan
df_day_filter['month'] = pd.Categorical(df_day_filter['month'], categories=month_order, ordered=True)
df_hour_filter['month'] = pd.Categorical(df_hour_filter['month'], categories=month_order, ordered=True)

# cek data kosong
if df_day_filter.empty or df_hour_filter.empty:
    st.warning("Data tidak tersedia untuk kombinasi filter ini.")
    st.stop()

# ========================
# TITLE
# ========================
st.title("🚴 Bike Sharing Dashboard")
st.caption("Analisis Penyewaan Sepeda 2011–2012")

st.info(f"Filter aktif: Tanggal={date_range}, Tahun={year_option}")

# ========================
# KPI
# ========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", f"{df_day_filter['cnt'].sum():,.0f}")
col2.metric("Rata-rata Harian", f"{df_day_filter['cnt'].mean():,.0f}")
col3.metric("Penyewaan Tertinggi", f"{df_day_filter['cnt'].max():,.0f}")

st.markdown("---")

# ========================
# 1. PENYEWAAN PER BULAN
# ========================
st.subheader("📈 Penyewaan per Bulan")

monthly_avg = df_day_filter.groupby('month')['cnt'].mean().sort_index()

fig1, ax1 = plt.subplots()
ax1.plot(monthly_avg.index, monthly_avg.values, marker='o')

peak_month = monthly_avg.idxmax()
peak_value = monthly_avg.max()

ax1.scatter(peak_month, peak_value, s=120)
ax1.text(peak_month, peak_value*0.92, f'{peak_value:.0f}', ha='center')

ax1.set_ylim(0, monthly_avg.max()*1.15)
ax1.set_title("Rata-rata Penyewaan per Bulan")

plt.xticks(rotation=45)
st.pyplot(fig1)

# ========================
# 2. WORKDAY VS WEEKEND
# ========================
st.subheader("📊 Working Day vs Weekend")

df_day_filter['day_type'] = df_day_filter['workingday'].replace({
    'Working Day': 'Working Day',
    'Holiday': 'Weekend/Holiday'
})

grouped = df_day_filter.groupby(['season','day_type'])['cnt'].mean().unstack()
grouped = grouped.reindex(columns=['Working Day','Weekend/Holiday'])

fig2, ax2 = plt.subplots()
grouped.plot(kind='bar', colormap='coolwarm', ax=ax2)

for c in ax2.containers:
    ax2.bar_label(c, fmt='%.0f', fontsize=8)

st.pyplot(fig2)

# ========================
# 3. JAM TERTINGGI
# ========================
st.subheader("⏰ Jam Tertinggi")

hourly_avg = df_hour_filter.groupby('hr')['cnt'].mean()

fig3, ax3 = plt.subplots()
ax3.plot(hourly_avg.index, hourly_avg.values, marker='o')

peak_hour = hourly_avg.idxmax()
peak_val = hourly_avg.max()

ax3.scatter(peak_hour, peak_val, s=120)
ax3.text(peak_hour, peak_val*0.92, f'{peak_val:.0f}', ha='center')

ax3.set_xticks(range(0,24))
ax3.set_ylim(0, hourly_avg.max()*1.15)

st.pyplot(fig3)

# ========================
# 4. PROPORSI USER
# ========================
st.subheader("👥 Proporsi Pengguna")

grouped_user = df_day_filter.groupby('season')[['casual','registered']].sum()
prop = grouped_user.div(grouped_user.sum(axis=1), axis=0)

fig4, ax4 = plt.subplots()
prop.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax4)

for c in ax4.containers:
    ax4.bar_label(c, fmt='%.2f', label_type='center', fontsize=8)

st.pyplot(fig4)

# ========================
# 5. DAMPAK CUACA
# ========================
st.subheader("🌧️ Dampak Cuaca")

avg_weather = df_day_filter.groupby('weathersit')['cnt'].mean()

clear = avg_weather.get(1, 0)
bad = avg_weather.loc[avg_weather.index.isin([3,4])].mean()

comparison = pd.DataFrame({
    'Kategori': ['Cerah', 'Buruk'],
    'Rata-rata': [clear, bad]
})

fig5, ax5 = plt.subplots()
bars = ax5.bar(comparison['Kategori'], comparison['Rata-rata'])

for bar in bars:
    y = bar.get_height()
    ax5.text(bar.get_x()+bar.get_width()/2, y, f'{y:.0f}', ha='center')

st.pyplot(fig5)

if clear != 0:
    drop_pct = (clear - bad)/clear * 100
    st.metric("Penurunan saat cuaca buruk", f"{drop_pct:.2f}%")

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("Dashboard by Hasna 🚀")
