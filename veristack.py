from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import matplotlib.pyplot as plt


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

urun_fiyat_list = {"trendyol.com": "","amazon.com.tr":""}


sites = {
     "trendyol.com": { "by_search" : By.CLASS_NAME , "search_name" : "V8wbcUhU", "by_button" : By.CLASS_NAME , "button_name" : "cyrzo7gC", "by_urun" : By.CLASS_NAME , "urun_name" : "prc-box-dscntd"   },
     #"hepsiburada.com": { "by_search" : By.CLASS_NAME , "search_name" : "searchBarContent-UfviL0lUukyp5yKZTi4k", "by_button" : "empty" , "button_name" : "empty", "by_urun" : By.CLASS_NAME , "urun_name" : "moria-ProductCard-kUDchF bITiu ss2sxxrapx4"   },
     "amazon.com.tr": { "by_search" : By.ID , "search_name" : "twotabsearchtextbox", "by_button" : By.ID , "button_name" : "nav-search-submit-button", "by_urun" : By.CLASS_NAME , "urun_name" : "a-price-whole"   }
}


def fiyat_cek(urun_ad):

    for site_ad , site_info in sites.items():
        driver.get(f"https://www.{site_ad}/")

        if site_ad == "trendyol.com":
            WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'modal-close')))
            close_trendyol = driver.find_element(By.CLASS_NAME, 'modal-close')
            close_trendyol.click()


        """try:
            WebDriverWait(driver, 5).until(
                expected_conditions.element_to_be_clickable((By.CLASS_NAME, "cc-btn"))
            ).click()  
        except Exception as e:
            print(f"Çerez penceresi engellendi veya bulunamadı: {e}")"""

        """if site_ad == "hepsiburada.com":
            WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,"data-test-id=search-bar-input")))
        
            hepsiburada_click = driver.find_element(By.CSS_SELECTOR,"data-test-id=search-bar-input")
            hepsiburada_click.click()"""
        
        WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((site_info["by_search"],site_info["search_name"])))
        
        search_element = driver.find_element(site_info["by_search"],site_info["search_name"])
        
        search_element.send_keys(urun_ad)
        
        WebDriverWait(driver,4).until(expected_conditions.element_to_be_clickable((site_info["by_button"],site_info["button_name"])))
        clk_button_element = driver.find_element(site_info["by_button"],site_info["button_name"])
        clk_button_element.click()

        WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((site_info["by_urun"],site_info["urun_name"])))
        
        
        
        for _ in range(10):  
            urun_elements = driver.find_elements(site_info["by_urun"],site_info["urun_name"])
            driver.execute_script("window.scrollBy(0, 500);")  # 500px kaydır
            time.sleep(1)

        urun_elements = urun_elements[:50]
        gecisi_list = []
        for urun in urun_elements:
            urun = urun.text
            urun = urun.split(" ")[0]
            gecisi_list.append(int(urun.replace(".", "").split(",")[0]))
            print(urun)
            print(float(urun.replace(".", "").replace(",", ".")))
            
            
        urun_fiyat_list[site_ad]=gecisi_list
        
        time.sleep(3)

def fiyat_karsilastir():

    for site_ad, urun_fiyat in urun_fiyat_list.items():
        
        plt.plot(range(len(urun_fiyat)), urun_fiyat, label=site_ad)
    plt.xlabel("Ürün Sırası")
    plt.ylabel("Fiyat (TL)")
    plt.title("Siteler Arası Fiyat Karşılaştırması")
    plt.legend()
    plt.show()






fiyat_cek("pantolon")
fiyat_karsilastir()
print(urun_fiyat_list)
driver.quit()

