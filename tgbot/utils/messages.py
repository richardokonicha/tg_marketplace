messages = {
    "select_preferred_lang": """
Please select your language
Per favore scelga la sua lingua
    """,

    "set_lang_text": {
          
        "en": """Language is set to: English 🇬🇧""",
        "it": """La lingua è impostata su: Italian 🇮🇹"""

    },

    "welcome_text": {

        "en": """
<b>Welcome to Queen Weed Bot</b>

        """,

        "it": """
<b>Benvenuti a Queen Weed Bot </b>

        """
    },

    "balance_msg": {

        "en": """
Your Account Balance:
<strong>{balance} BTC</strong>
Total Active Investments:
<strong>{active_investment} BTC</strong>
Total Active Reinvestments:
<strong>{active_reinvestment} BTC</strong>
Total Pending Investments:
<strong>{pending_investment} BTC</strong>
                """,

        "it": """

Saldo del conto:
<strong>{balance} BTC</strong>
Investimenti attivi:
<strong>{active_investment} BTC</strong>
Reinvestimenti attivi:
<strong>{active_reinvestment} BTC</strong>
Investimenti in sospeso:
<strong>{pending_investment} BTC</strong>

    """,
    },

    "no_balance_text": {
        "en": f"""
            No investment yet. Go to <b>Deposit</b> to add funds.
        """,
        "it": f"""
            Ancora nessun investimento
Andate a <b>Deposito</b> per aggiungere fondi.
        """
    },

    "markup_balances": {
        "en": "🏦 Balance  {account_balance} BTC",
        "it": "🏦 Bilance  {account_balance} BTC"
    },


    "text_insufficient": {
        "en": "You have insufficient account balance",
        "it": "Hai un saldo del conto insufficiente"
    },


    # callback

    "wallet_address_confirmation": {
        "en": """
Your bitcoin wallet address has been set to : 
<strong>{wallet_address}</strong>

You can now make a <b>withdrawal</b>
                """,
        "it": """
Il tuo indirizzo di portafoglio bitcoin è stato impostato su : 
<strong>{wallet_address}</strong>

Ora puoi effettuare un <b>prelievo</b>
                """
    },

    "payout_processing_text": {
        "en": f"""Your payout request will be processed within the next 48 hours""",
        "it": f"""La Vostra richiesta di pagamento sarà eseguita entro le prossime 48 ore"""
    },

    # transaction


    "transaction_text_info": {
        "en": """
    <b>Deposits:</b>
    .....  
    {text_deposit}
    <b>Payouts:</b>
    .....
    {text_payout}
    <b>Reinvestments:</b>
    ......
    {text_reinvestments}
    <b>Commissions:</b>
    .....
    {text_commissions}

            """,
        "it": """
    <b>Depositi:</b>
    .....
    {text_deposit}
    <b>Pagamenti:</b>
    .....
    {text_payout}
    <b>Reinvestimenti:</b>
    ......
    {text_reinvestments}
    <b>Commissioni:</b>
    .....
    {text_commissions}

            """
    },


    # Team


    "invitation_link": {
        "en": """
Invitation link to share with your friends:
https://t.me/{bot_name}?start={user_id}
    """,
        "it": """
Link di invito da condividere con i Vostri amici:
https://t.me/{bot_name}?start={user_id}
    """
    },

    # Withdrawal


    "withdrawal_amount_text": {
        "en": """<b>Enter the amount you wish to withdraw</b>""",
        "it": """Enter the amount you wish to withdraw(italian"""
    },

    "withdrawal_info": {
        "en": f"""
You can create a payout request any time, depending on your account balance.
Minimum amount to withdraw is 0.002 BTC.
        """,
        "it": f"""
E’ possibile fare una richiesta di pagamento in qualsiasi momento, a seconda del saldo del Vostro conto.
L’importo minimo di prelievo è di 0,002 BTC.
        """
    },
    "insufficient_funds": {
        "en": """
You don't have enough funds to create a payout request
        """,
        "it": """
Non avete abbastanza fondi per creare una richiesta di pagamento.
        """
    },

    "set_wallet_address_text": {
        'en': "<b>Set your BTC wallet address</b>",
        'it': "<b>Imposta l'indirizzo del tuo portafoglio BTC</b>"
    },

    "invalid_amount": {
        "en": "Invalid amount please insert number",
        "it": "Importo non valido inserire il numero"
    },
    "withdraw_address_confirmation": {
        "en": """
    Withdrawal Amount: <b>{amount}</b>
    Payment Address: <b>{wallet_address}</b>
    """,
        "it": """
    Importo prelievo: <b>{amount}</b>
    indirizzo di pagamento: <b>{wallet_address}</b>
            """
    },

    "invalid_address": {
        "en": f"""Invalid address""",
        "it": f"""Invalid address"""
    },
}
