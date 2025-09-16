class Account:
    def __init__(self, username: str):
        self.username = username
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []

    def create_account(self, username: str) -> None:
        self.username = username
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be greater than zero.')
        self.balance += amount
        self.transactions.append({'type': 'Deposit', 'amount': amount})

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Withdrawal amount must be greater than zero.')
        if self.balance - amount < 0:
            raise ValueError('Insufficient funds to withdraw the specified amount.')
        self.balance -= amount
        self.transactions.append({'type': 'Withdrawal', 'amount': amount})

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be greater than zero.')
        cost = get_share_price(symbol) * quantity
        if cost > self.balance:
            raise ValueError('Insufficient funds to buy shares.')
        self.balance -= cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append({'type': 'Buy', 'symbol': symbol, 'quantity': quantity})

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be greater than zero.')
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError('Not enough shares to sell.')
        proceeds = get_share_price(symbol) * quantity
        self.balance += proceeds
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({'type': 'Sell', 'symbol': symbol, 'quantity': quantity})

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        initial_investment = sum(t['amount'] for t in self.transactions if t['type'] == 'Deposit')
        current_value = self.get_portfolio_value()
        return current_value - initial_investment

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transaction_history(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)