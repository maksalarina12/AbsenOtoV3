from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os, time, datetime
from zoneinfo import ZoneInfo

# Load .env
load_dotenv()
USERNAME = os.getenv("NPM")
PASSWORD = os.getenv("PASSWORD")

# --- Konfigurasi Selenium ---
# Path ke chromedriver yang ada di folder proyek Anda
# chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver-linux64", "chromedriver")
# service = Service(executable_path=chromedriver_path)
# # Path ke binary Google Chrome yang sebenarnya
# chrome_binary_path = "/opt/google/chrome/google-chrome"
# options = Options()
# options.binary_location = chrome_binary_path
# # options.add_argument("--headless") # Aktifkan untuk mode headless
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# # Menambahkan user-agent untuk menghindari deteksi bot
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# # Inisialisasi driver dengan service dan options
# driver = webdriver.Chrome(service=service, options=options)


# --- Konfigurasi Selenium ---
options = Options()
options.add_argument("--headless") # Aktifkan untuk mode headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Menambahkan user-agent untuk menghindari deteksi bot
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# Inisialisasi driver (Selenium akan mencari chromedriver secara otomatis)
driver = webdriver.Chrome(options=options)


try:
    now = datetime.datetime.now(ZoneInfo("Asia/Jakarta"))
    if now.weekday() >= 5 or not (8 <= now.hour < 21):
        print(" Di luar jam kuliah. Tidak mencoba absen.")
    else:
        driver.get("https://simkuliah.usk.ac.id/")
        wait = WebDriverWait(driver, 10)

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

        time.sleep(2)  # Tunggu halaman berpindah
        print(" URL setelah login:", driver.current_url)

        # Cek apakah login berhasil
        if "login" in driver.current_url.lower():
            print(" Gagal login. Cek username/password atau CAPTCHA.")
            driver.save_screenshot("login_failed.png")
            driver.quit()
            exit()

        # Arahkan ke halaman absen
        driver.get("https://simkuliah.usk.ac.id/absensi")
        time.sleep(2)

        absen_button = None
        try:
            # Cari tombol berdasarkan ID yang sudah ditemukan
            absen_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "konfirmasi-kehadiran"))
            )
        except:
            print(" ID 'konfirmasi-kehadiran' tidak ditemukan. Mencoba alternatif...")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                text = btn.text.lower()
                html = btn.get_attribute("innerHTML").lower()
                if "absen" in text or "konfirmasi" in html:
                    absen_button = btn
                    break

# ... (semua bagian sebelumnya tidak berubah)

        if absen_button:
            print(" HTML tombol absen yang ditemukan:")
            print(absen_button.get_attribute("outerHTML"))
            print(" Menekan tombol absen...")
            driver.execute_script("arguments[0].click();", absen_button)

            time.sleep(2)

            driver.save_screenshot("after_click.png")
            print(" Klik selesai. Screenshot disimpan ke 'after_click.png'.")
            print(" URL sekarang:", driver.current_url)

            # Menunggu tombol konfirmasi
            konfirmasi_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "confirm"))
            )
            print("⏳ Menekan tombol konfirmasi...")
            driver.execute_script("arguments[0].click();", konfirmasi_button)

            time.sleep(2)

            driver.save_screenshot("after_konfirmasi_click.png")
            print(" Klik konfirmasi selesai. Screenshot disimpan ke 'after_konfirmasi_click.png'.")
            print(" URL sekarang:", driver.current_url)

            print(" Harap cek manual apakah absensi benar-benar tercatat.")

            # ✅ NOTIFIKASI hanya muncul jika absen dan konfirmasi sukses
            jam = now.strftime("%H:%M")
            os.system(f'notify-send "✅ Absensi Berhasil" "Jam {jam}, cihuy bot telah melakukan absensi ya boss."')

        else:
            print("ℹ️ Tidak ada tombol absen yang bisa diklik. Mungkin tidak ada jadwal.")

except Exception as e:
    print(" Terjadi error:", e)
    driver.save_screenshot("error.png")
    print(" Screenshot error disimpan sebagai 'error.png'")
    print(" Potongan halaman:\n", driver.page_source[:1000])

finally:
    driver.quit()

