from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os, time, datetime
from zoneinfo import ZoneInfo

load_dotenv()
USERNAME = os.getenv("NPM")
PASSWORD = os.getenv("PASSWORD")

options = Options()
options.add_argument("--headless") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=options)

try:
    now = datetime.datetime.now(ZoneInfo("Asia/Jakarta"))
    if now.weekday() >= 5 or not (8 <= now.hour < 21):
        print(" Di luar jam kuliah. Tidak mencoba absen.")
    else:
        driver.get("https://simkuliah.usk.ac.id/")
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

        time.sleep(2)  
        print(" URL setelah login:", driver.current_url)

        if "login" in driver.current_url.lower():
            print(" Gagal login. Cek username/password atau CAPTCHA.")
            driver.save_screenshot("login_failed.png")
            driver.quit()
            exit()

        driver.get("https://simkuliah.usk.ac.id/index.php/absensi")
        time.sleep(2)

        absen_dilakukan = False
        for i in range(2): 
            try:
                
                absen_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-success"))
                )
                
                print(f"--- Memproses Tombol Absen (Percobaan #{i+1}) ---")
                print("HTML tombol:", absen_button.get_attribute("outerHTML"))
                
                
                driver.execute_script("arguments[0].click();", absen_button)
                print("Tombol absen diklik.")
                time.sleep(2)
                driver.save_screenshot(f"after_absen_click_{i+1}.png")

                
                konfirmasi_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "confirm"))
                )
                driver.execute_script("arguments[0].click();", konfirmasi_button)
                print("Tombol konfirmasi diklik.")
                time.sleep(2)
                driver.save_screenshot(f"after_konfirmasi_click_{i+1}.png")
                
                print(f"--- Absen #{i+1} Selesai ---")
                absen_dilakukan = True
                time.sleep(3) 

            except Exception:
                
                print(f"Tidak ada lagi tombol absen yang ditemukan pada percobaan #{i+1}.")
                break
        
        if absen_dilakukan:
            print("Proses absensi selesai. Harap cek manual apakah absensi benar-benar tercatat.")
            os.system('curl -H "Title: Absen Berhasil" -d "Cihuyy, bot telah melakukan absensi." ntfy.sh/akbar-permana-absen-sukses')
        else:
            print("ℹ Tidak ada tombol absen yang bisa diklik. Mungkin tidak ada jadwal.")
            os.system('curl -H "Title: Tidak Ada Jadwal" -d "Bot berjalan, tapi tidak ada jadwal absen yang tersedia." ntfy.sh/lome_absen_gagal_yo')

except Exception as e:
    print(" Terjadi error:", e)
    driver.save_screenshot("error.png")
    print(" Screenshot error disimpan sebagai 'error.png'")
    print(" Potongan halaman:\n", driver.page_source[:1000])
    os.system('curl -H "Title:  Absen ERROR" -d "Terjadi error saat menjalankan bot. Cek log di GitHub Actions." ntfy.sh/lome_absen_error_yo')

finally:
    driver.quit()

