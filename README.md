# Password Checker
Password Checker adalah aplikasi desktop sederhana berbasis Python yang digunakan untuk menganalisis tingkat kekuatan sebuah password berdasarkan beberapa karakteristik keamanan, seperti panjang password, penggunaan huruf besar, huruf kecil, angka, dan karakter khusus.

Project ini dibuat sebagai project pembelajaran Cyber Security untuk pemula, khususnya untuk memahami dasar-dasar password security, password strength analysis, hashing, dan penggunaan Python dalam keamanan siber.

# Features
- Password Strength Checker — menganalisis kekuatan password.
- Strength Indicator — menampilkan tingkat kekuatan password melalui progress bar.
- Password Suggestion — memberikan saran password jika password yang dimasukkan masih lemah.
- Show/Hide Password — menampilkan atau menyembunyikan password.
- SHA-256 Hashing — melakukan hashing terhadap password menggunakan SHA-256.
- Save Password Hash — menyimpan hasil hash ke file lokal password.txt.
- Dark UI — menggunakan tampilan hitam-putih yang sederhana dan profesional.

# Technologies
- Python 3
- CustomTkinter — untuk membuat GUI.
- Regular Expression (re) — untuk memeriksa karakter password.
- Hashlib — untuk SHA-256 hashing.
- Random & String — untuk menghasilkan saran password.

# Installation
Pastikan Python sudah terinstall.

Clone repository:
git clone https://github.com/samkiputt/password-checker.git
cd password-checker

Install dependency:

pip install customtkinter
▶️ Run

Jalankan aplikasi menggunakan:

python app.py

Setelah dijalankan, aplikasi akan menampilkan GUI Password Checker.
