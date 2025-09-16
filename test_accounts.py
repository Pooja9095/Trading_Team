import unittest

class Account:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount: float) -> None:
        if self.balance - amount < 0:
            raise Exception('Insufficient funds')
        self.balance -= amount
        self.transactions.append({'type': 'withdraw', 'amount': amount})

    def buy_share(self, symbol: str, quantity: int) -> None:
        total_cost = get_share_price(symbol) * quantity
        if self.balance < total_cost:
            raise Exception('Insufficient funds to buy shares')
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.balance -= total_cost
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity})

    def sell_share(self, symbol: str, quantity: int) -> None:
        if self.holdings.get(symbol, 0) < quantity:
            raise Exception('Not enough shares to sell')
        total_earnings = get_share_price(symbol) * quantity
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.balance += total_earnings
        self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity})

    def calculate_portfolio_value(self) -> float:
        total_value = 0.0
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        total_deposited = sum(tx['amount'] for tx in self.transactions if tx['type'] == 'deposit')
        return (self.balance + self.calculate_portfolio_value()) - total_deposited

    def get_holdings(self) -> dict:
        return self.holdings.copy()

    def get_transactions(self) -> list:
        return self.transactions.copy()

    def get_current_balance(self) -> float:
        return self.balance


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('user123')

    def test_initial_balance(self):
        self.assertEqual(self.account.get_current_balance(), 0.0)

    def test_deposit(self):
        self.account.deposit(100.0)
        self.assertEqual(self.account.get_current_balance(), 100.0)

    def test_withdraw(self):
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        self.assertEqual(self.account.get_current_balance(), 50.0)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(Exception):
            self.account.withdraw(50.0)

    def test_buy_share(self):
        self.account.deposit(1000.0)
        self.account.buy_share('AAPL', 2)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
        self.assertEqual(self.account.get_current_balance(), 700.0)

    def test_buy_share_insufficient_funds(self):
        self.account.deposit(100.0)
        with self.assertRaises(Exception):
            self.account.buy_share('AAPL', 1)

    def test_sell_share(self):
        self.account.deposit(1000.0)
        self.account.buy_share('AAPL', 2)
        self.account.sell_share('AAPL', 1)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 1})
        self.assertEqual(self.account.get_current_balance(), 850.0)

    def test_sell_share_not_enough(self):
        self.account.deposit(1000.0)
        self.account.buy_share('AAPL', 1)
        with self.assertRaises(Exception):
            self.account.sell_share('AAPL', 2)

    def test_calculate_portfolio_value(self):
        self.account.deposit(1000.0)
        self.account.buy_share('AAPL', 2)
        self.assertEqual(self.account.calculate_portfolio_value(), 300.0)

    def test_calculate_profit_loss(self):
        self.account.deposit(1000.0)
        self.account.buy_share('AAPL', 2)
        self.assertEqual(self.account.calculate_profit_loss(), 300.0)
        self.account.withdraw(100.0)
        self.assertEqual(self.account.calculate_profit_loss(), 200.0)

if __name__ == '__main__':
    unittest.main()