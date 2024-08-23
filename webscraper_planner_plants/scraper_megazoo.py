import requests
from bs4 import BeautifulSoup


def extract_megazoo_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_description = soup.find('div', class_='et-product-description')
        if product_description:
            content = product_description.get_text(separator=" ", strip=True)
            price = soup.find('div', class_='price h1')
            if price:
                content += " Preis: " + price.get_text(separator=" ", strip=True)
                details = soup.find('div', class_='technical-details-content')
                if details:
                    content += " Lieferumfang und technische Details: " + details.get_text(separator=" ", strip=True)
                    return content
                return content
            return content
        else:
            print("Element 'et-product-description' not found")
            return None
    else:
        print(f"Failed to retrieve {url}")
        return None