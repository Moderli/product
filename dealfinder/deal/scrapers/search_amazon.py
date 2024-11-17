import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from random import choice
import re

def search_amazon(product, total_products_count):
    try:
        # Define headers for request
        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        user_agent = choice(user_agent_list)
        headers = {"User-Agent": user_agent}

        word_list = product.replace(' ', '+')
        url = 'https://www.amazon.in/s?k=' + word_list
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find_all('span', {'cel_widget_id': re.compile("^MAIN-SEARCH_RESULTS")})
        
        amazon_products_data = defaultdict(dict)
        count = 0
        for item_div in main_div:
            # Skip sponsored items
            sponsored_div = item_div.find('div', {'data-component-type': 'sp-sponsored-result'})
            if sponsored_div:
                continue

            item_name = item_div.find('img')['alt']
            if not item_name:
                continue
            amazon_products_data[count]['item_name'] = item_name.strip().replace(u'\xa0', u' ')

            # Get the rating
            item_rating = item_div.find('span', {'class': 'a-declarative'})
            amazon_products_data[count]['item_rating'] = item_rating.get_text().strip() if item_rating else 'Unavailable'

            # Get the price
            item_price = item_div.find('span', {'class': 'a-price-whole'})
            amazon_products_data[count]['item_price'] = item_price.get_text().strip().replace(',', '') if item_price else 'Unavailable'

            # Get the link
            item_link = item_div.find('a', {'class': 'a-link-normal a-text-normal'})
            amazon_products_data[count]['item_link'] = "".join(['https://www.amazon.in', item_link['href']]) if item_link else 'Unavailable'

            # Get the image URL
            item_image = item_div.find('img')['src'] if item_div.find('img') else 'Unavailable'
            amazon_products_data[count]['item_image'] = item_image

            count += 1
            if count == total_products_count:
                return amazon_products_data

        return amazon_products_data

    except Exception as e:
        print(f"Error fetching Amazon data: {e}")
        return {}
