import unittest

class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        self.user_id = user_id
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be positive')
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})

    def buy_shares(self, symbol: str, quantity: int) -> None:
        price = get_share_price(symbol)
        cost = price * quantity
        if cost > self.balance:
            raise ValueError('Insufficient funds for purchase')
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.balance -= cost
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity, 'price': price})

def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 600.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)

class TestAccount(unittest.TestCase):

    def test_create_account(self):
        account = Account('user1', 1000.0)
        self.assertEqual(account.user_id, 'user1')
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.holdings, {})

    def test_deposit(self):
        account = Account('user1', 1000.0)
        account.deposit(500.0)
        self.assertEqual(account.balance, 1500.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0], {'type': 'deposit', 'amount': 500.0})

    def test_buy_shares(self):
        account = Account('user1', 1000.0)
        account.buy_shares('AAPL', 2)
        self.assertEqual(account.balance, 700.0)
        self.assertEqual(account.holdings['AAPL'], 2)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0], {'type': 'buy', 'symbol': 'AAPL', 'quantity': 2, 'price': 150.0})

if __name__ == '__main__':
    unittest.main()