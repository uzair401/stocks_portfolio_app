# Stocks Portfolio Management Web Application
[Demo Link : https://stocks-portfolio-app.onrender.com/](https://stocks-portfolio-app.onrender.com/)


## Description

Stocks Portfolio Management Web Application is a web application designed to help users manage their personal financial portfolio. Users can buy and sell stocks, view their financial history, check stock prices, and track their total net worth. The application uses a combination of Flask for the backend, Jinja for templating, and SQLite for data storage, making it lightweight and easy to deploy.

## Features

- **User Registration/Login**: Secure user authentication for tracking personalized portfolios.
- **Quote Stocks**: Users can search for real-time stock quotes using an external API.
- **Buy and Sell Stocks**: Users can buy shares of stock at current market prices and sell them when needed.
- **Transaction History**: A complete history of all transactions (buys and sells) is maintained for each user.
- **Portfolio Overview**: A dashboard where users can view the current state of their portfolio, including the stocks they own and their respective values.
- **Check Account Balance**: Users can keep track of their cash balance after transactions.

## Prerequisites

To run this project locally, you will need:
- Python 3.8+
- Flask 2.0+
- SQLite3
- IEX Exchange API for fetching stock quotes

## Images

### Dashboard
![My Image](https://github.com/uzair401/stocks_portfolio_app/blob/master/templates/Dashboard.png)

### Qouting Stock price 
![My Image](https://github.com/uzair401/stocks_portfolio_app/blob/master/templates/Qoute.png)
### Stock selling 
![My Image](https://github.com/uzair401/stocks_portfolio_app/blob/master/templates/Sell.png)
### Transaction History
![My Image](https://github.com/uzair401/stocks_portfolio_app/blob/master/templates/Transaction%20History.png)






## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/uzair401/flask.git
cd flask/finance
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key

1. Register for an API key with a stock quote provider (such as [Alpha Vantage](https://www.alphavantage.co/) or [IEX Cloud](https://iexcloud.io/)).
2. Store the API key in your environment variables or in the `.env` file.

### Step 5: Set up the Database

```bash
flask shell
from app import db
db.create_all()
```

### Step 6: Run the Application

```bash
flask run
```

The app will run locally at `http://127.0.0.1:5000/`. Open your browser and start managing your finances!

## Usage

1. **Register/Login**: Start by creating an account and logging in to the system.
2. **View Stock Quotes**: Use the stock quote feature to search for stocks and get real-time price updates.
3. **Buy Stocks**: Select a stock and input the number of shares to buy. The cost will be deducted from your cash balance.
4. **Sell Stocks**: Choose stocks you own, and input the number of shares to sell. The proceeds will be added to your cash balance.
5. **Portfolio Management**: View your portfolio and track the performance of your investments.
6. **Transaction History**: A log of all your buys and sells is available for review.

## Folder Structure

```
flask/
│
├── finance/              # Main application directory
│   ├── app/              # Flask application files
│   ├── templates/        # HTML templates for rendering views
│   ├── static/           # Static files (CSS, JS)
│   ├── __init__.py       # App initialization
│   └── database.db         # Database  for user and transactions
│
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

