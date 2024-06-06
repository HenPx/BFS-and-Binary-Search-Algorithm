#pip install streamlit
#pip install mysql-connector-python
#pip install streamlit-option-menu

import streamlit as st
import mysql.connector
from mysql.connector import Error
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from streamlit_option_menu import option_menu

# Fungsi untuk menghubungkan ke database MySQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='fpdaa',
            username='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

def binary_search(products, target):
    low, high = 0, len(products) - 1
    result_indices = []

    while low <= high:
        # pembulatan kebawah
        mid = (low + high) // 2
        current_product = products[mid]

        if current_product[2] == target:  # Mencocokkan dengan namaBarang
            # Mengumpulkan semua indeks yang sesuai
            result_indices.append(mid)

            # Mengecek apakah ada elemen yang sama di kiri
            left = mid - 1
            while left >= 0 and products[left][2] == target:
                result_indices.append(left)
                left -= 1

            # Mengecek apakah ada elemen yang sama di kanan
            right = mid + 1
            while right < len(products) and products[right][2] == target:
                result_indices.append(right)
                right += 1

            # mengirimkan hasil
            return result_indices
        elif current_product[2] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result_indices  # Tidak ada hasil yang sesuai

def search_product(nama_produk):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            #urutkan berdasarkan nama barang
            query = "SELECT * FROM product ORDER BY namaBarang ASC"
            cursor.execute(query)
            results = cursor.fetchall()

            # Melakukan binary search di data yang sudah diurutkan
            indices = binary_search(results, nama_produk)

            if indices:
                # Menampilkan semua hasil pencarian dalam tabel
                st.table([results[i] for i in indices])
            else:
                st.warning("Nama produk salah atau tidak ditemukan.")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def cari_product():
    st.title("Cari Produk")
    # Formulir input pencarian produk
    nama_produk = st.text_input("Nama Produk:")
    
    # Tombol untuk menjalankan pencarian
    if st.button("Cari"):
        search_product(nama_produk)

def odd_even_sort(arr, column, order):
    n = len(arr)
    sorted = False

    while not sorted:
        sorted = True
        # Ganjil
        for i in range(1, n-1, 2):
            if (order == "ascending" and arr[i][column] > arr[i+1][column]) \
                or (order == "descending" and arr[i][column] < arr[i+1][column]):
                arr[i], arr[i+1] = arr[i+1], arr[i]
                sorted = False

        # Genap
        for i in range(0, n-1, 2):
            if (order == "ascending" and arr[i][column] > arr[i+1][column]) \
                or (order == "descending" and arr[i][column] < arr[i+1][column]):
                arr[i], arr[i+1] = arr[i+1], arr[i]
                sorted = False

    return arr

def sorting_product():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM product"
            cursor.execute(query)
            results = cursor.fetchall()

            # Menampilkan semua produk sebelum diurutkan
            st.header("Produk Sebelum Diurutkan")
            st.write("Keterangan Header: ")
            st.text("0 = Nama Pemilik\n1 = Kategori Barang\n2 = Nama Barang\n3 = Tahun Produksi\n4 = Warna\n5 = Harga\n6 = Deskripsi")
            st.table(results)

            # Pilihan kolom dan urutan pengurutan
            column_options = ["namaPemilik", "kategori", "namaBarang", "tahun", "warna", "harga"]
            selected_column = st.selectbox("Pilih Kolom untuk Pengurutan", column_options)
            order_options = ["Ascending", "Descending"]
            selected_order = st.radio("Pilih Urutan Pengurutan", order_options)

            # Menggunakan odd-even Sort untuk mengurutkan produk
            sorted_results = odd_even_sort(results, column=column_options.index(selected_column), order=selected_order.lower())

            # Menampilkan produk setelah diurutkan
            st.header("Produk Setelah Diurutkan")
            st.write("Keterangan Header: ")
            st.text("0 = Nama Pemilik\n1 = Kategori Barang\n2 = Nama Barang\n3 = Tahun Produksi\n4 = Warna\n5 = Harga\n6 = Deskripsi")
            st.table(sorted_results)

        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def is_product_exists(connection, nama_pemilik, kategori, nama_barang):
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM product WHERE namaPemilik = %s AND kategori = %s AND namaBarang = %s"
        cursor.execute(query, (nama_pemilik, kategori, nama_barang))
        result = cursor.fetchone()[0]
        return result > 0
    except Error as e:
        st.error(f"Error: {e}")
        return False
    finally:
        cursor.close()

