import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd
import os
from datetime import datetime

class AmazonScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.base_url = "https://www.amazon.in/dp/"

    def get_page(self, url):
        """Fetch page content with a random delay"""
        try:
            time.sleep(random.uniform(1, 3))
            response = self.session.get(url)
            print(f"Request status: {response.status_code} for URL: {url}")
            return response.text if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching the page: {e}")
            return None

    def extract_mrp(self, soup):
        """Extract MRP from the product page"""
        try:
            mrp_container = soup.find('div', class_='a-section a-spacing-small aok-align-center')
            if mrp_container:
                mrp_price = mrp_container.find('span', class_='a-price a-text-price')
                if mrp_price:
                    mrp_value = mrp_price.find('span', class_='a-offscreen')
                    if mrp_value:
                        return mrp_value.text.strip()
        except Exception as e:
            print(f"Error extracting MRP: {e}")
        return 'N/A'

    def parse_product_page(self, asin):
        """Extract product details using ASIN"""
        url = f"{self.base_url}{asin}"
        html_content = self.get_page(url)
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')
        product_data = {'asin': asin}

        # Extract product title
        title = soup.find('span', id='productTitle')
        product_data['title'] = title.text.strip() if title else 'N/A'

        # Extract sale price
        price = soup.find('span', class_='a-price-whole')
        fraction = soup.find('span', class_='a-price-fraction')
        product_data['sale_price'] = f"{price.text}{fraction.text}" if price and fraction else 'N/A'

        # Extract MRP using the new method
        product_data['mrp'] = self.extract_mrp(soup)

        # Extract seller
        seller = soup.find('a', id='sellerProfileTriggerId')
        product_data['seller'] = seller.text.strip() if seller else 'N/A'

        return product_data

    def parse_asins_from_file(self, file_path):
        """Read ASINs from a text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                asins = [line.strip() for line in file.readlines() if line.strip()]
            return asins
        except Exception as e:
            print(f"Error reading ASIN file: {e}")
            return []

    def parse_multiple_products(self, asins, save_path=r"PATH FOR EXCEL FILE"):    # ADD THE PATH FOR EXCEL FILE
        """Extract product details for multiple ASINs and save to an Excel file"""
        products = []
        for asin in asins:
            product_data = self.parse_product_page(asin)
            if product_data:
                products.append(product_data)
        
        if products:
            df = pd.DataFrame(products)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Ensure directory exists
            
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_save_path = save_path.replace(".xlsx", f"_{timestamp}.xlsx")
                df.to_excel(new_save_path, index=False)
                print(f"Results saved to: {new_save_path}")
            except PermissionError:
                print("Permission denied: Close the file if it's open and try again.")
        
        return products

# Usage Example
if __name__ == "__main__":
    scraper = AmazonScraper()
    file_path = r"PATH OF TEXT FILE CONTAINING THE ASIN"  # Use raw string for file path
    asin_list = scraper.parse_asins_from_file(file_path)
    
    if asin_list:
        product_details_list = scraper.parse_multiple_products(asin_list)

        for product_details in product_details_list:
            print("\nProduct Details:")
            for key, value in product_details.items():
                print(f"{key}: {value}")
    else:
        print("No ASINs found in the file.")
