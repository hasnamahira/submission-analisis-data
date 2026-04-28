
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat data yang sudah disimpan
@st.cache_data
def load_data():
    df_day = pd.read_csv('day_clean.csv')
    df_hour = pd.read_csv('hour_clean.csv')
    return df_day, df_hour

df_day, df_hour = load_data()

# Judul Dashboard
st.title('Bike Sharing Dashboard')

st.write("Selamat datang di dashboard analisis data penyewaan sepeda!")

# Tambahkan elemen-elemen dashboard lainnya di sini
# Contoh: Visualisasi, Insight, Rekomendasi

st.header("Rata-rata Penyewaan Sepeda per Bulan (2011)")
# Kode visualisasi dari pertanyaan 3
df_2011 = df_day[df_day['yr'] == 2011]
monthly_avg = df_2011.groupby('mnth')['cnt'].mean()
peak_month = monthly_avg.idxmax()

fig_monthly_avg, ax = plt.subplots(figsize=(8, 5))
ax.plot(monthly_avg.index, monthly_avg.values, marker='o')
ax.scatter(peak_month, monthly_avg.loc[peak_month], s=100)
ax.text(peak_month, monthly_avg.loc[peak_month] + 50,
         f'{monthly_avg.loc[peak_month]:.0f}',
         ha='center', va='bottom', fontsize=9)
ax.set_title('Rata-rata Penyewaan Sepeda per Bulan (2011)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata cnt')
st.pyplot(fig_monthly_avg)

st.write(f"Insight: Rata-rata penyewaan sepeda tertinggi pada tahun 2011 terjadi pada bulan {peak_month} sekitar {monthly_avg.loc[peak_month]:.0f}.")

st.header("Rata-rata Penyewaan: Working Day vs Weekend per Season")
# Kode visualisasi dari pertanyaan 2
df_day['day_type'] = df_day['workingday'].replace({'Holiday': 'Weekend/Holiday'})
grouped_season = df_day.groupby(['season', 'day_type'], observed=False)['cnt'].mean().unstack()

fig_season, ax_season = plt.subplots()
grouped_season.plot(kind='bar', colormap='coolwarm', ax=ax_season)
ax_season.set_ylim(0, grouped_season.values.max() * 1.1)

for container in ax_season.containers:
    ax_season.bar_label(container, fmt='%.0f', label_type='edge', fontsize=8)

ax_season.legend(fontsize=8, title_fontsize=9)
ax_season.set_title('Rata-rata Penyewaan: Working Day vs Weekend per Season')
ax_season.set_xlabel('Season')
ax_season.set_ylabel('Rata-rata cnt')
ax_season.tick_params(axis='x', rotation=45)
st.pyplot(fig_season)

st.write("Insight: Pada musim gugur (Fall), rata-rata penyewaan sepeda adalah yang tertinggi secara keseluruhan, baik pada hari kerja maupun akhir pekan/hari libur. Pada musim semi (Springer), gugur (Fall), dan dingin (Winter), rata-rata penyewaan sepeda pada hari kerja lebih tinggi dibandingkan akhir pekan/hari libur. Namun, pada musim panas (Summer), rata-rata penyewaan sepeda pada akhir pekan/hari libur sedikit lebih tinggi dibandingkan hari kerja.")

st.header("Jam Puncak Penyewaan Sepeda per Bulan (2011 vs 2012)")
# Kode visualisasi dari pertanyaan 4
df_hour_2yr = df_hour[df_hour['yr'].isin([2011, 2012])].copy()
grouped_hour = df_hour_2yr.groupby(['yr', 'mnth', 'hr'])['cnt'].mean().reset_index()
peak_hour = grouped_hour.loc[grouped_hour.groupby(['yr', 'mnth'])['cnt'].idxmax()]

fig_peak_hour, ax_peak_hour = plt.subplots(figsize=(10,6))
for year in [2011, 2012]:
    data = peak_hour[peak_hour['yr'] == year]
    ax_peak_hour.plot(data['mnth'], data['hr'], marker='o', label=str(year))
    for i in range(len(data)):
        x = data['mnth'].iloc[i]
        y = data['hr'].iloc[i]
        ax_peak_hour.text(x, y + 0.3, f'{int(y)}', ha='center', fontsize=8)

ax_peak_hour.set_title('Jam Puncak Penyewaan Sepeda per Bulan (2011 vs 2012)')
ax_peak_hour.set_xlabel('Bulan')
ax_peak_hour.set_ylabel('Jam Puncak')
ax_peak_hour.set_xticks(range(1,13))
ax_peak_hour.set_yticks(range(0,24))
ax_peak_hour.legend(title='Tahun')
st.pyplot(fig_peak_hour)

st.write("Insight: Jam 17:00 (5 sore) merupakan waktu puncak penyewaan sepeda tertinggi di setiap bulan selama tahun 2011 dan 2012.")

st.header("Proporsi Casual vs Registered per Season")
# Kode visualisasi dari pertanyaan 5
grouped_casual_registered = df_day.groupby('season')[['casual', 'registered']].sum()
prop = grouped_casual_registered.div(grouped_casual_registered.sum(axis=1), axis=0)

fig_prop, ax_prop = plt.subplots(figsize=(8,5))
prop.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax_prop)

for container in ax_prop.containers:
    ax_prop.bar_label(container, fmt='%.1f', label_type='center', fontsize=15)

ax_prop.legend(title='User Type', fontsize=8, title_fontsize=9, loc='upper right')
ax_prop.set_title('Proporsi Casual vs Registered per Season')
ax_prop.set_xlabel('Season')
ax_prop.set_ylabel('Proporsi')
ax_prop.tick_params(axis='x', rotation=0)
st.pyplot(fig_prop)

st.write("Insight: Pengguna terdaftar mendominasi total penyewaan sepeda di semua musim. Proporsi pengguna casual relatif lebih tinggi pada musim panas (Summer) dan gugur (Fall). Sementara itu, pada musim semi (Springer) dan dingin (Winter), proporsi pengguna casual lebih rendah.")

st.header("Penurunan Penyewaan pada Cuaca Buruk")
# Kode visualisasi dari pertanyaan 6
df_weather = df_day[df_day['yr'].isin([2011, 2012])]
avg_weather = df_weather.groupby('weathersit')['cnt'].mean()

clear = avg_weather.loc['Clear']
bad = avg_weather.loc[['Light Rain/Snow', 'Heavy Rain/Snow']].mean()

comparison = pd.DataFrame({
    'Kategori': ['Cerah (1)', 'Buruk (3-4)'],
    'Rata-rata': [clear, bad]
})

fig_weather, ax_weather = plt.subplots(figsize=(7,5))
bars = ax_weather.bar(comparison['Kategori'], comparison['Rata-rata'])

for bar in bars:
    y = bar.get_height()
    ax_weather.text(bar.get_x() + bar.get_width()/2, y,
             f'{y:.0f}', ha='center', va='bottom', fontsize=9)

ax_weather.set_title(f'Penurunan Penyewaan pada Cuaca')
ax_weather.set_ylabel('Rata-rata cnt')
st.pyplot(fig_weather)

st.write("Insight: Rata-rata jumlah penyewaan sepeda mengalami penurunan signifikan pada kondisi cuaca buruk dibandingkan dengan kondisi cuaca cerah. Hal ini menunjukkan penurunan sebesar kurang lebih 63% pada kondisi cuaca buruk dibandingkan cuaca cerah.")
