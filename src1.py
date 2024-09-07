import json
import logging
import os
import re
import smtplib
from email.message import EmailMessage
from time import sleep

# import schedule
import schedule
from pprint import pprint
from requests import Session
from requests.exceptions import ConnectionError, Timeout, RequestException

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

currencies = {
    'USD': 'Dólar Americano',
    'EUR': 'Euro',
    'GBP': 'Libra Esterlina Britânica',
    'BRL': 'Real do Brasil',
    'TWD': 'Novo Dólar Taiwanês',
    'KRW': 'Won Sul-Coreano',
    'JPY': 'Iene japonês',
    'RUB': 'Rublo Russo',
    'CNY': 'Yuan chinês',
    'AUD': 'Dólar Australiano',
    'CAD': 'Dólar Canadense',
    'IDR': 'Rúpia Indonésia'
}

def instructions():
    print("Choose the currency you want to track the Bitcoin price in: ")
    print("\n")
    for code, name in currencies.items():
        print(f"{code}: {name}")

def get_currency_choice():
    while True:
        print("\n")
        currency_code = input(f"{GREEN}{BOLD}Type the coin code (or 'exit' to close the program): {RESET}").upper()
        print("\n")
        if currency_code == 'EXIT':
            return None
        if currency_code in currencies:
            return currency_code
        else:
            print("Código de moeda inválido. Tente novamente.")

def configure_logging() -> None:
    """Configure logging settings."""
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    sleep(1.5)

def fetch_bitcoin_price(currency_code='USD') -> float | None:
    """Fetch the current Bitcoin price from the CoinMarketCap API."""
    API_KEY: str | None = os.getenv('API_KEY')
    print(f"{YELLOW}Fetching Bitcoin price...{RESET}")
    sleep(1)

    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters: dict[str, str] = {'id': '1', 'convert': currency_code}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        response.raise_for_status()
        data = json.loads(response.text)
        return data['data']['1']['quote'][currency_code]['price']
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
        if re.findall(r"@.{1,8}\.com", email) or re.findall(r"@.{1,8}\.com.br", email):
            return email
        print(f"{RED}{BOLD}Invalid e-mail address, please try again.{RESET}")

def get_specified_price(currency) -> str:

  try:
    specified_price = float(input(f"Please enter the price you want to track in {currencies[currency]}: "))
    print("\n")
    if specified_price <= 0:
      print(f"{RED}{BOLD}Please enter a valid price.{RESET}")
      print(f'{YELLOW}Please, follow the instructions above!{RESET}\n')

      return get_specified_price()

  except ValueError:
    print(f"{RED}{BOLD}Please enter a valid price.{RESET}")
    print(f'{YELLOW}Please, follow the instructions above!{RESET}\n')

    return get_specified_price()

  return specified_price

def main() -> None:
    """Main function to track Bitcoin price and send email notifications."""

    print(f'{GREEN}{BOLD} Please, follow the instructions below to configure the Bitcoin price tracker.{RESET}\n')
    print(f' Enter the price in this format, example: {GREEN}{BOLD}50000{RESET}')
    print(f' Enter your e-mail in the format:{GREEN}{BOLD} youremail@gmail.com\n{RESET}')

    instructions()
    currency_choice = get_currency_choice()
    specified_price = get_specified_price(currency_choice)  

    if currency_choice:
        price = fetch_bitcoin_price(currency_choice)
        if price <  specified_price:
            print(f"{GREEN}The current price is lower than the specified price.{RESET}")
            print('\n')
            recipient_email = verify_email()
            send_email(price, specified_price, recipient_email)
            sleep(1.5)
            print(f"{GREEN}E-mail sent successfully.{RESET}\n")
        else:
            print(f"{YELLOW}The current price is higher than the specified price.{RESET}\n")

def schedule_email(min_time: int = 10) -> None:
    """Schedule the email sending function to run at regular intervals."""
    schedule.every(min_time).minutes.do(main)
