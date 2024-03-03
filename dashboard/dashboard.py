import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the dashboard
st.title('Bike Sharing Analysis Dashboard 🚴🏻‍♂️')

# Biodata Section
st.subheader('Biodata Diri:')
st.write('Nama: Auvarifqi Putra Diandra')
st.write('Email: m002d4ky2877@bangkit.academy')
st.write('ID Dicoding: auvarifqi')

# Load data
df_hour = pd.read_csv('cleaned_bikeshare_hour.csv')


# Visualisasi rata-rata penyewaan sepeda berdasarkan tahun dan musim
st.subheader('1. Average Bike Rental Count by Season and Year')
avg_rentals = df_hour.groupby(['yr', 'season'])['cnt'].mean().unstack()
st.bar_chart(avg_rentals)
# Insight Section 1
st.subheader('Insights 1:')
st.write('Rata-rata penyewaan sepeda pada tahun 2011 lebih rendah daripada tahun 2012. Selain itu musim yang paling banyak penyewaan sepeda adalah musim Summer dan yang paling rendah adalah musim Winter. Hal ini sesuai dengan ekspektasi karena musim Summer adalah musim liburan dan musim Winter adalah musim dingin yang membuat orang enggan untuk bersepeda.')

# Visualisasi rata-rata penyewaan sepeda pada hari libur dan non-hari libur
st.subheader('2. Average Bike Rental Count on Holidays and Non-Holidays')
avg_rentals_holiday = df_hour.groupby('holiday')['cnt'].mean()
st.bar_chart(avg_rentals_holiday)
# Insight Section 2
st.subheader('Insights 2:')
st.write('Rata-rata penyewaan sepeda juga dipengaruhi dengan kegiatan orang-orang pada hari itu, dan hasilnya menunjukkan bahwa ketika non holiday penyewaan sepeda memiliki nilai yang lebih tinggi jika dibandingkan dengan ketika liburan. Hal ini mungkin terjadi karena jumlah hari ketika liburan itulebih sedikit daripada jumlah hari saat tidak liburan')

# Visualisasi jumlah total penyewaan sepeda berdasarkan jam
st.subheader('3. Count of bikeshare rides by hour')
hourly_users_df = df_hour.groupby("hr").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
}).reset_index()
# Set the style
sns.set_style("whitegrid")
# Create a figure and axis object
plt.figure(figsize=(16, 6))
# Plot casual users
sns.lineplot(x=hourly_users_df["hr"], y=hourly_users_df["casual"], label='Casual', color='blue')
# Plot registered users
sns.lineplot(x=hourly_users_df["hr"], y=hourly_users_df["registered"], label='Registered', color='orange')
# Add labels and a title to the plot
plt.xlabel("Hour")
plt.ylabel("Total Rides")
plt.title("Count of bikeshare rides by hour")
# Set ticks for x-axis
x_ticks = np.arange(0, 24, 1)
plt.xticks(x_ticks)

# Highlight the important data label in the chart
plt.axvline(x=8, color='gray', linestyle='--')
plt.axvline(x=17, color='gray', linestyle='--')
# Add a legend to the plot
plt.legend(loc='upper right', fontsize=14)

# Show the plot using Streamlit
st.pyplot(plt)

# Insight Section 3
st.subheader('Insights 3:')
st.write('Dari grafik di atas, kita dapat melihat bahwa jumlah penyewaan sepeda paling tinggi terjadi pada jam 8 pagi dan jam 5 sore. Hal ini mungkin terjadi karena pada jam-jam tersebut orang-orang sedang berangkat kerja atau pulang kerja. Selain itu, jumlah penyewaan sepeda paling rendah terjadi pada jam 3 pagi, hal ini mungkin terjadi karena pada jam tersebut orang-orang sedang tidur.')

