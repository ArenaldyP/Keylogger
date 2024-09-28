# Keylogger
Keylogger. Exfill Keylog Menggunakan Pastebin

# Penjelasan Fitur:
**Keylogger**: Kode ini menggunakan pynput untuk merekam penekanan tombol dan menyimpan hasilnya dalam file teks.
**Penyimpanan Log**: Log penekanan tombol disimpan di file dengan nama yang mengikuti format hostname_processmanager.txt di folder AppData.
**Pengiriman ke Pastebin**: Setiap 10 detik, log dikirim ke Pastebin menggunakan API Pastebin. Log diubah menjadi format base64 sebelum dikirim untuk menyembunyikan isinya agar tidak langsung terbaca.
**Self Destruct**: Setelah flag diubah, keylogger berhenti, dan file log dihapus untuk menghindari jejak.
