import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

bike_data = pd.read_csv("data/all_data.csv")
bike_data['dteday'] = pd.to_datetime(bike_data['dteday'])

weekday_mapping = {
    0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 
    4: "Friday", 5: "Saturday", 6: "Sunday"
}

bike_data['weekday'] = bike_data['weekday'].map(weekday_mapping)
casual_sorted = bike_data.groupby(['season', 'weekday'])['casual'].sum().reset_index()

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.sidebar.title("Bike Sharing Dashboard")
st.sidebar.markdown("**By: Aulia Halimatusyaddiah MC319D5X2048**")
st.sidebar.caption("Copywrite 2025")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Trend Penggunaan Harian", "Hari Tertinggi", "Hari Populer", "Musim Populer", "Casual Populer"
])

with tab1:
    with st.container():
        st.subheader("Pilih Bulan dan Tahun:")
        bike_data['year_month'] = bike_data['dteday'].dt.to_period('M')
        month_options = bike_data['year_month'].dt.strftime('%Y-%m').unique()
        selected_month = st.selectbox("Pilih Bulan:", month_options)
        filtered_data = bike_data[bike_data['year_month'].astype(str) == selected_month]
    
    st.subheader(f"Penggunaan Sepeda per Hari ({selected_month})")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(data=filtered_data, x='dteday', y='casual', label='Casual', color='orange', alpha=0.5, ci=None)
    sns.lineplot(data=filtered_data, x='dteday', y='registered', label='Registered', color='yellow', alpha=0.65, ci=None)
    sns.lineplot(data=filtered_data, x='dteday', y='cnt', label='Total (cnt)', color='green', linewidth=2, ci=None)
    ax.set(title='Penggunaan Sepeda per Hari', xlabel='Tanggal', ylabel='Jumlah Pengguna Sepeda')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))  
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

with tab2:
    st.subheader("Hari dengan Penggunaan Sepeda Terbanyak")
    base_on_date = bike_data.sort_values(by='cnt', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=base_on_date, x='dteday', y='cnt', color='green', label='Total (cnt)')
    sns.barplot(data=base_on_date, x='dteday', y='registered', color='yellow', label='Registered')
    sns.barplot(data=base_on_date, x='dteday', y='casual', color='orange', label='Casual')
    ax.set_title("Hari dengan Penggunaan Sepeda Tertinggi", fontsize=14)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Pengguna Sepeda")
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)

with tab3:
    st.subheader("Penggunaan Sepeda Berdasarkan Hari Kerja dan Libur")
    bike_usage = bike_data.groupby(['weekday', 'workingday', 'holiday'])[['cnt', 'casual', 'registered']].sum().reset_index()
    bike_usage_melted = bike_usage.melt(id_vars=['weekday', 'workingday', 'holiday'], value_vars=['cnt', 'casual', 'registered'], var_name='Type', value_name='Total')
    
    palette = {'cnt': 'green', 'casual': 'orange', 'registered': 'yellow'}
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    sns.barplot(data=bike_usage_melted, x='weekday', y='Total', hue='Type', palette=palette, ax=axes[0], ci=None)
    axes[0].set(title='Berdasarkan Weekday', xlabel='Weekday', ylabel='Jumlah Pengguna')
    axes[0].tick_params(axis='x', rotation=45)
    sns.barplot(data=bike_usage_melted, x='workingday', y='Total', hue='Type', palette=palette, ax=axes[1], ci=None)
    axes[1].set(title='Berdasarkan Workingday', xlabel='Workingday')
    sns.barplot(data=bike_usage_melted, x='holiday', y='Total', hue='Type', palette=palette, ax=axes[2], ci=None)
    axes[2].set(title='Berdasarkan Holiday', xlabel='Holiday')
    plt.tight_layout()
    st.pyplot(fig)

with tab4:
    st.subheader("Persebaran Penggunaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x=bike_data["season"], y=bike_data["cnt"], palette="coolwarm", ax=ax)
    ax.set(title="Persebaran Penggunaan Sepeda Berdasarkan Musim", xlabel="Musim", ylabel="Jumlah Pengguna Sepeda")
    st.pyplot(fig)

with tab5:
    st.subheader("Penggunaan Sepeda Casual Berdasarkan Hari dan Musim")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=casual_sorted, x="weekday", y="casual", hue="season", palette="Set2", ci=None, ax=ax)
    ax.set(title="Penggunaan Sepeda Casual Berdasarkan Hari dan Musim", xlabel="Weekday", ylabel="Jumlah Pengguna Casual")
    ax.legend(title="Season", loc="upper right")
    st.pyplot(fig)
