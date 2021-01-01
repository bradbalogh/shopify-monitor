import json
import requests
import time


def monitor(shop_name, refresh_delay):

    resp = requests.request("GET", url=f'https://{shop_name}.com/products.json')
    data = json.loads(resp.text)
    products = (data['products'])

    links = []
    # initial collection
    for product in products:
        links.append(product['handle'])


    # monitor for new products
    while True:
        resp = requests.request("GET", url=f'https://{shop_name}.com/products.json')
        data = json.loads(resp.text)
        products = (data['products'])

        links = []
        # initial collection
        for product in products:
            if product['handle'] not in links:
                newProductFound(product)
                links.append(product['handle'])

        time.sleep(refresh_delay)



def newProductFound(product_data):
    # parse data

    # send discord notification


# monitor(shop_name, refresh_delay)
monitor('prosperskateshop', 4000)



    # loop through all products
    # for product in products:
    #     product_title = (product['title'])
    #     product_link = (f'https://{shop_name}.com/products/'+product['handle'])
    #     print(f'{product_title} [{product_link}]')