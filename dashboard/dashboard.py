import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')

# Fungsi untuk memuat dataset dengan cache untuk mengurangi waktu load
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

#membuat fungsi untuk review score
def create_review_distribution(df):
    if "review_score" not in df.columns:
        raise ValueError("Kolom 'review_score' tidak ditemukan di DataFrame.")
    
    # Menghitung distribusi review berdasarkan skor
    review_distribution = df["review_score"].value_counts(normalize=True).reset_index()
    review_distribution.columns = ["review_score", "proportion"]
    return review_distribution

# Fungsi untuk membuat daily orders DataFrame
def create_daily_orders_df(df):
    if df.index.name != "order_purchase_timestamp":
        raise ValueError("Index DataFrame harus 'order_purchase_timestamp' untuk resample.")
    
    daily_orders_df = df.resample(rule='D').agg({
        "order_id": "nunique",    # Jumlah pesanan unik
        "price": "sum"           # Total harga
    }).reset_index()

    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_orders_df

# Fungsi untuk menghitung total item per kategori
def create_sum_order_item_df(df):
    if "product_category_name" not in df.columns or "product_id" not in df.columns:
        raise ValueError("Kolom 'product_category_name' atau 'product_id' tidak ditemukan di DataFrame.")
    
    # Mengelompokkan data berdasarkan kategori produk dan menghitung jumlah product_id
    sum_order_items_df = df.groupby("product_category_name")["product_id"].count().sort_values(ascending=False).reset_index()
    sum_order_items_df.rename(columns={"product_id": "total_quantity"}, inplace=True)
    return sum_order_items_df

# Fungsi untuk menghitung jumlah pelanggan per negara bagian
def create_bystate_df(df):
    if "customer_state" not in df.columns or "customer_id" not in df.columns:
        raise ValueError("Kolom 'customer_state' atau 'customer_id' tidak ditemukan di DataFrame.")
    
    bystate_df = df.groupby(by="customer_state")["customer_id"].nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bystate_df

# Memuat dataset
try:
    customer_dataset_df = load_data("dashboard/customers_dataset.csv")
    products_dataset_df = load_data("dashboard/products_dataset.csv") 
    order_items_dataset_df = load_data("dashboard/order_items_dataset_df.csv")
    order_dataset_df = load_data("dashboard/orders_dataset.csv")
    order_reviews_df = load_data("dashboard/order_reviews_dataset.csv")
except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e}")
    st.stop()

# menggabungkan order_item dan order
if 'order_id' in order_dataset_df.columns and 'order_id' in order_items_dataset_df.columns:
    # Menggabungkan kedua dataset
    order_combine = pd.merge(
        order_dataset_df,
        order_items_dataset_df,
        on='order_id',  # Kolom kunci yang digunakan untuk penggabungan
        how='left'      # Menggunakan join 'left'
    )
else:
    print("Kolom 'order_id' tidak ditemukan di salah satu DataFrame.")


#menggabungkan product dataset dengan tabel order
if 'product_id' in order_combine.columns and 'product_id' in products_dataset_df.columns:
    # Menggabungkan kedua dataset
    order_product_combine = pd.merge(
        order_combine,
        products_dataset_df,
        on='product_id',  # Kolom kunci yang digunakan untuk penggabungan
        how='left'      # Menggunakan join 'left'
    )
else:
    print("Kolom 'product_id' tidak ditemukan di salah satu DataFrame.")

#menggabungkan customer dataset dengan gabungan order dan product
if 'customer_id' in order_product_combine.columns and 'customer_id' in customer_dataset_df.columns:
    # Menggabungkan kedua dataset
    order_product_customer_combine = pd.merge(
        order_product_combine,
        customer_dataset_df,
        on='customer_id',  # Kolom kunci yang digunakan untuk penggabungan
        how='left'      # Menggunakan join 'left'
    )
else:
    print("Kolom 'customer_id' tidak ditemukan di salah satu DataFrame.")

# menggabungkan order_product_customer_combine dengan review
if 'order_id' in order_product_combine.columns and 'order_id' in order_reviews_df.columns:
    # Menggabungkan kedua dataset
    order_product_customer_combine = pd.merge(
        order_product_customer_combine,
        order_reviews_df,
        on='order_id',  # Kolom kunci yang digunakan untuk penggabungan
        how='left'      # Menggunakan join 'left'
    )
