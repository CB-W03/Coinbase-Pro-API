import pandas as pd
import cbpro

api_secret = "YOUR API SECRET"
api_key = "YOUR API KEY"
api_pass = "YOUR PASSPHRASE"


class TextWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        self.message_count = 0

    def on_message(self, msg):
        self.message_count += 1
        msg_type = msg.get('type', None)
        if msg_type == 'ticker':
            time_val = msg.get('time',('-'*27))
            price_val = msg.get('price',None)
            price_val = float(price_val) if price_val is not None else 'None'
            product_id = msg.get('product_id', None)

            print(f"{time_val:30} {price_val:3f} {product_id}\tchannel type:{msg_type}")

    def on_close(self):
        print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_count}")


stream = TextWebsocketClient(products=['BTC-USD'],channels=['ticker'])
stream.start()
stream.close()

url = 'https://api-public.sandbox.pro.coinbase.com'
client = cbpro.AuthenticatedClient(api_key,
                                   api_secret,
                                   api_pass,
                                   api_url=url)
payment_methods = client.get_payment_methods()
for method in payment_methods:
    currency = method.get('currency', None)
    if currency.upper() == 'USD':
        method_id = method.get('id', None)
    elif currency is None:
        continue
print(f"Currency is `{currency}`\n")

#client.place_market_order(product_id='BTC-USD', side='buy', size=1)

accounts = client.get_accounts()

for acc in accounts:
    currency = acc.get('currency')
    if currency=='BTC':
        acc_id = acc.get('id')

acc_history = client.get_account_history(acc_id)

import json
for hist in acc_history:
    print(json.dumps(hist, indent=1))