#RFM Analysis
st.subheader('4. RFM Analysis')
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
# Calculate Recency, Frequency, and Monetary Value
max_date = df_hour['dteday'].max()
rfm_df = df_hour.groupby('instant').agg({
    'dteday': lambda x: (max_date - x.max()).days,  # Recency
    'cnt': ['count', 'sum']  # Frequency, Monetary Value
})
rfm_df.columns = ['Recency', 'Frequency', 'Monetary']

# Streamlit UI
st.title('RFM Analysis Dashboard')
st.write("## RFM DataFrame")
st.write(rfm_df.head())

st.write("## RFM Distributions")
# Plot Recency Distribution
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.hist(rfm_df['Recency'], bins=20, color='skyblue', edgecolor='black')
plt.title('Recency Distribution', fontsize=16)
plt.xlabel('Recency', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Plot Frequency Distribution
plt.subplot(1, 3, 2)
plt.hist(rfm_df['Frequency'], bins=20, color='lightgreen', edgecolor='black')
plt.title('Frequency Distribution', fontsize=16)
plt.xlabel('Frequency', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Plot Monetary Distribution
plt.subplot(1, 3, 3)
plt.hist(rfm_df['Monetary'], bins=20, color='salmon', edgecolor='black')
plt.title('Monetary Distribution', fontsize=16)
plt.xlabel('Monetary', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

st.pyplot(plt)

st.subheader('Conclusion:')
st.write('''
Pola Penyewaan Sepeda Berdasarkan Musim atau Tahun:
Ditemukan bahwa ada pola yang jelas dalam penyewaan sepeda berdasarkan musim dan tahun.
- Penyewaan sepeda cenderung meningkat selama musim panas dan musim semi, sementara cenderung menurun selama musim dingin.
- Tahun juga memengaruhi pola penyewaan, dengan tren peningkatan yang terlihat dari tahun ke tahun.
- Langkah selanjutnya dapat meliputi:
    Menyiapkan strategi pemasaran yang lebih agresif selama musim panas dan musim semi untuk menarik lebih banyak penyewa.
    Mengantisipasi permintaan yang lebih tinggi selama musim panas dengan meningkatkan persediaan sepeda.
    
2. Pengaruh Hari Libur Terhadap Tingkat Penyewaan Sepeda:
- Hari libur memiliki pengaruh yang signifikan terhadap tingkat penyewaan sepeda.
- Penyewaan sepeda cenderung meningkat pada hari-hari libur dibandingkan dengan hari-hari biasa.
- Langkah selanjutnya dapat meliputi:
    Menyiapkan strategi khusus untuk memanfaatkan hari libur dengan menawarkan promosi atau acara khusus yang sesuai dengan tema hari libur.
    Memperluas layanan atau menambah persediaan sepeda selama hari libur untuk memenuhi permintaan yang lebih tinggi.
    
3. Pola Penggunaan Sewa Sepeda Berdasarkan Jam Penggunaannya Sehari-hari:
- Ditemukan pola penggunaan sewa sepeda yang bervariasi berdasarkan jam penggunaannya sehari-hari.
- Penyewaan sepeda cenderung meningkat pada pagi hari dan sore hari, kemungkinan karena penggunaan untuk berangkat dan pulang dari tempat kerja atau sekolah.
- Tren ini menunjukkan potensi untuk menyesuaikan operasi dan layanan penyewaan untuk memenuhi permintaan yang lebih tinggi selama jam-jam sibuk.
- Langkah selanjutnya dapat meliputi:
    Menerapkan strategi harga dinamis yang meningkatkan harga selama jam-jam sibuk untuk meningkatkan pendapatan.
    Menambah persediaan sepeda di stasiun-stasiun yang sering digunakan selama jam-jam sibuk.
    Dengan menganalisis pola-pola ini dan mengambil langkah-langkah yang sesuai, perusahaan penyewaan sepeda dapat meningkatkan kinerja operasional dan meningkatkan kepuasan pelanggan.''')