import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


# Load dataset with caching
@st.cache_data
def load_data():
    # Gantilah dengan path yang sesuai untuk file dataset Anda
    data = pd.read_csv('../data/hour.csv')
    data['dteday'] = pd.to_datetime(data['dteday'])  # Pastikan kolom dteday dalam format datetime
    return data


# Load the data
data = load_data()

# Sidebar untuk memilih rentang tanggal
with st.sidebar:
    st.title("Bike Sharing Data Analysis")

    # Rentang tanggal
    min_date = data['dteday'].min()
    max_date = data['dteday'].max()

    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

# Tampilkan data yang dipilih di halaman utama
st.header(f"Bike Usage Analysis from {start_date} to {end_date}")
st.write(filtered_data)

# Analisis data berdasarkan jam penggunaan sepeda
st.subheader('Hourly Bike Usage Pattern')
st.markdown(
    "Analisis ini menunjukkan pola penggunaan sepeda berdasarkan jam dalam satu hari. Data ini membantu memahami kapan sepeda paling banyak digunakan, misalnya pada jam sibuk pagi atau sore.")
hourly_usage = filtered_data.groupby('hr')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_usage, ax=ax, marker='o', color='blue')
ax.set_title('Total Bike Usage per Hour')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Total Bike Usage')
st.pyplot(fig)

# Analisis penggunaan sepeda berdasarkan cuaca
st.subheader('Bike Usage Based on Weather Conditions')
st.markdown(
    "Analisis ini menunjukkan hubungan antara kondisi cuaca dan jumlah penggunaan sepeda. Cuaca buruk biasanya mengurangi jumlah pengguna sepeda.")
weather_usage = filtered_data.groupby('weathersit')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_usage, ax=ax, palette='coolwarm')
ax.set_title('Total Bike Usage by Weather Condition')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Total Bike Usage')
st.pyplot(fig)

# Analisis penggunaan sepeda berdasarkan hari kerja dan libur
st.subheader('Bike Usage on Workdays vs Holidays')
st.markdown(
    "Grafik ini membandingkan penggunaan sepeda pada hari kerja dan hari libur. Analisis ini berguna untuk memahami pola pengguna sepeda kasual dibandingkan pengguna terdaftar.")
day_type_usage = filtered_data.groupby('holiday')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='holiday', y='cnt', data=day_type_usage, ax=ax, palette='Set2')
ax.set_title('Total Bike Usage on Workdays vs Holidays')
ax.set_xlabel('Holiday (0 = Workday, 1 = Holiday)')
ax.set_ylabel('Total Bike Usage')
st.pyplot(fig)

# Analisis penggunaan sepeda berdasarkan suhu
st.subheader('Bike Usage vs Temperature')
st.markdown(
    "Analisis ini mengeksplorasi hubungan antara suhu udara dan jumlah pengguna sepeda. Suhu yang nyaman cenderung menarik lebih banyak pengguna.")
sns.regplot(x='temp', y='cnt', data=filtered_data, scatter_kws={'s': 10}, line_kws={'color': 'red'})
plt.title('Bike Usage vs Temperature')
plt.xlabel('Temperature')
plt.ylabel('Total Bike Usage')
st.pyplot(plt)

# Analisis hubungan antara `casual`, `registered`, dan `cnt`
st.subheader('Casual vs Registered Bike Usage')
st.markdown(
    "Analisis ini menunjukkan hubungan antara pengguna kasual (pengguna tanpa registrasi) dan pengguna terdaftar, serta bagaimana keduanya berbeda di berbagai musim.")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='casual', y='registered', data=filtered_data, hue='season', palette='Set1')
ax.set_title('Casual vs Registered Bike Usage')
ax.set_xlabel('Casual Users')
ax.set_ylabel('Registered Users')
st.pyplot(fig)

# Analisis penggunaan sepeda per musim
st.subheader('Bike Usage Across Seasons')
st.markdown(
    "Grafik ini menunjukkan total penggunaan sepeda di setiap musim, membantu memahami apakah ada musim tertentu yang mendorong lebih banyak penggunaan sepeda.")
season_usage = filtered_data.groupby('season')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_usage, ax=ax, palette='viridis')
ax.set_title('Total Bike Usage Across Seasons')
ax.set_xlabel('Season')
ax.set_ylabel('Total Bike Usage')
st.pyplot(fig)

# Menampilkan statistik deskriptif
st.subheader('Descriptive Statistics')
st.markdown(
    "Statistik deskriptif ini memberikan gambaran umum tentang data, termasuk rata-rata, nilai minimum, maksimum, dan kuartil untuk setiap kolom numerik.")
st.write(filtered_data.describe())
