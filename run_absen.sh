#!/bin/bash
# Script untuk menjalankan absen.py dari direktori yang benar dengan environment yang aktif

# Pindah ke direktori proyek
cd /home/akbar-permana/codyeah/belajarpython/absenv0.1

# Aktifkan virtual environment
source mymyenv/bin/activate

# Jalankan skrip Python
# Menambahkan opsi -u (unbuffered) agar output langsung ditulis ke log systemd
python -u absen.py
