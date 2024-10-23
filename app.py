import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    id = session.get("user_id")
    rows = db.execute("SELECT * FROM portfolio WHERE id = ?",id )
    results = []
    total_sum = 0.0

    for row in rows:
        symbol = row["symbol"]
        result = lookup(symbol)
        results.append(result)
        total_sum += row["total"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", id)
    if cash:
        total_sum = cash[0]['cash'] - total_sum
    data = db.execute("SELECT * FROM portfolio WHERE id = ?",id)
    return render_template("home.html", data=data  , cash = cash, results = results, total_sum = total_sum)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":
        user_id = session.get("user_id")
        symbol = request.form.get("symbol")
        data = lookup(symbol)
        if data is None:
            return apology("Inavlid Symbol", 400)
        symbol = data['symbol']
        shares = request.form.get("shares")  # Convert shares to an integer
        if not shares.isnumeric():
            return apology ("Invalid Shares input")
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        # Call lookup function to get stock data

        if data is None:
            return apology("Incorrect Symbol")

        # Get the current portfolio information for the symbol
        portfolio_info = db.execute("SELECT * FROM portfolio WHERE id = ? AND symbol = ?", user_id, symbol)

        if not portfolio_info:
            # Symbol not in the portfolio, so insert a new record
            price = data['price']
            total = int(shares) * price
            if total > cash[0]['cash']:
                return apology("Cannot Afford the stock, out of cash ")
            else:
                db.execute("INSERT INTO portfolio (id, symbol, shares, price, total) VALUES (?, ?, ?, ?, ?)",
                       user_id, symbol, shares, price, total)
                db.execute("INSERT INTO history (user_id, symbol, shares,price) VALUES (?,?,?,?)",user_id, symbol, shares, price)
        else:
            # Symbol already in the portfolio, so update the shares and total
            current_shares = portfolio_info[0]['shares']
            current_price_per_share = portfolio_info[0]['price']
            current_total = current_shares * current_price_per_share

            price = data['price']
            additional_total = int(shares) * price
            new_total = current_total + additional_total
            if additional_total > cash[0]['cash']:
                return apology("Cannot Afford the stock, out of cash ")
            else:
                db.execute("UPDATE portfolio SET shares = shares + ?, total = ? WHERE id = ? AND symbol = ?",
                       shares, new_total, user_id, symbol)
                db.execute("INSERT INTO history (user_id, symbol, shares,price) VALUES (?,?,?,?)",user_id, symbol, shares, price)

    return redirect("/")



@app.route("/history")
@login_required
def history():
    id = session.get("user_id")
    logs = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC", id)
    return render_template("history.html", logs=logs)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    symbol = request.form.get("symbol")
    if request.method == "GET":
        return render_template("qoute.html")
    elif request.method == "POST":
        result = lookup(symbol)
        if result:
            return render_template('qouted.html', quote_result=result)
        else:
            return apology("Symbol not found")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password was submitted and matches confirmation
        elif password != confirmation:
            return apology("passwords do not match", 400)

        try:
            # Attempt to insert the user data into the database
            # If the username is not unique, this will raise a UNIQUE constraint error
            hashed_password = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hashed_password)

            # Redirect to the login page after successful registration
            return redirect("/login")

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                flash("Username already exists. Please choose a different username.")
                return apology("username already exist", 400)
            else:
                flash("An error occurred during registration. Please try again.")
            return redirect("/register")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    id = session.get("user_id")
    if request.method == "GET":
        list = db.execute("SELECT * FROM portfolio WHERE id = ?", id)
        list_item = []
        for item in list:
            symbol = item["symbol"]
            list_item.append(symbol)
        return render_template("sell.html", list_item=list_item)

    elif request.method == "POST":
        id = session.get("user_id")
        selected_item = request.form.get('symbol')
        symbol = selected_item
        if not selected_item:
            return apology("Select a Stock")
        shares = request.form.get('shares')
        if not str(shares).isnumeric():
            return apology("Invalid shares Input",400)
        shares = int(shares)
        if not shares:
            return apology("Enter amount of shares")
        elif shares < 0:
            return apology("Enter Positive Number ")
        data = lookup(selected_item)
        if data is None:
            return apology ("Data didn't returned by the lookup")
        elif data:
            price = data['price']
            d_shares = db.execute("SELECT shares FROM portfolio WHERE symbol = ? AND id = ?", symbol,id)
            for item in d_shares:
                d_shares = int(item['shares'])

            if shares > d_shares:
                return apology("You are Exceeding your shares Limit", 400)
            db.execute("UPDATE portfolio SET shares = shares - ?, total = total- (? * ?)  WHERE symbol = ? AND id = ? ",shares,shares,price,selected_item,id)
            negative_shares = -shares
            db.execute("INSERT INTO history (user_id, symbol, shares,price) VALUES (?,?,?,?)",id, symbol, negative_shares, price)
            return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")

    if request.method == "POST":
        id = session.get("user_id")
        current_password = request.form.get("current_password")
        new = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not current_password:
            return apology("Must provide current password", 400)
        elif not new:
            return apology("Must provide new password", 400)
        elif new != confirmation:
            return apology("Passwords do not match", 400)
        elif new == current_password:
            return apology("New password must be different from current password", 400)

        stored_hashed_password = db.execute("SELECT hash FROM users WHERE id = ?", id)
        if not stored_hashed_password:
            return apology("Password in database not found", 400)

        stored_hashed_password = stored_hashed_password[0]["hash"]
        if not check_password_hash(stored_hashed_password, current_password):
            return apology("Current password is incorrect", 400)

        new_password = generate_password_hash(new)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password, id)
        return redirect("/")
