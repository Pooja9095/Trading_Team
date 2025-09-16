from trading.py import TradingAccount
import pytest

def test_list_assets():
    """Test that list_assets returns all available symbols"""
    account = TradingAccount(cash=10000.0)
    assets = account.list_assets()
    
    # Should return sorted list of all available symbols
    expected = ["AAPL", "AMZN", "GOOGL", "META", "MSFT", "NFLX", "NVDA", "TSLA"]
    assert assets == expected

def test_quote():
    """Test that quote returns correct prices for known symbols"""
    account = TradingAccount(cash=10000.0)
    
    # Test known symbols
    assert account.quote("AAPL") == 150.0
    assert account.quote("TSLA") == 700.0
    assert account.quote("GOOGL") == 2500.0
    assert account.quote("MSFT") == 300.0
    
    # Test case insensitivity
    assert account.quote("aapl") == 150.0
    assert account.quote("tsLa") == 700.0

def test_quote_unknown_symbol():
    """Test that quote raises UnknownSymbolError for unknown symbols"""
    account = TradingAccount(cash=10000.0)
    
    with pytest.raises(UnknownSymbolError, match="Symbol 'INVALID' is not available for trading"):
        account.quote("INVALID")

def test_deposit():
    """Test deposit functionality"""
    account = TradingAccount(cash=1000.0)
    
    # Test successful deposit
    account.deposit(500.0)
    assert account.cash == 1500.0
    
    # Check history
    history = account.history()
    assert len(history) == 1
    assert history[0]["type"] == "deposit"
    assert history[0]["total_amount"] == 500.0

def test_deposit_invalid_amount():
    """Test that deposit raises InvalidQuantityError for non-positive amounts"""
    account = TradingAccount(cash=1000.0)
    
    with pytest.raises(InvalidQuantityError, match="Deposit amount must be positive"):
        account.deposit(0.0)
    
    with pytest.raises(InvalidQuantityError, match="Deposit amount must be positive"):
        account.deposit(-100.0)

def test_withdraw():
    """Test withdraw functionality"""
    account = TradingAccount(cash=1000.0)
    
    # Test successful withdrawal
    account.withdraw(300.0)
    assert account.cash == 700.0
    
    # Check history
    history = account.history()
    assert len(history) == 1
    assert history[0]["type"] == "withdrawal"
    assert history[0]["total_amount"] == -300.0

def test_withdraw_invalid_amount():
    """Test that withdraw raises InvalidQuantityError for non-positive amounts"""
    account = TradingAccount(cash=1000.0)
    
    with pytest.raises(InvalidQuantityError, match="Withdrawal amount must be positive"):
        account.withdraw(0.0)
    
    with pytest.raises(InvalidQuantityError, match="Withdrawal amount must be positive"):
        account.withdraw(-100.0)

def test_withdraw_insufficient_funds():
    """Test that withdraw raises InsufficientFundsError when amount exceeds available cash"""
    account = TradingAccount(cash=1000.0)
    
    with pytest.raises(InsufficientFundsError, match=r"Insufficient funds: \$1000\.00 available, need \$1500\.00"):
        account.withdraw(1500.0)

def test_buy():
    """Test buy functionality"""
    account = TradingAccount(cash=10000.0)
    
    # Test successful buy
    cost = account.buy("AAPL", 10)
    assert cost == 1500.0  # 10 shares * $150
    assert account.cash == 8500.0
    
    # Check position
    positions = account.positions()
    assert len(positions) == 1
    assert positions[0]["symbol"] == "AAPL"
    assert positions[0]["shares"] == 10
    assert positions[0]["avg_cost"] == 150.0
    
    # Check history
    history = account.history()
    assert len(history) == 1
    assert history[0]["type"] == "buy"
    assert history[0]["symbol"] == "AAPL"
    assert history[0]["quantity"] == 10
    assert history[0]["price"] == 150.0
    assert history[0]["total_amount"] == -1500.0

def test_buy_invalid_quantity():
    """Test that buy raises InvalidQuantityError for non-positive quantities"""
    account = TradingAccount(cash=10000.0)
    
    with pytest.raises(InvalidQuantityError, match="Buy quantity must be positive"):
        account.buy("AAPL", 0)
    
    with pytest.raises(InvalidQuantityError, match="Buy quantity must be positive"):
        account.buy("AAPL", -10)

