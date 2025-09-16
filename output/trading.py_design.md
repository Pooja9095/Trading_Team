```python
# trading.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Error definitions
class TradingError(Exception):
    """Base class for trading errors"""
    pass

class UnknownSymbolError(TradingError):
    """Raised when an unknown symbol is used"""
    def __init__(self, symbol: str):
        self.symbol = symbol
        super().__init__(f"Symbol '{symbol}' is not available for trading")

class InvalidQuantityError(TradingError):
    """Raised when an invalid quantity is provided"""
    def __init__(self, quantity: float, message: Optional[str] = None):
        self.quantity = quantity
        msg = message or f"Quantity must be positive, got {quantity}"
        super().__init__(msg)

class InsufficientFundsError(TradingError):
    """Raised when trying to spend more cash than available"""
    def __init__(self, required: float, available: float):
        self.required = required
        self.available = available
        super().__init__(f"Insufficient funds: ${available:.2f} available, need ${required:.2f}")

class InsufficientSharesError(TradingError):
    """Raised when trying to sell more shares than owned"""
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        super().__init__(f"Insufficient shares: {available} available, need {required}")

# PriceFeed implementation
@dataclass
class PriceFeed:
    """Provides fixed prices for trading symbols"""
    fixed_prices: Dict[str, float]
    
    def __init__(self):
        # Initialize with some common stock symbols and fixed prices
        self.fixed_prices = {
            "AAPL": 150.0,
            "TSLA": 700.0,
            "GOOGL": 2500.0,
            "MSFT": 300.0,
            "AMZN": 3200.0,
            "META": 300.0,
            "NFLX": 400.0,
            "NVDA": 500.0,
        }
    
    def get_price(self, symbol: str) -> float:
        """
        Get the current price for a trading symbol
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            
        Returns:
            Current price as a float
            
        Raises:
            UnknownSymbolError: If symbol is not available
        """
        symbol = symbol.upper()
        if symbol not in self.fixed_prices:
            raise UnknownSymbolError(symbol)
        return self.fixed_prices[symbol]

# Position data class
@dataclass
class Position:
    """Represents a position in a stock"""
    symbol: str
    shares: int
    avg_cost: float

# TradingAccount implementation
@dataclass
class TradingAccount:
    """Main trading account with positions, cash, and trading history"""
    cash: float
    price_feed: PriceFeed
    positions: Dict[str, Position] = field(default_factory=dict)
    trades: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        if not isinstance(self.price_feed, PriceFeed):
            self.price_feed = PriceFeed()
    
    # Public API methods
    
    def list_assets(self) -> List[str]:
        """
        List all available trading assets
        
        Returns:
            List of available symbols
        """
        return sorted(self.price_feed.fixed_prices.keys())
    
    def quote(self, symbol: str) -> float:
        """
        Get current price for a symbol
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            
        Returns:
            Current price as a float
            
        Raises:
            UnknownSymbolError: If symbol is not available
        """
        return self.price_feed.get_price(symbol)
    
    def deposit(self, amount: float) -> None:
        """
        Add cash to the account
        
        Args:
            amount: Amount to deposit (must be positive)
            
        Raises:
            InvalidQuantityError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidQuantityError(amount, "Deposit amount must be positive")
        self.cash += amount
        
        # Record trade history
        self._record_trade("deposit", None, None, None, amount)
    
    def withdraw(self, amount: float) -> None:
        """
        Remove cash from the account
        
        Args:
            amount: Amount to withdraw (must be positive)
            
        Raises:
            InvalidQuantityError: If amount is not positive
            InsufficientFundsError: If amount exceeds available cash
        """
        if amount <= 0:
            raise InvalidQuantityError(amount, "Withdrawal amount must be positive")
        if amount > self.cash:
            raise InsufficientFundsError(amount, self.cash)
            
        self.cash -= amount
        
        # Record trade history
        self._record_trade("withdrawal", None, None, None, -amount)
    
    def buy(self, symbol: str, quantity: int) -> float:
        """
        Buy shares of a stock
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            quantity: Number of shares to buy (must be positive)
            
        Returns:
            Total cost of the purchase
            
        Raises:
            UnknownSymbolError: If symbol is not available
            InvalidQuantityError: If quantity is not positive
            InsufficientFundsError: If cost exceeds available cash
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity, "Buy quantity must be positive")
            
        price = self.quote(symbol)
        total_cost = price * quantity
        
        if total_cost > self.cash:
            raise InsufficientFundsError(total_cost, self.cash)
            
        # Update cash
        self.cash -= total_cost
        
        # Update position
        if symbol in self.positions:
            # Update existing position
            position = self.positions[symbol]
            total_shares = position.shares + quantity
            total_cost = (position.shares * position.avg_cost) + (quantity * price)
            position.shares = total_shares
            position.avg_cost = total_cost / total_shares
        else:
            # Create new position
            self.positions[symbol] = Position(symbol, quantity, price)
            
        # Record trade history
        self._record_trade("buy", symbol, quantity, price, total_cost)
        
        return total_cost
    
    def sell(self, symbol: str, quantity: int) -> float:
        """
        Sell shares of a stock
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            quantity: Number of shares to sell (must be positive)
            
        Returns:
            Total revenue from the sale
            
        Raises:
            UnknownSymbolError: If symbol is not available
            InvalidQuantityError: If quantity is not positive
            InsufficientSharesError: If quantity exceeds owned shares
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity, "Sell quantity must be positive")
            
        if symbol not in self.positions:
            raise UnknownSymbolError(f"No position found for symbol '{symbol}'")
            
        position = self.positions[symbol]
        if quantity > position.shares:
            raise InsufficientSharesError(quantity, position.shares)
            
        price = self.quote(symbol)
        total_revenue = price * quantity
        
        # Update cash
        self.cash += total_revenue
        
        # Update position
        position.shares -= quantity
        if position.shares == 0:
            # Remove position if no shares left
            del self.positions[symbol]
            
        # Record trade history
        self._record_trade("sell", symbol, quantity, price, total_revenue)
        
        return total_revenue
    
    def positions(self) -> Dict[str, Dict]:
        """
        Get all current positions
        
        Returns:
            Dictionary of positions keyed by symbol
            Each position contains 'shares' and 'avg_cost'
        """
        return {
            symbol: {
                "shares": position.shares,
                "avg_cost": position.avg_cost
            }
            for symbol, position in self.positions.items()
        }
    
    def portfolio_totals(self) -> Dict[str, float]:
        """
        Calculate portfolio totals
        
        Returns:
            Dictionary with:
            - 'cash': current cash balance
            - 'positions_value': total value of all positions
            - 'total': sum of cash and positions value
        """
        positions_value = sum(
            position.shares * self.quote(position.symbol)
            for position in self.positions.values()
        )
        
        return {
            "cash": self.cash,
            "positions_value": positions_value,
            "total": self.cash + positions_value
        }
    
    def history(self) -> List[Dict]:
        """
        Get trading history
        
        Returns:
            List of trade dictionaries
            Each trade contains type, symbol, quantity, price, total_amount, and timestamp
        """
        return self.trades
    
    # Helper methods
    
    def _record_trade(self, trade_type: str, symbol: Optional[str], 
                     quantity: Optional[int], price: Optional[float], 
                     total_amount: float) -> None:
        """Record a trade in the history"""
        trade = {
            "type": trade_type,
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "total_amount": total_amount,
            "timestamp": "2023-01-01T00:00:00"  # Deterministic placeholder for no I/O requirement
        }
        self.trades.append(trade)

# UI Contract
# 
# For frontend integration:
# 1. Assets with buy/sell:
#    - Use list_assets() to get all available symbols
#    - Use quote(symbol) to get current price
#    - Use buy(symbol, quantity) and sell(symbol, quantity) for trading
#
# 2. Positions display:
#    - Use positions() to get current positions
#    - Use quote(symbol) to get current prices for valuation
#
# 3. History display:
#    - Use history() to get all trades with timestamps
#
# 4. Portfolio summary:
#    - Use portfolio_totals() to get cash, positions value, and total
#
# Values-only: All methods return primitive data types or dictionaries with primitive values,
#              avoiding complex UI objects to allow integration with any frontend framework.
#
# No deprecated Gradio: This module provides raw data values that can be formatted
#                       by any frontend framework including modern versions of Gradio or alternatives.
```