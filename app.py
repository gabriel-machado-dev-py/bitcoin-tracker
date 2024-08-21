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

# Adding my own style to the project
def simulate_loading_bar() -> None:
    """Simulate a loading bar with a progress indicator."""
    print(f"{GREEN}Loading program...{RESET}")
    print(f"{YELLOW + BOLD}Wait!{RESET}\n")
    sleep(1.5)

    for _ in tqdm(range(100), desc="Loading", ncols=75):
        sleep(0.02)

    print(CYAN + BOLD + r'''
                    █████████████████████████████████████████████████████████████
                    ████                                                   ████
                    ████                                                   ████
                    ████                                                   ████
                    ████                                                   ████
                          ██████╗ ███████╗██╗   ██╗       ██████╗ ██╗   ██╗
                          ██╔══██╗██╔════╝██║   ██║       ██╔══██╗╚██╗ ██╔╝
                          ██║  ██║█████╗  ██║   ██║       ██████╔╝ ╚████╔╝
                          ██║  ██║██╔══╝  ╚██╗ ██╔╝       ██╔═══╝   ╚██╔╝
                          ██████╔╝███████╗ ╚████╔╝     ██╗██║        ██║
                          ╚═════╝ ╚══════╝  ╚═══╝      ╚═╝╚═╝        ╚═╝
                    ████                                                   ████
                    ████                                                   ████
                    ████                                                   ████
                    ████             Bitcoin Advanced Tracker              ████
                    █████████████████████████████████████████████████████████████

    ''' + RESET)

# Configure logging in case of errors
def configure_logging() -> None:
    """Configure logging settings."""
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    sleep(1.5)

# Fetch the current Bitcoin price from the CoinMarketCap API
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

# Send an email notification with the current Bitcoin price
def send_email(current_price: float, specified_price: float, recipient_email: str) -> None:
    """Send an email notification with the current Bitcoin price."""
    print(f"{YELLOW}Creating e-mail...{RESET}")
    sleep(1)

    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    if not EMAIL_USER or not EMAIL_PASSWORD:
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

# Main function to track Bitcoin price and send email notifications
def main() -> None:
    """Main function to track Bitcoin price and send email notifications."""
    specified_price = float(input("Please enter the price you want to track (USD): "))
    recipient_email: str = input("Please enter your e-mail address: ")

    print(f'{YELLOW}Verify if the email {recipient_email} is correct.{RESET}\n')
    valid_email = input('Is the email correct? (y/n): ')
    if valid_email.lower() == 'n':
        recipient_email = input('Please enter your e-mail address: ')
    print(f'{RED}{BOLD}If the email is incorrect, you will not receive the e-mail.{RESET}')
    sleep(5)

    current_price = fetch_bitcoin_price()

    if current_price is not None:
        if current_price < specified_price:
            print(f"{GREEN}The current price is lower than the specified price.{RESET}")
            send_email(current_price, specified_price, recipient_email)
            sleep(1.5)
            print(f"{GREEN}E-mail sent successfully.{RESET}")
        else:
            sleep(1.5)
            print(f"{GREEN}{BOLD}The current price is higher than the specified price. ${current_price:.2f}{RESET}")
            sleep(5)
    else:
        print(f"{RED}{BOLD}Failed to fetch the current price of Bitcoin.{RESET}")
        sleep(5)

# Schedule the email sending function to run at regular intervals (every 10 minutes)
def schedule_email(min_time: int = 10) -> None:
    """Schedule the email sending function to run at regular intervals."""
    schedule.every(min_time).minutes.do(main)

# Run the main function
if __name__ == "__main__":
    load_dotenv()
    simulate_loading_bar()
    configure_logging()
    main()
    schedule_email()
    schedule_time: str = input("The bot is programmed to run every 10 minutes, do you wish to cancel or not? (y/n): ")
    if schedule_time.lower() == 'y':
        schedule.clear()
        print(f"{RED}{BOLD}The bot has been canceled.{RESET}")
        sleep(5)
    else:
        print(f"{GREEN}{BOLD}The bot will continue to run every 10 minutes.{RESET}")
        while True:
            schedule.run_pending()
            sleep(1)