else:
    print("Kolom 'order_id' tidak ditemukan di salah satu DataFrame.")


# Konversi kolom datetime
order_product_customer_combine_columns = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for column in order_product_customer_combine_columns:
    if column in order_product_customer_combine.columns:
        order_product_customer_combine[column] = pd.to_datetime(order_product_customer_combine[column])

# Validasi kolom datetime
required_columns = ['order_purchase_timestamp', 'order_id', 'price']
missing_columns = [col for col in required_columns if col not in order_product_customer_combine.columns]

if missing_columns:
    st.error(f"Kolom berikut tidak ditemukan dalam DataFrame: {missing_columns}")
    st.stop()

# Mendapatkan rentang tanggal minimum dan maksimum
min_date = order_product_customer_combine['order_purchase_timestamp'].min()
max_date = order_product_customer_combine['order_purchase_timestamp'].max()

# Sidebar untuk memilih rentang waktu
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

    # Filter negara bagian
    opsi_negara_bagian = order_product_customer_combine['customer_state'].dropna().unique()
    selected_states = st.multiselect(
        label="Pilih Negara Bagian",
        options=opsi_negara_bagian,
        default=opsi_negara_bagian  # Default semua negara bagian
    )
    
    # Filter kategori produk
    opsi_kategori = order_product_customer_combine['product_category_name'].dropna().unique()
    selected_categories = st.multiselect(
        label="Pilih Kategori Produk",
        options=opsi_kategori,
        default=opsi_kategori  # Default semua kategori produk
    )

# Validasi rentang tanggal
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
if start_date < min_date or end_date > max_date:
    st.error("Tanggal rentang waktu di luar batas data. Pilih rentang waktu yang valid.")
    st.stop()

# Filter data berdasarkan rentang waktu
main_df = order_product_customer_combine[
    (order_product_customer_combine["order_purchase_timestamp"] >= start_date) &
    (order_product_customer_combine["order_purchase_timestamp"] <= end_date) &
    (order_product_customer_combine["customer_state"].isin(selected_states)) &
    (order_product_customer_combine["product_category_name"].isin(selected_categories))
]


if main_df.empty:
    st.warning("Tidak ada data untuk rentang waktu yang dipilih.")
    st.stop()

# Set kolom datetime sebagai indeks
main_df.set_index('order_purchase_timestamp', inplace=True)

# Membuat DataFrame agregasi
daily_orders_df = create_daily_orders_df(main_df)
sum_orders_items_df = create_sum_order_item_df(main_df)
bystate_df = create_bystate_df(main_df)

# membuat agregasi review score
if "review_score" in main_df.columns:
    review_distribution = create_review_distribution(main_df)
else:
    st.warning("Kolom 'review_score' tidak ditemukan dalam dataset.")
    review_distribution = None

# Header dan visualisasi dashboard
st.header('Dashboard Data')

# Visualisasi by state
st.subheader("Orders by State")
fig, ax = plt.subplots()
sns.barplot(data=bystate_df, x="customer_state", y="customer_count", ax=ax, palette='viridis')
ax.set_title("Jumlah Pelanggan per State")
st.pyplot(fig)

# Visualisasi total produk terjual per kategori
st.subheader("Jumlah Produk Terjual per Kategori")
fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=sum_orders_items_df, x="total_quantity", y="product_category_name", ax=ax, palette='coolwarm', orient='h')
ax.set_title("Jumlah Produk Terjual per Kategori", fontsize=14)
ax.set_xlabel("Jumlah Produk", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig)

# Visualisasi daily orders
st.subheader("Daily Orders")
st.line_chart(daily_orders_df.set_index("order_purchase_timestamp")["order_count"])

# Visualisasi Order Review
if review_distribution is not None:
    st.subheader("Proporsi Review Pelanggan")
    
    fig, ax = plt.subplots()
    ax.pie(
        review_distribution["proportion"], 
        labels=review_distribution["review_score"], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=sns.color_palette("pastel")[0:len(review_distribution)]
    )
    ax.set_title("Distribusi Review Pelanggan", fontsize=14)
    st.pyplot(fig)




