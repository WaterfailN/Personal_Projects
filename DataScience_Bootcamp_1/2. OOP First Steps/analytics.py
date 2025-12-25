import sys
import os
from random import randint
import logging
import requests
import json


class Research:
    def __init__(self, has_header=True):
        logging.info("Initializing Research class")
        if len(sys.argv) > 1:
            self.path = sys.argv[1]
        else:
            self.path = "../ex00/data.csv"
            logging.warning("No file path provided, using default 'data.csv'")

        self.has_header = has_header  # Нужен для кастомной настройки и более удобной проверки

        if not os.path.exists(self.path):
            logging.error(f"File not found: {self.path}")
            raise FileNotFoundError(f"File not found: {self.path}")

        # Есть ли заголовок
        with open(self.path, "r") as file:
            header = file.readline()
            if header == "1,0" or header == "0,1":
                self.has_header = False
                logging.debug("Header auto-detected as data line")
            else:
                logging.debug(f"Header detected: {header}")

    def file_reader(self):
        logging.info(f"Reading file: {self.path}")

        # Сбор информации
        with open(self.path, "r") as file:
            lines = file.readlines()
            lines = [l.strip() for l in lines]

        logging.debug(f"Read {len(lines)} lines from file")

        # Проверка на заголовок
        if len(lines[0].split(',')) != 2 and self.has_header:
            logging.error(f"Invalid header format in line 0: {lines[0]}")
            raise ValueError("Invalid header format. Expected two comma-separated values")

        # Проверка на внутренности
        start_idx = 1 if self.has_header else 0
        for i, line in enumerate(lines[start_idx:], start_idx + 1):
            line = line.strip()
            if not line:
                logging.error(f"Empty line at line {i}")
                raise ValueError(f"Empty line at line {i}")

            if line != "0,1" and line != "1,0":
                logging.error(f"Invalid line at line {i}: {line}")
                raise ValueError(f"Invalid line at line {i}")

        logging.info(f"Successfully read and validated {len(lines[start_idx:])} data lines")
        return lines

    @staticmethod
    def send_telegram_message(message, config):
        logging.info("Attempting to send Telegram message")

        try:
            if not config.telegram_bot_token or not config.telegram_chat_id:
                logging.warning("Telegram credentials not configured")
                return False

            url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"

            payload = {
                "chat_id": config.telegram_chat_id,
                "text": message,
                "parse_mode": "HTML"
            }

            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()

            logging.info(f"Telegram message sent successfully: {message}")
            return True

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error sending Telegram message: {e}")
            return False

    class Calculations:
        def __init__(self, data):
            logging.info("Initializing Calculations class with data")
            self.data = data
            self.counts_arg = tuple(self.counts())
            logging.debug(f"Counts calculated: {self.counts_arg}")

        # Решил не переводить в инты, а сразу со строкой работать
        def counts(self):
            logging.info("Calculating the counts of heads and tails")
            heads, tails = 0, 0
            for line in self.data:
                if line.startswith("1"):
                    heads += 1
                elif line.startswith("0"):
                    tails += 1
            logging.debug(f"Heads: {heads}, Tails: {tails}")
            return heads, tails

        def fractions(self):
            logging.info("Calculating fractions of heads and tails")
            heads, tails = self.counts_arg
            total = heads + tails
            if total == 0:
                logging.warning("No data available for fraction calculation")
                return 0, 0

            fractions = (round(heads / total, 4), round(tails / total, 4))
            logging.debug(f"Fractions: heads={fractions[0]}, tails={fractions[1]}")
            return fractions


class Analytics(Research.Calculations):
    def __init__(self, data):
        logging.info("Initializing Analytics class with data")
        super().__init__(data)
        logging.debug(f"Analytics initialized with {len(data)} data points")

    def predict_random(self, n):
        logging.info(f"Generating {n} random predictions")
        preds = []
        for i in range(n):
            heads = randint(0, 1)
            tails = -heads + 1
            preds.append([heads, tails])
            logging.debug(f"Prediction {i + 1}: heads={heads}, tails={tails}")
        logging.info(f"Generated {len(preds)} predictions")
        return preds

    def predict_last(self):
        logging.info("Getting last prediction from data")
        last_pred = self.data[-1]
        logging.debug(f"Last prediction: {last_pred}")
        return last_pred

    def save_file(self, data, filename, extension='txt'):
        logging.info(f"Saving data to file: {filename}.{extension}")
        full_filename = f"{filename}.{extension}"
        try:
            with open(full_filename, "w") as file:
                file.write(data)
            logging.info(f"File saved successfully: {full_filename}")
            return full_filename
        except Exception as e:
            logging.error(f"Failed to save file {full_filename}: {e}")
            raise

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('analytics.log'),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging system initialized")

setup_logging()