import json
import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime


def testMonitor(shop_name):

    resp = requests.request("GET", url=f'https://{shop_name}.com/products.json')
    data = json.loads(resp.text)
    products = (data['products'])

    newProductFound(products[0], shop_name)



def monitor(shop_name, refresh_delay):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] Starting shopify-{shop_name} monitor | delay: {refresh_delay} second(s)...')

    resp = requests.request(
        "GET", url=f'https://{shop_name}.com/products.json')
    data = json.loads(resp.text)
    products = (data['products'])

    links = []
    # initial collection
    for product in products:
        links.append(product['handle'])

    # load proxies.txt
    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]
    f.close()

    # check to see if proxies.txt is empty
    if len(proxies) == 0:
        print("\n• Proxies are required to avoid shopify temp bans\n• Please add proxies to proxies.txt")

    proxy_counter = 0
    # monitor for new products
    while(proxy_counter <= len(proxies)-1):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] [{proxies[proxy_counter]}] Waiting for new product...')

        active_proxy = {'https': 'https://'+proxies[proxy_counter]}

        resp = requests.request("GET", url=f'https://{shop_name}.com/products.json',proxies=active_proxy)
        data = json.loads(resp.text)
        products = (data['products'])

        for product in products:
            if product['handle'] not in links:
                newProductFound(product, shop_name)
                links.append(product['handle'])

        time.sleep(refresh_delay)

        # rotate proxy
        if proxy_counter == len(proxies)-1:
            proxy_counter = 0
        else:
            proxy_counter+=1



def newProductFound(product_data, shop_name):
    # parse product data
    product_title = (product_data['title'])
    product_link = (f'https://{shop_name}.com/products/'+product_data['handle'])
    product_image = (product_data['images'][0]['src'])

    # parse variant data
    variants = product_data['variants']
    price = ('$'+variants[0]['price'])
    sizes = {}
    for variant in variants:
        variant_size = variant['title']
        variant_id = variant['id']
        sizes[str(variant_size)] = variant_id

    quick_task = f'[QuickTask](https://cybersole.io/dashboard/tasks?quicktask={product_link})'

    # build size string
    size_string = ''
    odd_count = 1
    for i in range(len(sizes)):
        size = str(list(sizes.keys())[i])
        id = str(list(sizes.values())[i])
        size_string += f'[{size}]' + f'(https://{shop_name}.com/cart/add/{id})\n'
    size_string += f'\n[QuickTask](https://cybersole.io/dashboard/tasks?quicktask={product_link})'
        
    # send discord notification
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/794705536783613992/RzttvPIL-mDCd00AUh7ArNTRrTCg20EmatzqIAoAFjMY1w1pjorNmapr5AVIng7UvxD2')
    embed = DiscordEmbed(title=product_title, url=product_link, color=0x35e811)
    embed.set_thumbnail(url=product_image)
    embed.add_embed_field(name=price, value=size_string, inline=True)
    embed.set_footer(text=f'shopify-{shop_name} | made by bard#1704')
    webhook.add_embed(embed)
    webhook.execute()


# production function
# Stores: prosperskateshop, kith, undefeated...
monitor('prosperskateshop', 1)

# test function
#testMonitor('prosperskateshop')

