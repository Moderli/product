import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def search_theitdepot(product, total_products_count):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        search_query = '+'.join(product.split())
        url = f'https://www.theitdepot.com/search.html?txtsearch={search_query}'
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        response.close()

        product_list = soup.find_all('div', class_='search-result-product')
        theitdepot_data = defaultdict(dict)
        
        count = 0
        for product in product_list:
            # Product name
            name = product.find('a', class_='product-title')
            theitdepot_data[count]['item_name'] = name.get_text(strip=True) if name else 'Unavailable'

            # Product rating (The IT Depot does not display ratings directly, so assuming it’s unavailable)
            theitdepot_data[count]['item_rating'] = 'Unavailable'

            # Product price
            price = product.find('span', class_='price')
            if price:
                theitdepot_data[count]['item_price'] = price.get_text(strip=True).replace('₹', '').replace(',', '')
            else:
                theitdepot_data[count]['item_price'] = 'Unavailable'
            
            # Product link
            link = name['href'] if name else None
            theitdepot_data[count]['item_link'] = link if link else 'Unavailable'

            # Get the image URL
            item_image = product.find('img')
            if item_image and item_image.get('data-src'):
                theitdepot_data[count]['item_image'] = item_image['data-src']
            else:
                theitdepot_data[count]['item_image'] = 'Unavailable'

            count += 1
            if count == total_products_count:
                return theitdepot_data

        return theitdepot_data

    except Exception as e:
        print(f"Error fetching The IT Depot data: {e}")
        return {}
