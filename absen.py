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

        # Login
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

        
        print("✅ Berhasil mengunjungi halaman absensi.")
        print("   Sistem baru sepertinya otomatis mencatat kehadiran.")
        print("   Harap cek manual di LMS untuk memastikan.")
        
        driver.save_screenshot("absen_sukses.png")
        print("   Screenshot disimpan sebagai 'absen_sukses.png'.")

        
        jam = now.strftime("%H:%M")
        os.system(f'notify-send "✅ Absensi Berhasil" "Jam {jam}, bot telah mengunjungi halaman absensi."')

except Exception as e:
    print(" Terjadi error:", e)
    driver.save_screenshot("error.png")
    print(" Screenshot error disimpan sebagai 'error.png'")
    print(" Potongan halaman:\n", driver.page_source[:1000])

finally:
    driver.quit()

