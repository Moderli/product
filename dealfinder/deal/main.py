# main.py
from scrapers import search_amazon, search_flipkart, search_mdcomputers, search_neweggindia, search_primeabgb, search_theitdepot

product = "graphics card"
total_products_count = 5

amazon_data = search_amazon(product, total_products_count)
flipkart_data = search_flipkart(product, total_products_count)
mdcomputers_data = search_mdcomputers(product, total_products_count)
neweggindia_data = search_neweggindia(product, total_products_count)
primeabgb_data = search_primeabgb(product, total_products_count)
theitdepot_data = search_theitdepot(product, total_products_count)

# Print data from each scraper for testing
print("Amazon Data:", amazon_data)
print("Flipkart Data:", flipkart_data)
print("MDComputers Data:", mdcomputers_data)
print("Newegg India Data:", neweggindia_data)
print("PrimeABGB Data:", primeabgb_data)
print("The IT Depot Data:", theitdepot_data)
