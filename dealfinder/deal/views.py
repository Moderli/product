from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .scrapers import search_amazon, search_flipkart, search_mdcomputers, search_neweggindia, search_primeabgb, search_theitdepot
import pprint
from collections import defaultdict

@login_required
def product_search(request):
    if request.method == 'GET':
        # Get the product name and count from the form inputs or set defaults
        product = request.GET.get('product', '')  # Default to an empty string if no product is provided
        total_products_count = int(request.GET.get('count', 10))  # Default to 10 products if count isn't specified

        if product:  # If a product name is provided in the search query
            # Call search functions for different e-commerce websites
            amazon_data = search_amazon(product, total_products_count)
            flipkart_data = search_flipkart(product, total_products_count)
            mdcomputers_data = search_mdcomputers(product, total_products_count)
            neweggindia_data = search_neweggindia(product, total_products_count)
            primeabgb_data = search_primeabgb(product, total_products_count)
            theitdepot_data = search_theitdepot(product, total_products_count)

            # Flatten defaultdict data into lists
            def flatten_data(data):
                if isinstance(data, defaultdict):
                    return [v for k, v in data.items()]  # Convert defaultdict to a list of values
                return data  # In case it's not defaultdict, return the data as is

            master_data = {
                'amazon': flatten_data(amazon_data),
                'flipkart': flatten_data(flipkart_data),
                'mdcomputers': flatten_data(mdcomputers_data),
                'neweggindia': flatten_data(neweggindia_data),
                'primeabgb': flatten_data(primeabgb_data),
                'theitdepot': flatten_data(theitdepot_data),
            }

            pprint.pprint(master_data)  # Debugging: check if data is in the expected format

            return render(request, 'query_page.html', {'master_data': master_data, 'product': product, 'count': total_products_count})

        else:
            # If no 'product' parameter is provided, render the query page with the search form only
            return render(request, 'query_page.html')

    return render(request, 'query_page.html')  # Default case


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)  # Logs the user out
    return redirect('/')  # Redirect to home page or any page you wan