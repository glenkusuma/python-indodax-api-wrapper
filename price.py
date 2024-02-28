"""
Module: price.py
Author: Mame29

This module provides a price class retrieving the price of a cryptocurrency 
in Indonesian Rupiah (IDR) from the Indodax API.
"""
import time
import requests as rq

class Price:
    """
    A class for retrieving the price of a cryptocurrency in 
    Indonesian Rupiah (IDR) from the Indodax API.
    """

    @staticmethod
    def price(coin, timeout=30):
        """
        Retrieve the price of a cryptocurrency in Indonesian Rupiah (IDR) from the Indodax API.

        Args:
            coin (str): The symbol of the cryptocurrency (e.g., 'btc', 'eth').
            timeout (int, optional): The maximum time to wait for the server to respond,
            in seconds. Defaults to 30.

        Returns:
            dict: A dictionary containing the response JSON from the API.
        """
        while True:
            try:
                m = coin + 'idr'
                url = 'https://indodax.com/api/ticker/' + m
                r = rq.get(url, timeout=timeout)
                return r.json()

            except rq.exceptions.ConnectionError:
                time.sleep(5)
                continue
