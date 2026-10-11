import csv
import time
import msvcrt 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. INISIALISASI BROWSER
driver = webdriver.Chrome()
URL_WEBSITE = "https://new-mika-pegawai.mikroskil.ac.id/bka/micard?stambuk=2026"
driver.get(URL_WEBSITE)

print("=====================================================")
print("SILAKAN LOGIN SECARA MANUAL DI BROWSER.")
print("Pastikan halaman MiCard untuk Stambuk 2026 sudah terbuka sepenuhnya.")
input("TEKAN ENTER DI SINI UNTUK MEMULAI OTOMATISASI...")
print("=====================================================\n")

# 2. BACA CSV
file_csv = 'C:/Users/Staff BKA/Downloads/MiCard/data_mahasiswa_2026.csv'

with open(file_csv, mode='r', encoding='utf-8-sig') as file:
    baris_pertama = file.readline()
    file.seek(0)
    pemisah = ';' if ';' in baris_pertama else ','
    
    reader = csv.DictReader(file, delimiter=pemisah)
    
    for row in reader:
        stambuk = row['Stambuk'].strip() 
        print(f"\n=====================================================")
        print(f"Memproses Stambuk: {stambuk}")
        
        try:
            print(" -> [Tahap A] Mencari kotak search tabel...")
            xpath_search = '//*[@id="input-v-12"]'
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_search))
            )
            search_box.send_keys(Keys.CONTROL, 'a') 
            search_box.send_keys(Keys.BACKSPACE)
            search_box.send_keys(stambuk)
            search_box.send_keys(Keys.RETURN) 
            
            print(" -> [Tahap B.1] Menunggu tabel data muncul dan mencari roda gigi...")
            xpath_baris_target = f"//tr[td[contains(., '{stambuk}')]]"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_baris_target))
            )
            xpath_tombol_roda_gigi = f"{xpath_baris_target}//button"
            btn_settings = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_tombol_roda_gigi))
            )
            btn_settings.click()
            
            print(" -> [Tahap B.2] Memvalidasi NIM di dalam pop-up...")
            xpath_nim_popup = f"//*[contains(., '{stambuk}')]"
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, xpath_nim_popup))
                )
            except:
                print(f"❌ BERHENTI! NIM {stambuk} tidak ditemukan di pop-up layar.")
                input("Tutup pop-up secara manual di browser, lalu tekan ENTER di sini untuk lanjut...")
                continue 
            
            print(" -> [Tahap C.1] Scroll ke bawah dan mencari tombol DAFTARKAN KARTU...")
            xpath_daftarkan = "//button[contains(translate(., 'daftarkan', 'DAFTARKAN'), 'DAFTARKAN')]"
            try:
                btn_daftarkan = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_daftarkan))
                )
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn_daftarkan)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", btn_daftarkan)
                print("✅ Tombol 'DAFTARKAN KARTU' berhasil diklik!")
            except Exception as e:
                print("⚠️ Tombol 'DAFTARKAN KARTU' tidak ditemukan. Menunggu konfirmasi data...")
            
            # --- TAHAP C.2: MENUNGGU KARTU DI-TAP ATAU DI-SKIP ---
            print(f">>> ROBOT MENUNGGU... SILAKAN TAP KARTU UNTUK {stambuk}! <<<")
            print(">>> Tekan 'N' di keyboard (pada jendela CMD ini) jika ingin SKIP mahasiswa ini. <<<")
            
            xpath_ya = "//button[contains(translate(., 'ya', 'YA'), 'YA')]"
            xpath_terdaftar = "//*[contains(translate(., 'id kartu terdaftar', 'ID KARTU TERDAFTAR'), 'ID KARTU TERDAFTAR')]"
            
            kartu_berhasil_ditap = False
            skip_kartu = False
            waktu_maksimal = time.time() + 3600 
            
            while time.time() < waktu_maksimal:
                if msvcrt.kbhit():
                    tombol_ditekan = msvcrt.getch().decode('utf-8').lower()
                    if tombol_ditekan == 'n':
                        print("\n⏩ SKIP DITEKAN! Membatalkan kartu ini dan lanjut ke Stambuk berikutnya...")
                        skip_kartu = True
                        break 
                
                try:
                    btn_ya = WebDriverWait(driver, 0.1).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_ya))
                    )
                    btn_ya.click()
                    print("\n✅ Kartu terdeteksi (Klik tombol 'Ya')!")
                    kartu_berhasil_ditap = True
                    break 
                except:
                    pass 
                
                try:
                    elemen_terdaftar = driver.find_element(By.XPATH, xpath_terdaftar)
                    if elemen_terdaftar.is_displayed():
                        print("\n✅ Label 'ID Kartu Terdaftar' terdeteksi! Lanjut ke penyimpanan...")
                        kartu_berhasil_ditap = True
                        break
                except:
                    pass
                
                time.sleep(0.5)
            
            # --- EKSEKUSI SETELAH MENUNGGU ---
            if skip_kartu:
                print(" -> Mengklik Batal untuk menutup pop-up...")
                try:
                    xpath_batal = "//button[contains(translate(., 'batal', 'BATAL'), 'BATAL')]"
                    btn_batal = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, xpath_batal))
                    )
                    driver.execute_script("arguments[0].click();", btn_batal)
                    print("✅ Pop-up berhasil ditutup.")
                except:
                    try:
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                        print("✅ Pop-up tertutup paksa via ESCAPE.")
                    except:
                        pass
                
                time.sleep(1.5) 
                continue 
                
            if kartu_berhasil_ditap:
                print(" -> [Tahap D] Menyimpan data secara final...")
                # Tambahan jeda 2 detik agar pop-up "Ya" benar-benar menghilang dari layar
                time.sleep(2) 
                
                # XPath Simpan disederhanakan dan menggunakan JS Click
                xpath_simpan = "//button[contains(translate(., 'simpan', 'SIMPAN'), 'SIMPAN')]"
                btn_simpan = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_simpan))
                )
                # Eksekusi klik paksa menembus halangan animasi
                driver.execute_script("arguments[0].click();", btn_simpan)
                print(f"✅ Data final untuk NIM {stambuk} berhasil disimpan.")
                time.sleep(2)
            
        except Exception as e:
            print(f"\n⚠️ ERROR TEKNIS PADA STAMBUK {stambuk}")
            print(f"Pesan Error Asli: {str(e)[:300]}...") # Memunculkan kembali error asli untuk panduan
            print("Sistem mengalami kemacetan yang tidak terduga.")
            input("Cek browser Anda, refresh jika perlu, lalu tekan ENTER di sini untuk lanjut ke kartu berikutnya...")

print("\nSELESAI! Seluruh data dari CSV telah diproses.")
