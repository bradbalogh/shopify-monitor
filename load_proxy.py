
# load proxy file
with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]
f.close()

# cycle loaded proxies
proxy_counter = 0
while(proxy_counter <= len(proxies)-1):
    print(proxies[proxy_counter])
    if proxy_counter == len(proxies)-1:
        proxy_counter = 0
    else:
        proxy_counter+=1