def test_buy_unknown_symbol():
    """Test that buy raises UnknownSymbolError for unknown symbols"""
    account = TradingAccount(cash=10000.0)
    
    with pytest.raises(UnknownSymbolError, match="Symbol 'INVALID' is not available for trading"):
        account.buy("INVALID", 10)

def test_buy_insufficient_funds():
    """Test that buy raises InsufficientFundsError when cost exceeds available cash"""
    account = TradingAccount(cash=1000.0)
    
    with pytest.raises(InsufficientFundsError, match=r"Insufficient funds: \$1500\.00 available, need \$1500\.00"):
        account.buy("AAPL", 10)  # 10 shares * $150 = $1500

def test_buy_average_cost_calculation():
    """Test that buy correctly calculates average cost when adding to existing position"""
    account = TradingAccount(cash=10000.0)
    
    # First purchase
    account.buy("AAPL", 10)
    assert account.positions()[0]["avg_cost"] == 150.0
    
    # Second purchase at different price
    account.buy("AAPL", 5)  # 5 more shares
    assert account.positions()[0]["shares"] == 15
    
    # Calculate expected average cost: (10*150 + 5*150) / 15 = 150
    expected_avg_cost = (10 * 150.0 + 5 * 150.0) / 15
    assert account.positions()[0]["avg_cost"] == expected_avg_cost
    
    # Test with different price
    account2 = TradingAccount(cash=10000.0)
    account2.buy("AAPL", 10)  # 10 shares at $150
    account2.buy("AAPL", 10)  # 10 more shares at $160
    
    # Calculate expected average cost: (10*150 + 10*160) / 20 = 155
    expected_avg_cost = (10 * 150.0 + 10 * 160.0) / 20
    assert account2.positions()[0]["avg_cost"] == expected_avg_cost

def test_sell():
    """Test sell functionality"""
    account = TradingAccount(cash=10000.0)
    
    # First buy some shares
    account.buy("AAPL", 10)
    assert account.cash == 8500.0
    
    # Then sell some shares
    revenue = account.sell("AAPL", 5)
    assert revenue == 750.0  # 5 shares * $150
    assert account.cash == 9250.0
    
    # Check position
    positions = account.positions()
    assert len(positions) == 1
    assert positions[0]["symbol"] == "AAPL"
    assert positions[0]["shares"] == 5
    assert positions[0]["avg_cost"] == 150.0  # Average cost doesn't change
    
    # Check history
    history = account.history()
    assert len(history) == 2
    assert history[1]["type"] == "sell"
    assert history[1]["symbol"] == "AAPL"
    assert history[1]["quantity"] == 5
    assert history[1]["price"] == 150.0
    assert history[1]["total_amount"] == 750.0

def test_sell_all_shares():
    """Test selling all shares removes the position"""
    account = TradingAccount(cash=10000.0)
    
    # Buy some shares
    account.buy("AAPL", 10)
    assert len(account.positions()) == 1
    
    # Sell all shares
    account.sell("AAPL", 10)
    assert len(account.positions()) == 0

def test_sell_invalid_quantity():
    """Test that sell raises InvalidQuantityError for non-positive quantities"""
    account = TradingAccount(cash=10000.0)
    account.buy("AAPL", 10)
    
    with pytest.raises(InvalidQuantityError, match="Sell quantity must be positive"):
        account.sell("AAPL", 0)
    
    with pytest.raises(InvalidQuantityError, match="Sell quantity must be positive"):
        account.sell("AAPL", -5)

def test_sell_unknown_symbol():
    """Test that sell raises UnknownSymbolError for symbols not in portfolio"""
    account = TradingAccount(cash=10000.0)
    
    with pytest.raises(UnknownSymbolError, match="No position found for symbol 'TSLA'"):
        account.sell("TSLA", 10)

def test_sell_insufficient_shares():
    """Test that sell raises InsufficientSharesError when quantity exceeds owned shares"""
    account = TradingAccount(cash=10000.0)
    account.buy("AAPL", 10)
    
    with pytest.raises(InsufficientSharesError, match="Insufficient shares: 10 available, need 15"):
        account.sell("AAPL", 15)

