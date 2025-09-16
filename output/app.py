import gradio as gr
from accounts import Account

account = Account("User")

def create_account(username: str):
    account.create_account(username)
    return "Account created successfully!"

def deposit(amount: float):
    try:
        account.deposit(amount)
        return f"Deposited ${amount:.2f}"
    except ValueError as e:
        return str(e)

def withdraw(amount: float):
    try:
        account.withdraw(amount)
        return f"Withdrew ${amount:.2f}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol: str, quantity: int):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol: str, quantity: int):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}"
    except ValueError as e:
        return str(e)

def get_balance():
    return f"Balance: ${account.balance:.2f}"

def get_holdings():
    holdings = account.get_holdings()
    return f"Holdings: {holdings}" if holdings else "No holdings."

def get_profit_loss():
    profit_loss = account.get_profit_loss()
    return f"Profit/Loss: ${profit_loss:.2f}"

def get_transactions():
    transactions = account.get_transaction_history()
    return transactions if transactions else "No transactions."

with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Row():
            username_input = gr.Textbox(label="Username")
            create_button = gr.Button("Create Account")
            create_output = gr.Textbox(label="Account Creation", interactive=False)
        
        with gr.Row():
            deposit_input = gr.Number(label="Deposit Amount")
            deposit_button = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Deposit Status", interactive=False)
        
        with gr.Row():
            withdraw_input = gr.Number(label="Withdrawal Amount")
            withdraw_button = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Withdrawal Status", interactive=False)

        create_button.click(create_account, inputs=username_input, outputs=create_output)
        deposit_button.click(deposit, inputs=deposit_input, outputs=deposit_output)
        withdraw_button.click(withdraw, inputs=withdraw_input, outputs=withdraw_output)

    with gr.Tab("Trading"):
        with gr.Row():
            buy_symbol_input = gr.Textbox(label="Buy Symbol", placeholder="e.g., GOOGL, TSLA, AAPL")
            buy_quantity_input = gr.Number(label="Buy Quantity")
            buy_button = gr.Button("Buy")
            buy_output = gr.Textbox(label="Buy Status", interactive=False)

        with gr.Row():
            sell_symbol_input = gr.Textbox(label="Sell Symbol", placeholder="e.g., GOOGL, TSLA, AAPL")
            sell_quantity_input = gr.Number(label="Sell Quantity")
            sell_button = gr.Button("Sell")
            sell_output = gr.Textbox(label="Sell Status", interactive=False)

        buy_button.click(buy_shares, inputs=[buy_symbol_input, buy_quantity_input], outputs=buy_output)
        sell_button.click(sell_shares, inputs=[sell_symbol_input, sell_quantity_input], outputs=sell_output)

    with gr.Tab("Reports"):
        with gr.Row():
            balance_button = gr.Button("Check Balance")
            balance_output = gr.Textbox(label="Balance", interactive=False)

        with gr.Row():
            holdings_button = gr.Button("Check Holdings")
            holdings_output = gr.Textbox(label="Holdings", interactive=False)

        with gr.Row():
            profit_loss_button = gr.Button("Check Profit/Loss")
            profit_loss_output = gr.Textbox(label="Profit/Loss", interactive=False)

        with gr.Row():
            transactions_button = gr.Button("View Transactions")
            transactions_output = gr.Textbox(label="Transaction History", interactive=False)

        balance_button.click(get_balance, outputs=balance_output)
        holdings_button.click(get_holdings, outputs=holdings_output)
        profit_loss_button.click(get_profit_loss, outputs=profit_loss_output)
        transactions_button.click(get_transactions, outputs=transactions_output)

demo.launch()