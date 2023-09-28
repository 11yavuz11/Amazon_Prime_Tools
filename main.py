from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re
import uuid


class XLSXReader:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def create_dict_from_xlsx(self):
        """
        Reads data from an XLSX file and converts it into a dictionary.
        """
        try:
            data = pd.read_excel(self.file_path)
            data_dict = dict(zip(data['sku'], data['asin']))
            return data_dict
        except FileNotFoundError:
            print("Envanter Dosya bulunamadı.")
            return {}
        except pd.errors.EmptyDataError:
            print("Envanter Dosya boş.")
            return {}
        except Exception as e:
            print("Envanter Bir hata oluştu:", e)
            return {}

class URLGenerator:
    def __init__(self, data, marketplace):
        self.data = data
        self.results = [] 
        self.marketplace = marketplace


    def checker(self):
        """
        Verilen veri sözlüğünden uygun Amazon ürün URL'lerini oluşturur.

        Generates the appropriate Amazon product URLs from the given data dictionary.
        """
        if self.marketplace == "sa": #SA için domain oluşturuyor UK US UAE
            for key, value in self.data.items():
                if key.startswith('UK') or key.startswith('uk'):
                    url = f"https://www.amazon.sa/-/en/dp/{value}/?m=A2R3VIMQ1WRL53&th=1"
                    self.results.append((url, key, value))
                elif key.startswith('US') or key.startswith('us'):
                    url = f"https://www.amazon.sa/-/en/dp/{value}/?m=A14PAP71RVPZX1&th=1"
                    self.results.append((url, key, value))
                elif key.startswith('UAE') or key.startswith('uae'):
                    url = f"https://www.amazon.sa/-/en/dp/{value}/?m=A33KVCWMBJ7XV6&th=1"
                    self.results.append((url, key, value))

        elif self.marketplace == "sg": #SG için domain oluşturuyor JP US 
            for key, value in self.data.items():
                if key.startswith('JP') or key.startswith('jp'):
                    url = f"https://www.amazon.sg/dp/{value}/?m=A78PUD8UBC03E&th=1"
                    self.results.append((url, key, value))
                elif key.startswith('US') or key.startswith('us'):
                    url = f"https://www.amazon.sg/dp/{value}/?m=ARPIJN329XQ0D&th=1"
                    self.results.append((url, key, value))

        elif self.marketplace == "ae": #AE için domain oluşturuyor UK US 
            for key, value in self.data.items():
                if key.startswith('UK') or key.startswith('uk'):
                    url = f"https://www.amazon.ae/-/en/dp/{value}/?m=A18S2T518BNNTX&th=1"
                    self.results.append((url, key, value))
                elif key.startswith('US') or key.startswith('us'):
                    url = f"https://www.amazon.ae/-/en/dp/{value}/?m=A2QUTRSO1ZHRN9&th=1"
                    self.results.append((url, key, value))

        elif self.marketplace == "com.au": #AU için domain oluşturuyor UK US DE
            for key, value in self.data.items():
                if key.startswith('UK') or key.startswith('uk'):
                    url = f"https://www.amazon.com.au/dp/{value}/?m=A3JCEYBC5L8UJ8&th=1"
                    self.results.append((url, key, value))
                elif key.startswith('US') or key.startswith('us'):
                    url = f"https://www.amazon.com.au/dp/{value}/?m=A4XRJ8S0WXSO0&th=1"
                    self.results.append((url, key, value))
                elif key.startswith('DE') or key.startswith('de'):
                    url = f"https://www.amazon.com.au/dp/{value}/?m=A3P6X2GIMA114Z&th=1"
                    self.results.append((url, key, value))
                
        return self.results

 
