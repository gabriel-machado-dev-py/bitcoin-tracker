# Bitcoin Advanced Tracker

Bitcoin Advanced Tracker is a Python application that tracks the price of Bitcoin and sends email notifications when the price falls below a specified value. The application uses the CoinMarketCap API to fetch the current Bitcoin price and sends email notifications using the SMTP protocol.

## Features

- Fetches the current Bitcoin price from the CoinMarketCap API.
- Sends email notifications when the Bitcoin price falls below a specified value.
- Simulates a loading bar with a progress indicator.
- Configurable email credentials and API key using environment variables.
- Scheduled execution to check the Bitcoin price at regular intervals.

## Requirements

- Python 3.7+
- `requests` library
- `python-dotenv` library
- `tqdm` library
- `schedule` library

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/bitcoin-advanced-tracker.git
   cd bitcoin-advanced-tracker
   ```
2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```
3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your API key and email credentials.
``

   ```env
   API_KEY=your_coinmarketcap_api_key
   EMAIL_USER=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   ```
5. To get your e-mail password, follow the steps above.
   ```
   1. Go to your e-mail
   2. Go to: manage your google account
   3. Search for App password and create one
   4. Copy the code and paste it on your EMAIL_PASSWORD
   ```

* [ ] Usage

1. Run the application:

   ```sh
   python app.py
   ```
2. Follow the prompts to enter the price you want to track and your email address.
3. The application will fetch the current Bitcoin price and send an email notification if the price falls below the specified value.
4. The application will continue to run and check the Bitcoin price at regular intervals (every 10 minutes by default).

## Known Issues ⚠️
- **Data Collection Failures:** Data collection may fail if the CoinMarketCap API is down or if there are connectivity issues.
- **Permission Problems:** If the program is run in a protected directory, there may be issues with creating files due to lack of proper permissions. To resolve, run the program as an administrator.
- **Email Authentication Error:** If the email credentials are incorrect or if there are authentication problems with the email server, sending notifications may fail.


## Code Overview

### Colors

The application uses ANSI escape codes to print colored text in the terminal.

```python
# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'
```

## Licença 📝

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
