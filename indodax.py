"""
Modul: indodax.py
Penulis: Mame29

Modul ini menyediakan kelas price yang mengambil harga cryptocurrency 
dalam Rupiah Indonesia (IDR) dari API Indodax.
"""
import json
import time
import urllib
from hmac import HMAC
import requests as c
from price import Price

class Indodax:
    '''
    Ini dirancang agar mempermudah jual beli mata uang digital di Indodax. 
    Ambil key dan secret di akun Anda.
    >>> from Indodax import indodax
    >>> key = 'ABCD-EFGH-IJKL-MNOP' # Ambil dari akun Indodax Anda
    >>> secret = b'hiwiwijwjsjsjsj' # Ini juga sama
    >>> a = indodax(key, secret)
    >>> a.get_info() # Nanti akan muncul informasi saldo
    '''

    def __init__(self, key, secret):
        '''
        Inisialisasi instance ApiKeyManager.

        Args:
            key (str): Kunci dari Indodax.
            secret (bytes): Secret dari Indodax.
        '''
        # Kunci dari Indodax
        self.key = key
        # Secret dari Indodax
        self.secret = secret

    def query(self, method, **kwargs: dict):
        '''
        Mengirimkan permintaan ke API Indodax.

        Args:
            method (str): Metode yang akan dipanggil.
            **kwargs (dict): Argumen tambahan untuk permintaan.

        Returns:
            str: Respon dari API Indodax dalam bentuk JSON.
        '''
        url = 'https://indodax.com/tapi/'

        kwargs['method'] = method
        kwargs['nonce'] = int(time.time()*1000000)

        sign = HMAC(self.secret, urllib.parse.urlencode(kwargs).encode('utf-8'), 'sha512').hexdigest()
        headers = {
            'Sign': sign,
            'Key': self.key
        }

        s = c.Session()
        r = s.post(url, headers=headers, data=kwargs)
        js = json.dumps(json.loads(r.text), sort_keys=False, indent=4)
        return js

    def get_price(self, coin):
        '''
        Mengambil harga cryptocurrency dari API Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').

        Returns:
            dict: Dictionary yang berisi respons JSON dari API.
        '''
        a = Price.price(coin)
        return a

    def get_info(self):
        '''
        Mengambil informasi saldo dari akun Indodax.

        Returns:
            str: Informasi saldo dari akun Indodax.
        '''
        return self.query('getInfo')

    def history(self):
        '''
        Mengambil riwayat transaksi dari akun Indodax.

        Returns:
            str: Riwayat transaksi dari akun Indodax.
        '''
        return self.query('transHistory')

    def trade_history(self, coin, idr_or_btc='idr'):
        '''
        Mengambil riwayat perdagangan cryptocurrency dari akun Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Riwayat perdagangan cryptocurrency dari akun Indodax.
        '''
        pair = coin+'_'+idr_or_btc
        m = {'pair': pair}
        return self.query('tradeHistory', **m)

    def trade_buy(self, coin, diharga, jumlah, idr_or_btc='idr'):
        '''
        Melakukan pembelian cryptocurrency di Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            diharga (str): Harga pembelian cryptocurrency.
            jumlah (str): Jumlah cryptocurrency yang ingin dibeli.
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Respon dari API setelah melakukan pembelian.
        '''
        pair = coin+'_'+idr_or_btc
        m = {
            'pair': pair,
            'type': 'buy',
            'price': diharga,
            idr_or_btc: jumlah,
        }

        return self.query('trade', **m)

    def trade_sell(self, coin, diharga, jumlah, idr_or_btc='idr'):
        '''
        Melakukan penjualan cryptocurrency di Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            diharga (str): Harga penjualan cryptocurrency.
            jumlah (str): Jumlah cryptocurrency yang ingin dijual.
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Respon dari API setelah melakukan penjualan.
        '''
        pair = coin+'_'+idr_or_btc
        m = {
            'pair': pair,
            'type': 'sell',
            'price': diharga,
            coin: jumlah
        }

        return self.query('trade', **m)

    def open_order(self,coin, idr_or_btc='idr'):
        '''
        Mendapatkan daftar pesanan terbuka untuk cryptocurrency tertentu di Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Respon dari API yang berisi daftar pesanan terbuka.
        '''
        pair = coin+'_'+idr_or_btc
        m = {
            'pair': pair
        }

        return self.query('openOrders', **m)

    def order_history(self, coin, idr_or_btc='idr'):
        '''
        Mendapatkan riwayat pesanan untuk cryptocurrency tertentu di Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Respon dari API yang berisi riwayat pesanan.
        '''
        pair = coin+'_'+idr_or_btc
        m = {'pair': pair}

        return self.query('orderHistory', **m)

    def get_order(self, coin, order_id, idr_or_btc='idr'):
        '''
        Mendapatkan detail pesanan tertentu untuk cryptocurrency tertentu di Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            order_id (str): ID pesanan yang ingin dilihat detailnya.
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Respon dari API yang berisi detail pesanan.
        '''
        pair = coin+'_'+idr_or_btc
        m = {
            'pair': pair,
            'order_id': order_id
        }

        return self.query('getOrder', **m)

    def cancel_order_buy(self, coin, order_id, idr_or_btc='idr'):
        '''
        Membatalkan pesanan pembelian cryptocurrency tertentu di Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            order_id (str): ID pesanan pembelian yang ingin dibatalkan.
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Respon dari API setelah pembatalan pesanan.
        '''
        pair = coin+'_'+idr_or_btc
        m = {
            'pair': pair,
            'order_id': order_id,
            'type': 'buy'
        }
        return self.query('cancelOrder', **m)

    def cancel_order_sell(self, coin, order_id, idr_or_btc='idr'):
        '''
        Membatalkan pesanan penjualan cryptocurrency tertentu di Indodax.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            order_id (str): ID pesanan penjualan yang ingin dibatalkan.
            idr_or_btc (str, opsional): Unit pembayaran untuk harga (IDR atau BTC). Default 'idr'.

        Returns:
            str: Respon dari API setelah pembatalan pesanan.
        '''
        pair = coin+'_'+idr_or_btc
        m = {
            'pair': pair,
            'order_id': order_id,
            'type': 'sell'
        }

        return self.query('cancelOrder', **m)

    def withdraw(self, coin, address, amount, memo='', req_id=''):
        '''
        Menarik cryptocurrency tertentu dari akun Indodax ke alamat yang ditentukan.

        Args:
            coin (str): Simbol cryptocurrency (mis., 'btc', 'eth').
            address (str): Alamat tujuan penarikan cryptocurrency.
            amount (str): Jumlah cryptocurrency yang ingin ditarik.
            memo (str, opsional): Memo atau pesan tambahan untuk penarikan. Default ''.
            req_id (str, opsional): ID permintaan untuk penarikan. Default ''.

        Returns:
            str: Respon dari API setelah permintaan penarikan.
        '''
        m = {
            'currency': coin,
            'withdraw_address': address,
            'withdraw_amount': amount,
            'withdraw_memo': memo,
            'request_id': req_id
        }

        return self.query('withdrawCoin', **m)
