import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def search_flipkart(product, total_products_count):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        url = f"https://www.flipkart.com/search?q={'+'.join(product.split())}"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        response.close()

        all_divs = soup.find_all('div', {'class': 'bhgxx2 col-12-12'})[2:-2]
        flipkart_products_data = defaultdict(dict)

        regex = re.compile("^[a-zA-z]*")
        count = 0
        for div in all_divs:
            for item_div in soup.find_all("div", {"data-id": regex}):
                item_name = item_div.find('img')['alt'].strip() if item_div.find('img') else "Unavailable"
                flipkart_products_data[count]['item_name'] = item_name

                # Get the rating
                item_rating = item_div.find('span', {'id': re.compile("^productRating_")})
                flipkart_products_data[count]['item_rating'] = "".join([item_rating.get_text().strip(), '/5']) if item_rating else 'Unavailable'

                # Get the price
                item_price = item_div.get_text().strip()
                price_index = item_price.find('₹')
                if price_index == -1:
                    flipkart_products_data[count]['item_price'] = 'Unavailable'
                else:
                    price = ''.join(filter(str.isdigit, item_price[price_index + 1:]))
                    flipkart_products_data[count]['item_price'] = price

                # Get the link
                item_link = item_div.find("a", {"href": regex})
                flipkart_products_data[count]['item_link'] = 'https://www.flipkart.com' + item_link['href'] if item_link else 'Unavailable'

                # Get the image link
                item_image = item_div.find('img')['src'] if item_div.find('img') else 'Unavailable'
                flipkart_products_data[count]['item_image'] = item_image

                count += 1
                if count == total_products_count:
                    return flipkart_products_data

        return flipkart_products_data

    except Exception as e:
        print(f"Error fetching Flipkart data: {e}")
        return {}