class SeleniumScraper:
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 2)
        self.results = []  # Sonuçları toplamak için boş bir liste oluşturuldu
        self.data = {}  # ASIN değerlerini tutmak için bir sözlük oluşturun
        self.price = 0  # Örnek olarak price'i başlatıyorum
        self.shipping_price = 0  # Örnek olarak shipping_price'i başlatıyorum
        self.max_stock = 0  # Örnek olarak max_stock'u başlatıyorum

   
    def scrape_data_sa(self, url, sku, asin):
        shipping_xpath = "//span[@data-csa-c-type='element'][contains(@data-csa-c-delivery-price, 'SAR')]"
        price_xpath_expression = '//*[@id="corePrice_feature_div"]/div/span[1]'
        availability_xpath_expression = '//*[@id="quantity"]'
        shipping_alternative_xpath = "//span[contains(text(), 'SAR') and contains(text(), 'delivery')]"
        self.driver.get(url)
        currency = 'SAR'
        self.priceChecker(price_xpath_expression, shipping_xpath, shipping_alternative_xpath, currency, availability_xpath_expression, marketplace="sa")

        result = [
            {
                "SKU": sku,
                "ASIN": asin,
                "Price": self.price,
                "Shipping Price": self.shipping_price,
                "Quantity": self.max_stock,
                "URL": url
            }
        ]
        self.results.append(result)

    def scrape_data_ae(self, url, sku, asin):
        shipping_xpath = "//span[@data-csa-c-type='element'][contains(@data-csa-c-delivery-price, 'AED')]"
        price_xpath_expression = '//*[@id="corePrice_feature_div"]/div/span[1]'
        availability_xpath_expression = '//*[@id="quantity"]'
        shipping_alternative_xpath = "//span[contains(text(), 'AED') and contains(text(), 'delivery')]"
        self.driver.get(url)
        currency = 'AED'
        self.priceChecker(price_xpath_expression, shipping_xpath, shipping_alternative_xpath, currency, availability_xpath_expression, marketplace="ae")

        result = [
            {
                "SKU": sku,
                "ASIN": asin,
                "Price": self.price,
                "Shipping Price": self.shipping_price,
                "Quantity": self.max_stock,
                "URL": url
            }
        ]
        self.results.append(result)

    def priceChecker(self,price_xpath_expression,shipping_xpath,shipping_alternative_xpath,currency ,availability_xpath_expression, marketplace ):
        try:
            self.price_element = self.wait.until(EC.presence_of_element_located((By.XPATH, price_xpath_expression)))
            self.price_text = self.price_element.text
            self.price = self.price_text.replace("\n", ".").replace(" ", "").replace(currency, "")
            self.shippingChecker(shipping_xpath, shipping_alternative_xpath, currency , marketplace , availability_xpath_expression)
            return self.price_text , self.price
        except Exception: #Price Exception
            with open(f"{marketplace}_error.txt", "a") as f:
                f.write(f"Price Fonksiyonunda Hata olustu SKU: {sku}, ASIN: {asin}\n")
            self.price = 0
            self.price_text = 0
            self.shipping_price = 0
            self.shipping_text = 0
            self.max_stock = 0
            
    def shippingChecker(self, shipping_xpath, shipping_alternative_xpath, currency, marketplace, availability_xpath_expression):
        try:
                shipping_element = self.wait.until(EC.presence_of_element_located((By.XPATH, shipping_xpath)))
                self.shipping_text = shipping_element.text
                shipping_price_match = re.search(fr'{currency} (\d+\.\d+)', self.shipping_text)
                self.shipping_price = float(shipping_price_match.group(1)) if shipping_price_match else 0
                self.quantityChecker(marketplace, availability_xpath_expression)
                return self.shipping_text , self.shipping_price

        except Exception:
                try:
                    element = self.wait.until(EC.presence_of_element_located((By.XPATH, shipping_alternative_xpath)))
                    self.shipping_text = element.text
                    shipping_price_match = re.search(fr'{currency} (\d+\.\d+)', self.shipping_text)
                    self.shipping_price = float(shipping_price_match.group(1)) if shipping_price_match else 0
                    self.quantityChecker(marketplace, availability_xpath_expression)
                    return self.shipping_text , self.shipping_price

                except Exception: #Shipping Exception
                    self.shipping_text = 0
                    self.shipping_price = 0
                    with open(f"{marketplace}_error.txt", "a") as f:
                        f.write(f"Shipping Fonksiyonunda Hata olustu SKU: {sku}, ASIN: {asin}\n")
            
    def quantityChecker(self, marketplace, availability_xpath_expression):
        
        try:
            delivery_index = self.shipping_text.find("delivery")
            if delivery_index != -1:
                after_delivery = self.shipping_text[delivery_index + len("delivery"):].strip()
                if after_delivery:
                    try:
                        availability_element = self.wait.until(EC.presence_of_element_located((By.XPATH, availability_xpath_expression)))
                        availability_text = availability_element.text.strip()
                        quantities = [int(q.strip()) for q in availability_text.split() if q.strip().isdigit()]

                        self.max_stock = max(quantities) if quantities else 0
                    except Exception: #Availability Exception
                        availability_xpath_expression = '//*[@id="availability"]/span'
                        availability_element = self.wait.until(EC.presence_of_element_located((By.XPATH, availability_xpath_expression)))
                        availability_text = availability_element.text.strip()
                        quantities = [int(q.strip()) for q in availability_text.split() if q.strip().isdigit()]
                        self.max_stock = max(quantities) if quantities else 0
                        with open(f"{marketplace}_error.txt", "a") as f:
                            f.write(f"Quantity Availability Fonksiyonunda Hata olustu SKU: {sku}, ASIN: {asin}\n")
                else:
                    self.max_stock = 0
            else:
                self.max_stock = 0
        except Exception: #Delivery Exception
            self.max_stock = 0
            with open(f"{marketplace}_error.txt", "a") as f:
                f.write(f"Quantity Delivery Fonksiyonunda Hata olustu SKU: {sku}, ASIN: {asin}\n")

        return self.max_stock

