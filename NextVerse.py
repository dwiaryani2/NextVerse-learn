from ast import main
import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu
import os
import re


# Styling
st.markdown("""
    <style>
        .option-box {
            border: 2px solid #ccc;
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            cursor: pointer;
            display: flex;
            align-items: center;
        }
        .option-box:hover {
            background-color: #f1f1f1;
        }
        .selected {
            border-color: #4caf50 !important;
            background-color: #e8f5e9 !important;
        }
        .custom-image {
            margin-top: 50px;  /* Sesuaikan nilai untuk posisi gambar */
        }
        .title-section {
        text-align: left;
        }
        .content-section {
        text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi session state untuk login/signup
if "user_authenticated" not in st.session_state:
    st.session_state["user_authenticated"] = False

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Login"

# Path ke database pengguna
user_db_path = "users.pkl"

# Fungsi untuk memuat database pengguna
def load_users():
    if os.path.exists(user_db_path):
        with open(user_db_path, "rb") as f:
            return pickle.load(f)
    return {}

# Fungsi untuk menyimpan database pengguna
def save_users(users):
    with open(user_db_path, "wb") as f:
        pickle.dump(users, f)

# Load database pengguna
users = load_users()

# Fungsi untuk memeriksa kredensial
def authenticate(username, password):
    if username in users:
        return users[username]["password"] == password
    return False

# Fungsi untuk menambah pengguna baru
def add_user(username, password):
    if username in users:
        return False  # Username sudah ada
    users[username] = {"password": password, "nama": nama, "email": email}
    save_users(users)
    return True

# Fungsi untuk validasi email
def validate_email(email):
    # Email harus mengandung @gmail.com
    if not email.endswith("@gmail.com"):
        return "Email harus berakhiran @gmail.com."
    return None

# Fungsi untuk validasi password
def validate_password(password):
    # Password harus memiliki minimal 8 karakter
    if len(password) < 8:
        return "Password harus memiliki minimal 8 karakter."
    # Password harus mengandung angka atau karakter apapun
    if not re.search(r'[0-9]', password) and not re.search(r'[A-Za-z]', password):
        return "Password harus mengandung angka atau huruf."
    return None


# Navigasi Sidebar
with st.sidebar:
    if st.session_state["user_authenticated"]:
        selected = option_menu("NextVerse", ["Home", "Cek Kesiapan", "Setting"], 
                               icons=["house", "clipboard", "gear"], 
                               menu_icon="menu-app-fill", default_index=0)
    else:
        selected = option_menu("NextVerse", ["Login", "Signup"], 
                               icons=["key", "person-add"],  # Login: FaSignInAlt, Signup: FaUserPlus
                               menu_icon="menu-app-fill", default_index=0)

    st.session_state.selected = selected


# Halaman Login
if selected == "Login":
    if not st.session_state["user_authenticated"]:
        st.title("Selamat Datang di NextVerse 🎓")
        st.markdown("<div class='custom-login-box'>", unsafe_allow_html=True)

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
            
        if st.button("Login", key="login_button"):
            if authenticate(username, password):
                st.session_state["user_authenticated"] = True
                st.session_state["selected_page"] = "Home"
                st.success("Login berhasil!")
                st.rerun()  # Memicu rerun aplikasi untuk redirect

            else:
                st.error("Username atau password salah.")



# Halaman Register (Signup)
elif selected == "Signup" and not st.session_state["user_authenticated"]:
    st.title("Daftar Akun Baru 📝")
    st.markdown("<div class='custom-login-box'>", unsafe_allow_html=True)

    # Kolom input untuk Nama, Email, Username, dan Password
    nama = st.text_input("Nama Lengkap", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    new_username = st.text_input("Username ", key="signup_username")
    new_password = st.text_input("Password ", type="password", key="signup_password")
            
    if st.button("Signup"):
        # Validasi form
        if nama and email and new_username and new_password:
            # Validasi password
            password_error = validate_password(new_password)
            if password_error:
                st.error(password_error)
            else:
                # Validasi email
                email_error = validate_email(email)
                if email_error:
                    st.error(email_error)
                else:
                    if add_user(new_username, new_password):
                        # Simpan data nama dan email sesuai dengan kebutuhan, misalnya dalam dictionary pengguna
                        users[new_username] = {
                            "password": new_password,
                            "nama": nama,
                            "email": email
                        }
                        save_users(users)  # Simpan data pengguna yang baru
                        st.success("Akun berhasil dibuat. Silakan login.")
                    else:
                        st.error("Username sudah digunakan. Coba username lain.")
        else:
            st.error("Mohon isi semua field.")


    
        
# Setelah login berhasil, redirect ke halaman yang dipilih
if st.session_state["user_authenticated"]:
    if selected == "Login" or selected == "Signup":
        selected = "Home"  # Atur halaman awal setelah login
        st.session_state["selected_page"] = selected
    st.session_state.selected = selected


        

# Inisialisasi scaler jika file ada
if os.path.exists('scaler.sav'):
    with open('scaler.sav', "rb") as f:
        scaler = pickle.load(f)





# Data kecerdasan dan jurusan
kecerdasan = {
    1: "Kecerdasan linguistik, Kecerdasan linguistik adalah kemampuan untuk menyusun pikiran dengan jelas melalui kata-kata.",
    2: "Kecerdasan logika matematika, Kecerdasan logika matematika adalah kemampuan untuk memahami angka dan pola.",
    3: "Kecerdasan spasial, Kecerdasan spasial adalah kemampuan untuk berpikir dalam bentuk visual.",
    4: "Kecerdasan musikal, Kecerdasan musikal adalah kemampuan untuk mengembangkan dan menikmati musik.",
    5: "Kecerdasan kinestetik, Kecerdasan kinestetik adalah kemampuan menggunakan tubuh untuk beraktivitas.",
    6: "Kecerdasan interpersonal, Kecerdasan interpersonal adalah kemampuan berkomunikasi dan berempati dengan orang lain.",
    7: "Kecerdasan intrapersonal, Kecerdasan intrapersonal adalah kemampuan untuk mengenali diri sendiri.",
    8: "Kecerdasan naturalistik, Kecerdasan naturalistik adalah kemampuan untuk memahami dunia alami."
}

jurusan = {
    1: ["Ilmu Perpustakaan", "Ilmu Komunikasi", "Bahasa dan Sastra", "Ilmu Hukum"],
    2: ["Statistika", "Akuntansi", "Ilmu Ekonomi", "Teknik Informatika"],
    3: ["Seni Rupa", "Teknik Arsitektur", "Teknik Sipil"],
    4: ["Seni Musik"],
    5: ["Kedokteran Gigi", "Kebidanan", "PJKR"],
    6: ["Ilmu Sosiologi", "Psikologi", "Ilmu Keperawatan"],
    7: ["Ilmu Agama", "Administrasi Niaga"],
    8: ["Ilmu Biologi", "Teknologi Pertanian", "Ilmu Kelautan"]
}

fakta = {
        1: "Apakah Anda suka membaca?",
        2: "Apakah Anda suka mengeksplorasi berbagai ide dan konsep dalam tulisan saya?",
        3: "Apakah Anda memiliki kosakata yang luas?",
        4: "Apakah Anda gemar menyelesaikan teka-teki silang dan mencari kata-kata?",
        5: "Apakah Anda gemar bercerita tentang humor, teka-teki, dan dongeng?",
        6: "Apakah Anda suka berpidato dan berdebat?",
        7: "Apakah acara TV favorit Anda adalah acara-acara komedi?",
        8: "Jika mendapatkan hadiah, apakah Anda akan memilih buku?",
        9: "Apakah pelajaran favorit Anda adalah Bahasa?",
        10: "Apakah Anda senang belajar secara bertahap?",
        11: "Apakah Anda suka menyelesaikan masalah?",
        12: "Apakah Anda menikmati menjelaskan cara kerja suatu hal kepada orang lain dan bekerja dengan angka itu menyenangkan?",
        13: "Apakah Anda suka melakukan eksperimen ilmiah?",
        14: "Apakah Anda merasa puas dengan segala hal yang bersifat logis?",
        15: "Apakah acara TV favorit Anda adalah acara dokumenter?",
        16: "Jika ada yang berniat memberi hadiah kepada Anda, apakah Anda akan memilih game komputer?",
        17: "Apakah pelajaran favorit Anda adalah matematika dan ilmu pengetahuan alam?",
        18: "Apakah Anda suka menggambar dan melukis?",
        19: "Apakah Anda menikmati membuat model, mural, dan kolase?",
        20: "Apakah Anda gemar memanfaatkan gambar dan diagram dalam proses belajar?",
        21: "Apakah Anda mampu membayangkan hasil akhir di dalam pikiran Anda?",
        22: "Apakah warna sangat penting bagi Anda?",
        23: "Apakah Anda mampu membayangkan peta dalam benak Anda?",
        24: "Apakah Anda lebih suka menonton acara televisi yang menampilkan seni dan kerajinan tangan?",
        25: "Jika seseorang ingin memberikan Anda hadiah, apakah Anda akan memilih puzzle?",
        26: "Apakah pelajaran favorit Anda adalah seni?",
        27: "Apakah Anda sangat menyukai berkolaborasi dengan orang lain?",
        28: "Apakah Anda suka menolong orang lain?",
        29: "Apakah Anda suka bertemu orang-orang baru?",
        30: "Apakah Anda suka olahraga dalam tim?",
        31: "Apakah Anda memiliki banyak teman?",
        32: "Apakah Anda memiliki banyak gagasan untuk kelas kita?",
        33: "Apakah acara TV favorit Anda adalah drama?",
        34: "Jika diberi pilihan hadiah, apakah Anda akan memilih untuk mendapatkan pengalaman liburan atau berwisata dengan teman-teman?",
        35: "Apakah Anda merasa senang saat bekerja dalam kelompok di sekolah?",
        36: "Apakah Anda menyukai fotografi?",
        37: "Apakah Anda suka mendaki bukit?",
        38: "Apakah Anda mempunyai hewan peliharaan?",
        39: "Apakah Anda senang berkebun?",
        40: "Apakah Anda lebih suka menonton acara televisi yang membahas tentang alam?",
        41: "Jika ada yang ingin memberi Anda hadiah, apakah Anda lebih memilih untuk pergi ke kebun binatang atau melakukan kegiatan outbound?",
        42: "Apakah Anda lebih suka berada di luar ruangan?",
        43: "Apakah Anda peduli terhadap lingkungan dengan cara melakukan daur ulang?",
        44: "Apakah Anda menikmati olahraga?",
        45: "Apakah Anda suka bekerja menggunakan tangan?",
        46: "Apakah Anda lebih mudah memahami dan belajar ketika langsung terlibat dalam kegiatan praktis atau pengalaman langsung, daripada hanya mendengarkan atau membaca teori?",
        47: "Apakah Anda menyukai akting?",
        48: "Apakah Anda suka bergerak saat bekerja?",
        49: "Apakah Anda lebih menyukai program olahraga televisi?",
        50: "Jika diberi hadiah, apakah Anda lebih memilih alat olahraga?",
        51: "Apakah Anda suka menari?",
        52: "Apakah kegiatan favorit Anda di sekolah adalah drama?",
        53: "Apakah Anda senang mengerjakan sendiri?",
        54: "Apakah Anda senang memikirkan hal-hal secara intelektual?",
        55: "Apakah Anda sering mengevaluasi diri?",
        56: "Apakah Anda menulis buku atau jurnal harian?",
        57: "Apakah Anda sering mengira-ngira apa yang dipikirkan orang?",
        58: "Jika diberi hadiah, apakah Anda akan memilih buku harian?",
        59: "Apakah Anda suka memikirkan perasaan Anda?",
        60: "Apakah saat-saat menyenangkan di sekolah adalah saat diberi kebebasan untuk memilih tugas sendiri?",
        61: "Apakah Anda suka menetapkan tujuan?",
        62: "Apakah Anda senang menyanyi?",
        63: "Apakah Anda menikmati mendengarkan musik?",
        64: "Apakah Anda merasa bahwa suara adalah hal yang menarik?",
        65: "Apakah Anda senang memainkan alat musik?",
        66: "Apakah Anda kadang menciptakan lagu sendiri?",
        67: "Apakah Anda sering menggerakkan kaki atau jemari mengikuti irama saat mendengarkan musik?",
        68: "Apakah program televisi favorit Anda adalah acara musik?",
        69: "Jika diberi hadiah, apakah Anda lebih suka mendapatkan kaset atau CD lagu-lagu sebagai hadiah?",
        70: "Apakah mata pelajaran favorit Anda adalah musik?",
}

# Aturan kecerdasan yang terkait dengan fakta
aturan = {
        1: [1, 2, 3, 4, 5, 6, 7, 8, 9], # Fakta terkait Linguistic-Verbal
        2: [10, 11, 12, 13, 14, 15, 16, 17], # Fakta terkait Logika-Matematik
        3: [18, 19, 20, 21, 22, 23, 24,25,26], # Fakta terkait Spasial-Visual
        4: [27, 28, 29, 30, 31, 32, 33, 34, 35], # Fakta terkait Interpersonal
        5: [36, 37, 38, 39, 40, 41, 42, 43, 44], # Fakta terkait Naturalis
        6: [45, 46, 47, 48, 49, 50, 51, 52, 53], # Fakta terkait Kinestetik
        7: [54, 55, 56, 57, 58, 59, 60, 61, 62], # Fakta terkait Intrapersonal
        8: [63, 64, 65, 66, 67, 68, 69, 70, 71], # Fakta terkait Musik-Ritmik
}

# Fungsi untuk mencocokkan fakta dengan kecerdasan
def cari_kecerdasan(input_fakta):
    hasil = []
    for id_kecerdasan, fakta_aturan in aturan.items():
        match_count = sum(1 for f in fakta_aturan if f in input_fakta)
        if match_count >= 7:  # Ambang batas kecocokan
            hasil.append(kecerdasan[id_kecerdasan])
    return hasil

# Fungsi untuk menentukan jurusan berdasarkan kecerdasan
def tentukan_jurusan(kecerdasan_terpilih):
    hasil_jurusan = []
    for id_kecerdasan, nama_kecerdasan in kecerdasan.items():
        if nama_kecerdasan in kecerdasan_terpilih:
            hasil_jurusan.extend(jurusan[id_kecerdasan])
    return hasil_jurusan

# Fungsi untuk menentukan jurusan berdasarkan kecerdasan
def tentukan_jurusan(kecerdasan_terpilih):
    hasil_jurusan = []
    for id_kecerdasan, nama_kecerdasan in kecerdasan.items():
        if nama_kecerdasan in kecerdasan_terpilih:
            hasil_jurusan.extend(jurusan[id_kecerdasan])
    return hasil_jurusan


# Halaman Home
if selected == "Home":
    # Membuat dua kolom (kolom kiri untuk teks, kolom kanan untuk gambar)
    col1, col2 = st.columns([1, 1])  # Ratio kolom kiri (lebih besar) dan kolom kanan (lebih kecil)

    # Menampilkan salam dengan format markdown dan emoji
    with col1:
        st.markdown("# Halo, Calon Mahasiswa Sukses! 🎓")
        st.markdown("### Pusing pilih jurusan?")
        
        # Pesan deskripsi dengan font yang lebih besar dan lebih rapi
        st.markdown("<p style='font-size: 16px;'>Jangan khawatir, kami punya solusi cerdas buat kamu! Sistem kami akan membantu memetakan minat dan bakatmu, lalu mencocokannya dengan jurusan yang paling tepat. Karena kuliah itu soal minat, bukan ikut-ikutan! 😊</p>", unsafe_allow_html=True)

        # Menambahkan paragraf dengan HTML untuk styling lebih lanjut
        st.markdown("<p style='font-size: 16px;'>Kalian bisa pilih menu di sebelah kiri untuk mulai menggunakan aplikasi ini.</p>", unsafe_allow_html=True)
    
        # Pemisah (line separator) antara bagian informasi
        st.markdown("---")

    with col2:
        st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;">', unsafe_allow_html=True)
        st.image("https://thumbs.dreamstime.com/b/university-campus-building-hall-education-students-cartoon-vector-illustration-brotherhood-smart-nerd-classes-hipster-young-155883192.jpg",  use_container_width=False)  # Gambar memenuhi kolom
        st.markdown('</div>', unsafe_allow_html=True)


# Halaman Hitung Persiapan
if selected == 'Cek Kesiapan':
    st.title('Yuk, Jawab pertanyaan berikut sesuai dengan keadaanmu saat ini')

    # Instruksi untuk pengguna
    st.markdown(
     f"""
        <div style="margin-bottom: 10px;">
            
        </div>
        """, unsafe_allow_html=True)

    # Input Fakta dari Pengguna
    input_fakta = []
    for id_fakta, pernyataan in fakta.items():
    # Tampilkan nomor dan pertanyaan
        st.write(f"{id_fakta}. {pernyataan}")  # Nomor dan pertanyaan yang terformat
        
        
        # Buat kotak container untuk pilihan "Ya" dan "Tidak"
        with st.container():
            # Pilihan Ya atau Tidak yang tampil dalam satu baris
            pilihan = st.radio(f"Pilih jawaban", ('Ya', 'Tidak'), index=None, horizontal=True, key=f"radio_{id_fakta}")

            # Menambahkan jawaban yang dipilih ke list input_fakta jika memilih 'Ya'
            if pilihan == 'Ya':
                input_fakta.append(id_fakta)
                
                
                # Mengatur margin dan jarak antara elemen
        st.markdown("<div style='margin-top: -5px;'></div>", unsafe_allow_html=True)  # Mengurangi jarak antara elemen

    # Proses dan tampilkan hasil
    if st.button("Cek Kesiapan"):
        kecerdasan_terpilih = cari_kecerdasan(input_fakta)
        if kecerdasan_terpilih:
            st.subheader("Jenis Kecerdasan yang Cocok dengan Kamu")
            for k in kecerdasan_terpilih:
                st.write(f"- {k}")
            
            jurusan_rekomendasi = tentukan_jurusan(kecerdasan_terpilih)
            st.subheader("Rekomendasi Jurusan Buat Kamu:")
            for j in jurusan_rekomendasi:
                st.write(f"- {j}")
        else:
            st.warning("Maaf, tidak ada kecerdasan yang cocok berdasarkan jawaban Anda.")
            

    if __name__ == "__main__":
                    main()

# Halaman Setting
if selected == 'Setting':
    st.title("Selamat tinggal sementara! Kami tunggu kedatanganmu lagi! 🤗🙌")
    if st.button("Logout", key="logout_button", help="Keluar dari akun"):
        st.session_state["user_authenticated"] = False  # Set session state as False
        st.session_state.selected = "Login"  # Set page to Login
        st.session_state["selected_page"] = "Login"  # Set selected page to Login
        st.success("Anda telah berhasil logout.")  # Show success message
        st.rerun()
        
    
            
# Menampilkan halaman Login setelah logout
if not st.session_state["user_authenticated"] and selected == "Login":
    st.warning('Silakan masuk dengan username dan password Anda.')

