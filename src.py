import json
import logging
import os
import smtplib
from email.message import EmailMessage
from time import sleep

import schedule
from dotenv import load_dotenv
from pprint import pprint
from requests import Session
from requests.exceptions import ConnectionError, Timeout, RequestException
from tqdm import tqdm

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(CYAN + BOLD + r'''

      ░█▀▄░▀█▀░▀█▀░█▀▀░█▀█░▀█▀░█▀█░░░█▀█░█▀▄░▀█▀░█▀▀░█▀▀░░░▀█▀░█▀▄░█▀█░█▀▀░█░█░█▀▀░█▀▄
      ░█▀▄░░█░░░█░░█░░░█░█░░█░░█░█░░░█▀▀░█▀▄░░█░░█░░░█▀▀░░░░█░░█▀▄░█▀█░█░░░█▀▄░█▀▀░█▀▄
      ░▀▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀

    ''' + RESET)

def configure_logging() -> None:
    """Configure logging settings."""
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    sleep(1.5)

def fetch_bitcoin_price() -> float | None:
    """Fetch the current Bitcoin price from the CoinMarketCap API."""
    API_KEY: str | None = os.getenv('API_KEY')
    print(f"{YELLOW}Fetching Bitcoin price...{RESET}")
    sleep(1)

    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters: dict[str, str] = {'id': '1'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        response.raise_for_status()
        data = json.loads(response.text)
        return data['data']['1']['quote']['USD']['price']
    except (ConnectionError, Timeout, RequestException) as e:
        logging.error(f"Error fetching Bitcoin price: {e}")
        pprint(e)
    return None

def send_email(current_price: float, specified_price: str, recipient_email: str) -> None:
    """Send an email notification with the current Bitcoin price."""
    print(f"{YELLOW}Creating e-mail...{RESET}")
    sleep(1)

    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    if not EMAIL_USER or not EMAIL_PASSWORD:
        logging.error("Environment variables EMAIL_USER and EMAIL_PASSWORD were not found.")
        raise EnvironmentError("Environment variables EMAIL_USER and EMAIL_PASSWORD were not found.")


    msg = EmailMessage()
    msg['Subject'] = 'Bitcoin Price Report'
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email
    msg.add_header('Content-Type', 'text/html')

    message: str = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Preço do Bitcoin</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 80%;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
            }}
            p {{
                font-size: 16px;
                color: #555;
            }}
            .price {{
                font-size: 24px;
                color: #d9534f;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Relatório de Preço do Bitcoin</h1>
            <p>Olá,</p>
            <p>O preço do Bitcoin caiu abaixo do valor especificado.</p>
            <p>Preço atual: <span class="price">{current_price:.2f}</span></p>
            <p>Valor especificado: <span class="price">{specified_price}</span></p>
            <p>Por favor, tome as medidas necessárias.</p>
            <p>Atenciosamente,</p>
            <p>Equipe de Rastreamento de Criptomoedas</p>
        </div>
    </body>
    </html>
    """
    msg.set_payload(message.encode('utf-8'))

    print(f"{GREEN}E-mail created!!!{RESET}")
    sleep(1.5)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
            sleep(1.5)
    # Main exceptions
    except smtplib.SMTPRecipientsRefused as e:
        logging.error(f"The e-mail typed is invalid, please check the e-mail and try again: {e}")
        print(f"{RED}{BOLD}The e-mail typed is invalid, please check the e-mail and try again: {recipient_email}{RESET}")
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Failed to authenticate with the email server: {e}")
        print(f"Failed to authenticate with the email server: {EMAIL_USER}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while sending email: {e}")
        print(f"An unexpected error occurred while sending email: {e}")

def verify_email() -> str:
    """Verify if the email is valid."""
    while True:
        email = input("Please enter your e-mail address: ")
        print("\n")
        if "@" in email and "." in email:
            return email
        print(f"{RED}{BOLD}Invalid e-mail address, please try again.{RESET}")

def get_specified_price() -> str:
  specified_price = input("Please enter the price you want to track (USD): ")

  if specified_price == "" or specified_price == "0":
      print(f"{RED}{BOLD}Please enter a valid price.{RESET}")
      specified_price = input("Please enter the price you want to track (USD): " + "\n")

  return float(specified_price)

def main() -> None:
    """Main function to track Bitcoin price and send email notifications."""

    print(f'{GREEN}{BOLD} Please, follow the instructions below to configure the Bitcoin price tracker.{RESET}\n')
    print(f'{YELLOW} Enter the price in USD in the format without the dollar sign, example: {GREEN}{BOLD}50000{RESET}')
    print(f'{YELLOW} Enter your e-mail in the format:{RESET} {GREEN}fulanodetal@gmail.com{RESET}\n')

    specified_price = get_specified_price()
    recipient_email = verify_email()
    current_price = fetch_bitcoin_price()


    if current_price is not None:
        if current_price < specified_price:
            print(f"{GREEN}The current price is lower than the specified price.{RESET}")
            send_email(current_price, specified_price, recipient_email)
            sleep(1.5)
            print(f"{GREEN}E-mail sent successfully.{RESET}\n")
        else:
            sleep(1.5)
            print(f"{GREEN}{BOLD}The current price is higher than the specified price. ${current_price:.2f}{RESET}\n")
            sleep(5)
    else:
        print(f"{RED}{BOLD}Failed to fetch the current price of Bitcoin.{RESET}")
        sleep(5)

def schedule_email(min_time: int = 10) -> None:
    """Schedule the email sending function to run at regular intervals."""
    schedule.every(min_time).minutes.do(main)
