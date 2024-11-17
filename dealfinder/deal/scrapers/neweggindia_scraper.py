import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def search_neweggindia(product, total_products_count):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        search_query = '+'.join(product.split())
        url = f'https://www.newegg.com/global/in-en/p/pl?d={search_query}'
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        response.close()

        product_list = soup.find_all('div', class_='item-cell')
        newegg_data = defaultdict(dict)
        
        count = 0
        for product in product_list:
            # Product name
            name = product.find('a', class_='item-title')
            newegg_data[count]['item_name'] = name.get_text(strip=True) if name else 'Unavailable'
            
            # Product rating
            rating = product.find('a', class_='item-rating')
            newegg_data[count]['item_rating'] = rating['title'] if rating else 'Unavailable'

            # Product price
            price_whole = product.find('li', class_='price-current')
            if price_whole:
                price = price_whole.find('strong').get_text(strip=True) if price_whole.find('strong') else 'Unavailable'
                newegg_data[count]['item_price'] = price.replace(',', '')
            else:
                newegg_data[count]['item_price'] = 'Unavailable'
            
            # Product link
            link = name['href'] if name else None
            newegg_data[count]['item_link'] = link if link else 'Unavailable'

            # Product image
            image = product.find('img', class_='lazy-img')
            newegg_data[count]['item_image'] = image['data-src'] if image else 'Unavailable'

            count += 1
            if count == total_products_count:
                return newegg_data

        return newegg_data

    except Exception as e:
        print(f"Error fetching Newegg India data: {e}")
        return {}