class ExcelWriter:
    def __init__(self, filename):
        self.filename = filename

    def export_to_excel(self, results):
        data = []
        for result in results:
            data.append({
                "SKU": result[0]["SKU"],
                "ASIN": result[0]["ASIN"],  
                "Price": str(result[0]["Price"]).replace(",", "."),
                "Shipping Price": str(result[0]["Shipping Price"]).replace(",", "."),
                "Quantity": result[0]["Quantity"],
                "URL": result[0]["URL"]
            })

        df = pd.DataFrame(data)
        df.to_excel(self.filename, index=False)

    def clean_error_file(marketplace):
        with open(f"{marketplace}_error.txt", "w") as f:
            f.write("")


registered_mac_address = "2E:BB:ED:B4:D2:4B"
system_mac_address = ':'.join(['{:02X}'.format((uuid.getnode() >> elements) & 0xFF) for elements in range(0, 2 * 6, 2)][::-1])
print(system_mac_address)
if system_mac_address == registered_mac_address:

    # Ana program akışı
    if __name__ == "__main__":
        marketplace = input('Lütfen 2 karakterlik market place giriniz: ').lower()

        # 2 karakter kontrolü
        if len(marketplace) != 2:
            print("Hatalı giriş! Market place 2 karakter olmalıdır.")
        else:
            file_path = "inventory.xlsx"
            xlsx_reader = XLSXReader(file_path)
            data = xlsx_reader.create_dict_from_xlsx()

            if marketplace == "sa":
                ExcelWriter.clean_error_file('sa')
                url_generator = URLGenerator(data, marketplace)
                results = url_generator.checker()

                scraper = SeleniumScraper()
                excel_writer = ExcelWriter(f"{marketplace}_results.xlsx")

                for url, sku, asin in results:
                    scraper.scrape_data_sa(url, sku, asin)
                excel_writer.export_to_excel(scraper.results)

                print(f"Veri çekme ve dışa aktarma tamamlandı. Sonuçlar {marketplace}_results.xlsx dosyasına kaydedildi.")

                scraper.driver.quit()
                
            elif marketplace == "ae":
                ExcelWriter.clean_error_file('ae')
                url_generator = URLGenerator(data, marketplace)
                results = url_generator.checker()

                scraper = SeleniumScraper()
                excel_writer = ExcelWriter(f"{marketplace}_results.xlsx")

                for url, sku, asin in results:
                    scraper.scrape_data_ae(url, sku, asin)
                excel_writer.export_to_excel(scraper.results)

                print(f"Veri çekme ve dışa aktarma tamamlandı. Sonuçlar {marketplace}_results.xlsx dosyasına kaydedildi.")

                scraper.driver.quit()
    else:
        print("Hatalı bir işlem yaptınız!\n Lütfen (sa, ae, sg) şeklinde seçim yapınız")
else:
    print("Error: MAC addresses do not match. The program will not run.")
    # Code for the program to stop running goes here.