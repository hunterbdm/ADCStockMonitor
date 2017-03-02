from colorama import Fore, init, Style
import requests
import os
import time
from pygame import mixer


clear = lambda: os.system('cls')


def print_(output):
    print(Style.RESET_ALL + output)


def main():
    init()
    print_(Fore.WHITE + 'Adidas.com Stock Monitor - @hunter_bdm')
    while True:
        try:
            sku = input('Enter SKU: ')
            sleep_t = int(input('Enter sleep time: '))
            break
        except:
            clear()
            print_('Invalid Input')

    url = 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Product-GetAvailableSizes?pid=' + sku

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    loaded = False
    starting_stock = 0

    while True:
        resp = requests.get(url, headers=headers)
        JSON = resp.json()['sizes']

        clear()
        if len(JSON) == 0:
            loaded = False
            print_(Fore.WHITE + 'SKU Not Loaded')
        else:
            if not loaded:
                # Product was just loaded, maybe play sound or something
                print_(Fore.GREEN + 'STOCK LOADED')
                for size in JSON:
                    starting_stock += int(float(size['quantityAvailable']) if not size['quantityAvailable'] == 'null' else 0)
                try:
                    mixer.init()
                    mixer.music.load('alert.mp3')
                    mixer.music.play()
                except:
                    # This may not work on some OS's, not too big of a deal just a sound so pass.
                    pass
                loaded = True

            print_(Fore.WHITE + 'SKU         STATUS         SIZE  QUANTITY')
            print_(Fore.WHITE + '-----------------------------------------')
            current_stock = 0
            for size in JSON:
                if size['status'] == 'NOT_AVAILABLE':
                    print_('{}{:<12}{:<15}{:<6}{:>8}'.format(Fore.RED, size['sku'], size['status'], size['literalSize'], '0'))
                else:
                    print_('{}{:<12}{:<15}{:<6}{:>8}'.format(Fore.GREEN, size['sku'], size['status'], size['literalSize'], size['quantityAvailable']))
                    current_stock += int(float(size['quantityAvailable']) if not size['quantityAvailable'] == 'null' else 0)

            print_(Fore.WHITE + 'Starting Stock: ' + str(starting_stock))
            print_(Fore.WHITE + 'Current Stock:  ' + str(current_stock))

        time.sleep(sleep_t)

if __name__ == '__main__':
    main()