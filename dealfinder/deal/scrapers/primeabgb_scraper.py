import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def search_primeabgb(product, total_products_count):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        search_query = '+'.join(product.split())
        url = f'https://www.primeabgb.com/?s={search_query}&post_type=product'
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        response.close()
        
        product_list = soup.find_all('div', class_='product')
        primeabgb_data = defaultdict(dict)
        
        count = 0
        for product in product_list:
            # Product name
            name = product.find('h3')
            primeabgb_data[count]['item_name'] = name.get_text(strip=True) if name else 'Unavailable'

            # Product rating (PrimeABGB does not display ratings directly, so assuming it’s unavailable)
            primeabgb_data[count]['item_rating'] = 'Unavailable'

            # Product price
            price = product.find('span', class_='woocommerce-Price-amount')
            if price:
                primeabgb_data[count]['item_price'] = price.get_text(strip=True).replace('₹', '').replace(',', '')
            else:
                primeabgb_data[count]['item_price'] = 'Unavailable'
            
            # Product link
            link = product.find('a', href=True)
            primeabgb_data[count]['item_link'] = link['href'] if link else 'Unavailable'
            
            # Product image
            image = product.find('img')
            primeabgb_data[count]['item_image'] = image['src'] if image else 'Unavailable'

            count += 1
            if count == total_products_count:
                return primeabgb_data

        return primeabgb_data

    except Exception as e:
        print(f"Error fetching PrimeABGB data: {e}")
        return {}
