import json
import requests
import time


def testMonitor(shop_name):

    resp = requests.request(
        "GET", url=f'https://{shop_name}.com/products.json')
    data = json.loads(resp.text)
    products = (data['products'])

    newProductFound(products[0], shop_name)



def monitor(shop_name, refresh_delay):

    resp = requests.request(
        "GET", url=f'https://{shop_name}.com/products.json')
    data = json.loads(resp.text)
    products = (data['products'])

    links = []
    # initial collection
    for product in products:
        links.append(product['handle'])

    # monitor for new products
    while True:
        resp = requests.request(
            "GET", url=f'https://{shop_name}.com/products.json')
        data = json.loads(resp.text)
        products = (data['products'])

        links = []
        for product in products:
            if product['handle'] not in links:
                newProductFound(product, shop_name)
                links.append(product['handle'])

        time.sleep(refresh_delay)



def newProductFound(product_data, shop_name):
    # parse product data
    product_title = (product_data['title'])
    product_link = (f'https://{shop_name}.com/products/'+product_data['handle'])
    product_image = (product_data['images'][0]['src'])

    # parse variant data
    variants = product_data['variants']
    print('$'+variants[0]['price'])
    for variant in variants:
        variant_size = variant['title']
        variant_id = variant['id']
        print(f'[{variant_size}] {variant_id}')


def sendNotification():
    # send discord notification
    print("Sending Notification")



#monitor('prosperskateshop', 4000)
testMonitor('prosperskateshop')

