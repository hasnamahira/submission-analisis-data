import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
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
# DATA
# ========================
# Mapping tahun
df_day['year'] = df_day['yr'].map({0: 2011, 1: 2012})
df_hour['year'] = df_hour['yr'].map({0: 2011, 1: 2012})

# Mapping cuaca
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
st.sidebar.header("Filter")

year_option = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua", 2011, 2012]
)

if year_option == "Semua":
    df_day_filter = df_day.copy()
else:
    df_day_filter = df_day[df_day['year'] == year_option]

# ========================
# TITLE
# ========================
st.title("🚴 Bike Sharing Dashboard")
st.write("Dashboard analisis penyewaan sepeda 2011-2012")

# ========================
# 1. BULAN TERBAIK
# ========================
st.subheader("📈 Penyewaan per Bulan")

# Urutan bulan
month_order = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

df_day_filter = df_day_filter.copy()

df_day_filter['mnth'] = pd.Categorical(
    df_day_filter['mnth'],
    categories=month_order,
    ordered=True
)

monthly_avg = df_day_filter.groupby('mnth')['cnt'].mean().sort_index()

if not monthly_avg.empty:
    peak_month = monthly_avg.idxmax()

    fig1, ax1 = plt.subplots(figsize=(8,5))
    ax1.plot(monthly_avg.index, monthly_avg.values, marker='o')

    y = monthly_avg.loc[peak_month]
    ax1.scatter(peak_month, y, s=100)

    ax1.text(peak_month, y - y*0.92,
             f'{y:.0f}', ha='center', va='top', fontsize=9)

    ax1.set_ylim(0, monthly_avg.max()*1.15)

    ax1.set_title("Rata-rata Penyewaan per Bulan")
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("cnt")

    plt.xticks(rotation=45)

    st.pyplot(fig1)
    st.success(f"Bulan tertinggi: {peak_month}")

# ========================
# 2. WORKDAY VS WEEKEND
# ========================
st.subheader("📊 Working Day vs Weekend")

df_day_filter['day_type'] = df_day_filter['workingday'].replace({
    'Holiday': 'Weekend/Holiday'
})

grouped = df_day_filter.groupby(['season','day_type'])['cnt'].mean().unstack()

fig2, ax2 = plt.subplots()
grouped.plot(kind='bar', colormap='coolwarm', ax=ax2)

ax2.set_ylim(0, grouped.values.max()*1.1)

for c in ax2.containers:
    ax2.bar_label(c, fmt='%.0f', fontsize=8)

st.pyplot(fig2)

# ========================
# 3. JAM PUNCAK
# ========================
st.subheader("⏰ Jam Puncak")

grouped_hour = df_hour.groupby(['year','mnth','hr'])['cnt'].mean().reset_index()
peak_hour = grouped_hour.loc[grouped_hour.groupby(['year','mnth'])['cnt'].idxmax()]

fig3, ax3 = plt.subplots()

for year in [2011, 2012]:
    data = peak_hour[peak_hour['year'] == year]
    ax3.plot(data['mnth'], data['hr'], marker='o', label=str(year))

ax3.legend()
ax3.set_title("Jam Puncak per Bulan")
ax3.set_xlabel("Bulan")
ax3.set_ylabel("Jam")

st.pyplot(fig3)

# ========================
# 4. CASUAL vs REGISTERED
# ========================
st.subheader("👥 Proporsi Pengguna")

grouped_user = df_day.groupby('season')[['casual','registered']].sum()
prop = grouped_user.div(grouped_user.sum(axis=1), axis=0)

fig4, ax4 = plt.subplots()
prop.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax4)

for c in ax4.containers:
    ax4.bar_label(c, fmt='%.1f', label_type='center', fontsize=8)

st.pyplot(fig4)

# ========================
# 5. CUACA
# ========================
st.subheader("🌧️ Dampak Cuaca")

avg_weather = df_day.groupby('weather_label')['cnt'].mean()

# AMAN (tidak error)
clear = avg_weather.get('Clear', 0)
bad = avg_weather.loc[
    avg_weather.index.isin(['Light Rain/Snow','Heavy Rain/Snow'])
].mean()

comparison = pd.DataFrame({
    'Kategori': ['Cerah', 'Buruk'],
    'Rata-rata': [clear, bad]
})

fig5, ax5 = plt.subplots()
bars = ax5.bar(comparison['Kategori'], comparison['Rata-rata'])

for bar in bars:
    y = bar.get_height()
    ax5.text(bar.get_x()+bar.get_width()/2, y,
             f'{y:.0f}', ha='center')

st.pyplot(fig5)

# Hitung penurunan aman
if clear != 0:
    drop_pct = (clear - bad)/clear * 100
    st.warning(f"Penurunan: {drop_pct:.2f}%")

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("Dashboard by Hasna 🚀")
