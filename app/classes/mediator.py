import json


class Mediator():
    def __init__(self, bot, balance):
        self.bot = bot
        self.balance = balance
        with open('conf.json', 'r') as file:
            config = json.load(file)
        self.critical_balance = config['critical_balance']
        self.critical_hours_remaining = config['critical_hours_remaining']
        self.success_check_alerting = config['success_check_alerting']

    def handle_request(self, request):
        if request == "status":
            self.bot.send_message("Ready to handle requests")
        if request == "balance":
            self.handle_balance()
        if request == "settings":
            self.bot.send_message(
                f"Current settings: \n\nCritical balance: {self.critical_balance} ₽ \nCritical hours: {self.critical_hours_remaining} \nSuccess check alerting: {self.success_check_alerting}")

    def handle_balance(self):
        collecting_message_response = self.bot.send_message(
            "Collecting balances info...")
        if collecting_message_response:
            collecting_message_id = collecting_message_response['result']['message_id']
        else:
            collecting_message_id = False

        balance_notes = self.balance.get_all_balances()

        if collecting_message_id:
            self.bot.delete_message(collecting_message_id)

        for note in balance_notes:
            if note['status'] != 'ok':
                self.bot.send_message(
                    f"Can't get balance info for account: {note['account_id']}")
                continue
            message = f"\nAccount: {note['account_id']} \nBalance: {note['balance']} ₽ \nRemaining: ~{int(note['hours_remaining'] / 24)} days (~{note['hours_remaining']} hours)"
            self.bot.send_message(message)

    def check_balance_validity(self):
        balance_notes = self.balance.get_all_balances()
        for note in balance_notes:
            if note['status'] != 'ok':
                self.bot.send_message(
                    f"Can't get balance info for account: {note['account_id']}")
                continue
            if note['balance'] < self.critical_balance or note['hours_remaining'] < self.critical_hours_remaining:
                message = f"❗❗❗Balance parameter is less than the critical value \n({self.critical_balance} ₽ / {self.critical_hours_remaining} hours): \n\nAccount: {note['account_id']} \nBalance: {note['balance']} ₽ \nRemaining: ~{int(note['hours_remaining'] / 24)} days (~{note['hours_remaining']} hours)"
                self.bot.send_message(message)
            else:
                if self.success_check_alerting:
                    message = f"Account: {note['account_id']} checked \nBalance: OK"
                    self.bot.send_message(message)