def test_positions():
    """Test positions method returns correct position data"""
    account = TradingAccount(cash=10000.0)
    
    # Initially no positions
    assert account.positions() == []
    
    # Buy some shares
    account.buy("AAPL", 10)
    account.buy("GOOGL", 5)
    
    # Check positions
    positions = account.positions()
    assert len(positions) == 2
    
    # Check AAPL position
    aapl_pos = next(p for p in positions if p["symbol"] == "AAPL")
    assert aapl_pos["shares"] == 10
    assert aapl_pos["avg_cost"] == 150.0
    
    # Check GOOGL position
    googl_pos = next(p for p in positions if p["symbol"] == "GOOGL")
    assert googl_pos["shares"] == 5
    assert googl_pos["avg_cost"] == 2500.0

def test_portfolio_totals():
    """Test portfolio_totals method returns correct calculations"""
    account = TradingAccount(cash=10000.0)
    
    # Initially only cash
    totals = account.portfolio_totals()
    assert totals["cash"] == 10000.0
    assert totals["positions_value"] == 0.0
    assert totals["total"] == 10000.0
    
    # Buy some shares
    account.buy("AAPL", 10)
    account.buy("GOOGL", 5)
    
    # Check totals
    totals = account.portfolio_totals()
    expected_cash = 10000.0 - (10 * 150.0) - (5 * 2500.0)
    expected_positions_value = (10 * 150.0) + (5 * 2500.0)
    expected_total = expected_cash + expected_positions_value
    
    assert totals["cash"] == expected_cash
    assert totals["positions_value"] == expected_positions_value
    assert totals["total"] == expected_total

def test_portfolio_totals_after_sell():
    """Test portfolio_totals after selling some shares"""
    account = TradingAccount(cash=10000.0)
    account.buy("AAPL", 10)
    account.buy("GOOGL", 5)
    
    # Sell half of AAPL shares
    account.sell("AAPL", 5)
    
    # Check totals
    totals = account.portfolio_totals()
    expected_cash = 10000.0 - (10 * 150.0) - (5 * 2500.0) + (5 * 150.0)
    expected_positions_value = (5 * 150.0) + (5 * 2500.0)
    expected_total = expected_cash + expected_positions_value
    
    assert totals["cash"] == pytest.approx(expected_cash)
    assert totals["positions_value"] == pytest.approx(expected_positions_value)
    assert totals["total"] == pytest.approx(expected_total)

def test_history_structure():
    """Test that history returns properly structured trades"""
    account = TradingAccount(cash=10000.0)
    
    # Initially empty history
    history = account.history()
    assert history == []
    
    # Perform some trades
    account.deposit(1000.0)
    account.buy("AAPL", 10)
    account.sell("AAPL", 5)
    account.withdraw(500.0)
    
    # Check history structure
    history = account.history()
    assert len(history) == 4
    
    # Check each trade has all required fields
    for trade in history:
        assert "type" in trade
        assert "symbol" in trade
        assert "quantity" in trade
        assert "price" in trade
        assert "total_amount" in trade
        assert "timestamp" in trade
        assert trade["timestamp"] == "2023-01-01T00:00:00"

def test_history_ordering():
    """Test that history maintains chronological order"""
    account = TradingAccount(cash=10000.0)
    
    # Perform trades in a specific order
    account.deposit(1000.0)
    account.buy("AAPL", 10)
    account.sell("AAPL", 5)
    account.withdraw(500.0)
    account.buy("GOOGL", 2)
    
    # Check that history is in correct order
    history = account.history()
    assert history[0]["type"] == "deposit"
    assert history[1]["type"] == "buy"
    assert history[1]["symbol"] == "AAPL"
    assert history[2]["type"] == "sell"
    assert history[2]["symbol"] == "AAPL"
    assert history[3]["type"] == "withdrawal"
    assert history[4]["type"] == "buy"
    assert history[4]["symbol"] == "GOOGL"

def test_history_recorded_amounts():
    """Test that history records correct amounts"""
    account = TradingAccount(cash=10000.0)
    
    # Deposit
    account.deposit(1000.0)
    assert account.history()[0]["total_amount"] == 1000.0
    
    # Buy
    account.buy("AAPL", 10)
    assert account.history()[1]["total_amount"] == -1500.0  # Cash spent
    
    # Sell
    account.sell("AAPL", 5)
    assert account.history()[2]["total_amount"] == 750.0  # Cash received
    
    # Withdraw
    account.withdraw(500.0)
    assert account.history()[3]["total_amount"] == -500.0  # Cash withdrawn