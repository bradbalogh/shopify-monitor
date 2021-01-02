import json
import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed


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
    price = ('$'+variants[0]['price'])
    sizes = {}
    for variant in variants:
        variant_size = variant['title']
        variant_id = variant['id']
        sizes[str(variant_size)] = variant_id

    print(sizes)

    # /cart/add/id
    # build size string
    size_string = ''
    odd_count = 1
    for i in range(len(sizes)):
        size = str(list(sizes.keys())[i])
        id = str(list(sizes.values())[i])
        size_string += f'[{size}]' + f'(https://{shop_name}/cart/add/{id})\n'
        # if odd_count%2 == 0:
        #     size_string+='\n'
        # else:
        #     size_string+='\t'
        # odd_count+=1
        

    # send discord notification
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/794705536783613992/RzttvPIL-mDCd00AUh7ArNTRrTCg20EmatzqIAoAFjMY1w1pjorNmapr5AVIng7UvxD2')
    embed = DiscordEmbed(title=product_title, url=product_link, color=0x35e811)
    embed.set_thumbnail(url=product_image)
    embed.add_embed_field(name=price, value='---------', inline=False)
    embed.add_embed_field(name='Sizes:', value=size_string, inline=False)
    embed.set_footer(text="CyberQuickTask")
    webhook.add_embed(embed)
    webhook.execute()



#monitor('prosperskateshop', 4000)
testMonitor('prosperskateshop')

