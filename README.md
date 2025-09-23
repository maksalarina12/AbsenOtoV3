# Absen Otomatis USK

> *"Karena mahasiswa yang baik adalah mahasiswa yang hadir, tapi mahasiswa yang genius adalah yang bikin bot untuk hadir sambil rebahan (masi aja ada orang yang bayar untuk jasa absen online)"* 

Automated attendance system untuk mahasiswa Universitas Syiah Kuala yang sering lupa absen karena masih ngantuk atau lagi asik scroll TikTok. Dibuat oleh mahasiswa malas yang capek bangun pagi cuma buat pencet tombol absen.

## Features

- **Auto-login** ke SIMKULIAH USK (karena males ngingat password setiap hari)
- **Smart scheduling** dengan GitHub Actions (gratis pula, untung ada Microsoft)
- **Multi-session support** untuk yang jadwalnya chaos kayak hidup kita
- **Error handling** yang lumayan robust (hasil pengalaman sering gagal login)
- **Screenshot evidence** buat debugging atau bukti ke dosen kalau sistem error lagi

## Quick Start

### Prerequisites
- Akun GitHub (yang masih inget passwordnya)
- Credentials SIMKULIAH yang belum expired
- Doa agar WiFi kampus tidak lemot
- Niat untuk tidak bolos kuliah fisik (ini yang paling susah)

### Setup Instructions

1. **Fork/Clone repository ini**
   ```bash
   git clone https://github.com/NapoleonPro/absenv0.1.git
   ```

2. **Setup GitHub Secrets**
   - Buka Settings > Secrets and variables > Actions (kalau lupa dimana, googling aja)
   - Tambahkan secrets berikut:
     - `NPM`: Nomor Pokok Mahasiswa kamu (yang sering lupa pas ditanya dosen)
     - `PASSWORD`: Password SIMKULIAH (jangan yang sama dengan password semua akun lain ya, please!)

3. **Activate Workflow**
   - Buka tab Actions di repository
   - Enable workflows (tinggal klik doang kok, gampang)
   - Duduk santai sambil ngopi dan berharap bot nya gak ngambek

## Schedule

- **Selasa**: 08:05 & 10:50 WIB
- **Rabu**: 08:05, 10:50 & 14:05 WIB  
- **Kamis**: 14:05 & 17:00 WIB
- **Jumat**: 10:50 WIB

*Schedule dapat disesuaikan di file `.github/workflows/absen.yml` (kalau kamu tau cara edit CRON - kalau ngga tau, jangan diutak-atik nanti rusak)*

## Tech Stack

- **Python 3.12** - Karena developer males upgrade dari 3.11 tapi YOLO
- **Selenium WebDriver** - Biar bisa klik-klik otomatis kayak tangan kita
- **GitHub Actions** - CI/CD gratis, siapa yang nolak coba?
- **Chrome Headless** - Browser siluman yang kerja tanpa kelihatan

## Local Development

```bash
# Setup virtual environment (buat yang peduli sama dependency hell)
python -m venv mymyenv
source mymyenv/bin/activate  # Linux/Mac
# atau
mymyenv\Scripts\activate     # Windows (wtf is this os)

# Install dependencies (semoga gak error)
pip install -r requirement.txt

# Setup environment variables (jangan lupa!)
cp .env.example .env
# Edit .env dengan credentials  (kocak si kalo lupa?)

# Run manual test (doain jalan ya)
python absen.py
```

## Roadmap

### Near Future (ketika developer udah gak malas lagi)
- **Multi-account support** - Tinggal nambahin loop doang sih, tapi males mikir error handlingnya
- **Custom schedule per user** - Soalnya jadwal setiap mahasiswa beda-beda kayak kehidupan
- **Telegram/Discord notifications** - Biar tau kalau bot berhasil atau lagi mogok

### Far Future (ketika developer dapet pencerahan atau kena deadline)
- **GUI Desktop Application** - Buat yang alergi terminal hitam-hitam
- **Web dashboard** - Monitoring absensi dengan tampilan kece
- **AI prediction** - Prediksi kapan sistem USK bakal down lagi (spoiler: sering banget)

## Disclaimer

- Tool ini dibuat untuk **educational purposes** dan membantu mahasiswa pelupa kayak developer
- Gunakan dengan bijak dan tetap ikut kuliah beneran (jangan cuma ngandalin bot doang)
- Developer tidak bertanggung jawab jika:
  - Dosen jadi curiga kenapa kamu tiba-tiba rajin absen tepat waktu
  - Sistem USK upgrade security terus bot-nya jadi gabisa login
  - Kamu ketagihan bikin automation buat hal lain sampe lupa ngerjain tugas
  - Bot-nya lagi bad mood dan gamau jalan (namanya juga teknologi)

## Contributing

Pull requests are welcome! Apalagi kalau ada yang mau:
- Fix bugs yang developer udah tau tapi males benerin
- Nambahin fitur keren (yang developer kepikiran tapi lupa dicatet)
- Improve documentation (ini paling dibutuhin, soalnya developer jelek nulis dokumentasi)
- Kasih kopi virtual atau doa biar developer semangat coding lagi

## License

MIT License - Bebas dipake, dimodifikasi, bahkan dijual (tapi kasih tau developer ya, siapa tau bisa bagi hasil buat beli kopi)

## Developer Notes

*"Code yang bagus adalah code yang bisa dipahami oleh kamu di masa depan ketika kamu udah lupa sama sekali kenapa kamu bikin ini dan lagi desperate nyari solusi yang sama"*

Dibuat dengan ❤️(wth), ☕, dan sedikit frustrasi oleh mahasiswa malas tapi pengen lulus tepat waktu tanpa ribet.

---

**Kalau terbantu, kasi star plis karena star bikin developer merasa dihargai (dan semangat maintain code-nya).**