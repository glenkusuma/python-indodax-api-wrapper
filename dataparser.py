"""
Module: dataparser.py
Author: GlenKusuma

This module provides a DataParser class for parsing trade history data 
and converting it to CSV format.
"""

import datetime
import time
import math
import os
import pandas as pd


class DataParser:
    """
    A class for parsing trade history data and converting it to CSV format.
    """

    class TradeHistory:
        """
        A nested class for processing trade history data.
        """

        def __init__(self):
            pass

        def json_to_csv(self, trade_history, output_folder):
            """
            Parses trade history data and saves it as a CSV file.

            Args:
                trade_history (dict): The trade history data.
                output_folder (str): The path to the output folder where the CSV file will be saved.

            Returns:
                str: The file path of the saved CSV file.
            """
            # Creating DataFrame from json data
            df = pd.DataFrame(data=trade_history["return"]["trades"])

            # Generating filename for the CSV file
            filename = (
                "trade-history-indodax-"
                + df["pair"][0].replace("_", "")
                + f"-{datetime.date.today()}-{int(time.time())}.csv"
            )

            # Getting the absolute path of the output folder
            output_folder_abs = os.path.abspath(output_folder)

            # Creating output folder if it does not exist
            if not os.path.exists(output_folder_abs):
                os.makedirs(output_folder_abs)

            # Creating full path for the CSV file
            filepath = os.path.join(output_folder_abs, filename)

            # Converting columns to appropriate data types
            df = df.astype(
                {
                    "currency": str,
                    "pair": str,
                    "trade_id": int,
                    "order_id": int,
                    "type": str,
                    df.columns[5]: float,
                    "price": float,
                    "fee": float,
                    "trade_time": object,
                    "client_order_id": str,
                }
            )

            # Calculating IDR column
            df["IDR"] = df.apply(
                lambda row: math.floor(row[df.columns[5]] * round(row["price"], 9)),
                axis=1,
            )

            # Mapping 'type' column to 'beli' or 'jual'
            df["type"] = df.apply(
                lambda row: "beli" if row["type"] == "buy" else "jual", axis=1
            )

            # Selecting required columns and renaming them
            df = df[["trade_time", "type", "price", "IDR", df.columns[5], "fee"]]
            df["trade_time"] = (
                pd.to_datetime(df["trade_time"], unit="s")
                .dt.tz_localize("UTC")
                .dt.tz_convert("Asia/Jakarta")
                .dt.strftime("%Y-%m-%d %H:%M:%S")
            )
            df = df.rename(
                columns={
                    "trade_time": "WAKTU",
                    "type": "TIPE",
                    df.columns[-2]: df.columns[-2].upper(),
                    "price": "HARGA",
                    "fee": "FEE",
                }
            )

            # Saving DataFrame to CSV
            df.to_csv(filepath, index=False, encoding="utf-8")

            # Returning the filepath
            return filepath

    def __init__(self):
        self.trade_history = self.TradeHistory()


# Example usage
if __name__ == "__main__":
    parser = DataParser()
    trade_history_data = {
        "return": {
            "trades": [{"pair": "ETH_USD", "price": 2000, "trade_time": 1646612345}]
        }
    }
    OUTPUT_FOLDER = "output"
    file_path = parser.trade_history.json_to_csv(trade_history_data, OUTPUT_FOLDER)
    print("CSV File saved at:", file_path.replace("\\", "/"))
