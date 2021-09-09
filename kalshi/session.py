import os
import requests

class Session():
    """A Kalshi session.  All API requests are defined on this class."""
    def __init__(self, email=None, password=None,
                 endpoint='https://trading-api.kalshi.com/v1'):
        """Create a new Kalshi session.

        :param str email: The email you use to log in.  (This can also be configured with the KALSHI_EMAIL environment variable.)
        :param str password: The password you use to log in.  (This can also be configured with the KALSHI_PASSWORD environment variable.)
        :param str endpoint: The Kalshi API endpoint.  Defaults to the public v1 API.
        """
        if email is None:
            if 'KALSHI_EMAIL' not in os.environ:
                raise RuntimeError(
                    "kalshi.Session needs to know your email.  "+
                    "Either provide `email` as a keyword argument "+
                    "or set `KALSHI_EMAIL` in the environment.")
            email = os.environ['KALSHI_EMAIL']
        if password is None:
            if 'KALSHI_PASSWORD' not in os.environ:
                raise RuntimeError(
                    "kalshi.Session needs to know your password.  "+
                    "Either provide `password` as a keyword argument "+
                    "or set `KALSHI_PASSWORD` in the environment.")
            password = os.environ['KALSHI_PASSWORD']
        self.endpoint = endpoint

        res = requests.post(endpoint+'/log_in', json={'email': email, 'password': password})
        if res.status_code != 200:
            raise RuntimeError('kalshi.Session failed to log in (%s) (%s)' %
                               (res.status_code, res.text))

        parsed = res.json()
        self.token = parsed['token']
        self.user_id = parsed['user_id']

    def post(self, path, obj=None):
        if obj is not None and obj != {}:
            res = requests.post(self.endpoint+path, json=obj, headers={'Authorization': self.token})
        else:
            res = requests.post(self.endpoint+path, headers={'Authorization': self.token})
        if res.status_code != 200:
            raise RuntimeError('Error from Kalshi API (%s) (%s)' % (res.status_code, res.text))
        return res.json()

    def get(self, path, obj=None):
        if obj is not None and obj != {}:
            res = requests.get(self.endpoint+path, json=obj, headers={'Authorization': self.token})
        else:
            res = requests.get(self.endpoint+path, headers={'Authorization': self.token})
        if res.status_code != 200:
            raise RuntimeError('Error from Kalshi API (%s) (%s)' % (res.status_code, res.text))
        return res.json()

    def get_markets_cached(self):
        return self.get(f'/cached/markets', None)

    def get_market_history_cached(self, market_id, last_seen_ts=None):
        return self.get(f'/cached/markets/{market_id}/stats_history', dict((x, y) for x, y in [('last_seen_ts', last_seen_ts)] if y is not None))

    def get_exchange_status(self):
        return self.get(f'/exchange/status', None)

    def login_mfa(self):
        return self.post(f'/log_in_mfa', None)

    def logout(self):
        return self.post(f'/log_out', None)

    def get_markets(self):
        return self.get(f'/markets', None)

    def get_market_cached(self, market_id):
        return self.get(f'/markets/{market_id}', None)

    def get_market_order_book_cached(self, market_id):
        return self.get(f'/markets/{market_id}/order_book', None)

    def get_market_history(self, market_id, last_seen_ts=None):
        return self.get(f'/markets/{market_id}/stats_history', dict((x, y) for x, y in [('last_seen_ts', last_seen_ts)] if y is not None))

    def reset_password(self):
        return self.post(f'/passwords/reset', None)

    def reset_password_confirm(self, code):
        return self.put(f'/passwords/reset/{code}/confirm', None)

    def user_create(self):
        return self.post(f'/users', None)

    def user_get_profile(self, user_id):
        return self.get(f'/users/{user_id}', None)

    def user_update_profile(self, user_id):
        return self.put(f'/users/{user_id}', None)

    def user_get_account_history(self, user_id, ShouldReturnDeposits=None, ShouldReturnWithdrawals=None, ShouldReturnOrders=None, ShouldReturnSettlements=None, ShouldReturnTrades=None, Limit=None):
        return self.get(f'/users/{user_id}/account/history', dict((x, y) for x, y in [('ShouldReturnDeposits', ShouldReturnDeposits), ('ShouldReturnWithdrawals', ShouldReturnWithdrawals), ('ShouldReturnOrders', ShouldReturnOrders), ('ShouldReturnSettlements', ShouldReturnSettlements), ('ShouldReturnTrades', ShouldReturnTrades), ('Limit', Limit)] if y is not None))

    def user_get_balance(self, user_id):
        return self.get(f'/users/{user_id}/balance', None)

    def user_list_ledgerx_bank_accounts(self, user_id):
        return self.get(f'/users/{user_id}/banks/linked_accounts', None)

    def user_link_bank_accounts(self, user_id):
        return self.post(f'/users/{user_id}/banks/linked_accounts', None)

    def get_user_deposits(self, user_id, page_size=None, page_number=None):
        return self.get(f'/users/{user_id}/deposits', dict((x, y) for x, y in [('page_size', page_size), ('page_number', page_number)] if y is not None))

    def user_request_deposit(self, user_id):
        return self.post(f'/users/{user_id}/deposits', None)

    def user_send_email_confirmation(self, user_id):
        return self.post(f'/users/{user_id}/email_confirmation', None)

    def user_get_kyc(self, user_id):
        return self.get(f'/users/{user_id}/kyc', None)

    def user_update_kyc(self, user_id):
        return self.put(f'/users/{user_id}/kyc', None)

    def user_get_notifications(self, user_id, page_size=None, page_number=None):
        return self.get(f'/users/{user_id}/notifications', dict((x, y) for x, y in [('page_size', page_size), ('page_number', page_number)] if y is not None))

    def notification_mark_read(self, user_id, notification_id):
        return self.put(f'/users/{user_id}/notifications/{notification_id}/read', None)

    def get_notification_preferences(self, user_id):
        return self.get(f'/users/{user_id}/notifications/preferences', None)

    def user_orders_get(self, user_id, market_id=None, is_yes=None, min_price=None, max_price=None, min_place_count=None, max_place_count=None, min_initial_count=None, max_initial_count=None, min_remaining_count=None, max_remaining_count=None, min_date=None, max_date=None):
        return self.get(f'/users/{user_id}/orders', dict((x, y) for x, y in [('market_id', market_id), ('is_yes', is_yes), ('min_price', min_price), ('max_price', max_price), ('min_place_count', min_place_count), ('max_place_count', max_place_count), ('min_initial_count', min_initial_count), ('max_initial_count', max_initial_count), ('min_remaining_count', min_remaining_count), ('max_remaining_count', max_remaining_count), ('min_date', min_date), ('max_date', max_date)] if y is not None))

    def user_order_create(self, user_id):
        return self.post(f'/users/{user_id}/orders', None)

    def user_order_cancel(self, user_id, order_id):
        return self.delete(f'/users/{user_id}/orders/{order_id}', None)

    def user_order_decrease(self, user_id, order_id):
        return self.post(f'/users/{user_id}/orders/{order_id}/decrease', None)

    def user_change_password(self, user_id):
        return self.put(f'/users/{user_id}/password', None)

    def user_create_plaid_link_token(self, user_id):
        return self.post(f'/users/{user_id}/plaid/link_token', None)

    def user_get_portfolio_history(self, user_id):
        return self.get(f'/users/{user_id}/portfolio/history', None)

    def user_get_market_positions(self, user_id):
        return self.get(f'/users/{user_id}/positions', None)

    def user_get_market_position(self, user_id, market_id):
        return self.get(f'/users/{user_id}/positions/{market_id}', None)

    def change_subscription(self, user_id):
        return self.put(f'/users/{user_id}/subscribe', None)

    def user_trades_get(self, user_id, market_id=None, order_id=None, MinPrice=None, MaxPrice=None, MinCount=None, max_count=None, min_date=None, max_date=None):
        return self.get(f'/users/{user_id}/trades', dict((x, y) for x, y in [('market_id', market_id), ('order_id', order_id), ('MinPrice', MinPrice), ('MaxPrice', MaxPrice), ('MinCount', MinCount), ('max_count', max_count), ('min_date', min_date), ('max_date', max_date)] if y is not None))

    def user_verify(self, user_id):
        return self.post(f'/users/{user_id}/verify', None)

    def user_get_watchlist(self, user_id):
        return self.get(f'/users/{user_id}/watchlist', None)

    def user_remove_watchlist(self, user_id, market_id):
        return self.delete(f'/users/{user_id}/watchlist/{market_id}', None)

    def user_add_watchlist(self, user_id, market_id):
        return self.put(f'/users/{user_id}/watchlist/{market_id}', None)

    def get_user_withdrawals(self, user_id, page_size=None, page_number=None):
        return self.get(f'/users/{user_id}/withdrawals', dict((x, y) for x, y in [('page_size', page_size), ('page_number', page_number)] if y is not None))

    def user_request_withdrawal(self, user_id):
        return self.post(f'/users/{user_id}/withdrawals', None)

    def send_sign_up_link(self):
        return self.post(f'/users/resume_sign_up', None)