def tambah_product():
    st.title("Tambah Produk")
    # Formulir input produk
    nama_pemilik = st.text_input("Nama Pemilik")
    kategori = st.selectbox("Kategori", ["Elektronik", "Fashion", "Kecantikan", "Dekorasi Rumah", "Buku", "Mainan", "Outdoor", "Alat Dapur", "Olahraga", "Perabotan", "Gadget", "Kesehatan", "Pakaian", "Fitness"])
    nama_barang = st.text_input("Nama Barang")
    tahun = st.number_input("Tahun", min_value=0)
    warna = st.text_input("Warna")
    harga = st.number_input("Harga", min_value=0)
    deskripsi = st.text_area("Deskripsi")
    
    # Tombol untuk menambah produk
    if st.button("Tambah Produk"):
        # Mengecek apakah semua field telah diisi
        if not (nama_pemilik and kategori and nama_barang and tahun and warna and harga and deskripsi):
            st.warning("Semua field harus diisi!")
            return
        
        # Mengecek apakah produk sudah ada dalam database
        connection = create_connection()
        if connection:
            if is_product_exists(connection, nama_pemilik, kategori, nama_barang):
                st.warning("Produk dengan nama pemilik, kategori, dan nama barang yang sama sudah ada!")
            else:
                try:
                    cursor = connection.cursor()
                    # Query untuk menambahkan produk ke database
                    query = "INSERT INTO product (namaPemilik, kategori, namaBarang, tahun, warna, harga, deskripsi) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    data = (nama_pemilik, kategori, nama_barang, tahun, warna, harga, deskripsi)
                    cursor.execute(query, data)
                    connection.commit()
                    st.success("Produk berhasil ditambahkan!")
                except Error as e:
                    st.error(f"Error: {e}")
                finally:
                    cursor.close()
                    connection.close()
        if st.button("Tambah Produk Lainnya"):
            st.experimental_rerun()

def generate_random_graph(num_nodes, num_edges):
    graph = nx.gnm_random_graph(num_nodes, num_edges)
    return graph
    
def bfs_order(graph, start_node=0):
    queue = Queue()
    visited = set()
    order = []

    queue.put(start_node)
    visited.add(start_node)
    order.append(start_node)

    while not queue.empty():
        current_node = queue.get()
        temp_order = []

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                temp_order.append(neighbor)
                visited.add(neighbor)

        temp_order.sort()
        order.extend(temp_order)
        for neighbor in temp_order:
            queue.put(neighbor)  # Tambahkan tetangga yang menjadi queue selanjutnya
    return order

def mini_games():
    st.title("Mini Games: Urutan Node dengan BFS")
    num_nodes = st.slider("Jumlah Nodes", min_value=5, max_value=20, value=7)
    num_edges = st.slider("Jumlah Edges", min_value=5, max_value=30, value=10)
    # Initialize user_answer and order in st.session_state
    if 'order' not in st.session_state:
        st.session_state.order = None
    
    st.subheader("Pertanyaan:")
    st.write("Urutkan node dari node awal (0) ke node terakhir menggunakan BFS:")
    user_answer = st.text_input("Simpan Jawabanmu Disini")

    if st.button("Mulai"):
        st.button("Check jawaban")
        graph = generate_random_graph(num_nodes, num_edges)

        # Gambar graf
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black')

        st.pyplot(plt)

        # Hitung urutan menggunakan BFS
        st.session_state.order = bfs_order(graph, start_node=0)

        # Tampilkan pertanyaan
    elif st.button("Check jawaban"):
        if user_answer is "" or st.session_state.order is None:
            st.error("Silahkan mulai game.")
        else:
            order = st.session_state.order
            correct_answer = " ".join(map(str, order))

            st.write(f"{correct_answer}")
            st.write(f"{user_answer}")
            if order is not None:
                if user_answer.strip() == correct_answer:
                    st.success("Jawaban Anda benar! Selamat!")
                else:
                    st.error("Jawaban Anda salah.")
                    st.write(f"Jawaban yang benar: {correct_answer}")

if __name__ == "__main__":
    st.title("Hello")
    user_name = st.text_input("Ketik namamu disini")
    if user_name:
        st.title(f"Selamat Datang, {user_name}!")
        st.write("Ini adalah program sederhana untuk mencari produk, mengurutkan produk, dan menambahkan produk yang tersimpan di dalam database MYSQL. Namun disini kami menyediakan extra fitur yaitu Mini Game yang bisa dicoba 😎😎😎.")
    selected = option_menu(
        menu_title = None,
        options = ["Searching", "Sorting", "Adding", "Mini Game"],
        icons= ["search", "list-task","database-add", "controller"],
        orientation = "horizontal",
        styles={
            "nav-link": {"font-size": "15px", "text-align": "mid"},
        }
    )

    if selected == "Searching":
        cari_product()
    elif selected == "Sorting":
        sorting_product()
    elif selected == "Adding":
        tambah_product()
    elif selected == "Mini Game":
        mini_games()
