import os
import requests

class Session():
    """A Kalshi session.  All API requests are defined on this class.

       :param str email: The email you use to log in.  (This can also be configured with the KALSHI_EMAIL environment variable.)
       :param str password: The password you use to log in.  (This can also be configured with the KALSHI_PASSWORD environment variable.)
       :param str endpoint: The Kalshi API endpoint.  Defaults to the public v1 API.
"""
    def __init__(self, email=None, password=None,
                 endpoint='https://trading-api.kalshi.com/v1'):
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
        self.access_level = parsed['access_level']

    def _http_op(self, op, path, obj=None):
        headers = {'Authorization': 'Basic ' + self.token}
        if obj is not None and obj != {}:
            res = getattr(requests, op)(self.endpoint+path, json=obj, headers=headers)
        else:
            res = getattr(requests, op)(self.endpoint+path, headers=headers)
        if res.status_code != 200:
            raise RuntimeError('Error from Kalshi API (%s) (%s)' % (res.status_code, res.text))
        return res.json()


    def get_markets_cached(self):
        """End-point for listing / discovering markets on Kalshi with data that is cached and so slightly lagged.

"""
        return self._http_op('get', f'/cached/markets', None)

    def get_market_history_cached(self, market_id, last_seen_ts=None):
        """End-point for getting the statistics history for a market with data that is cached and so slightly lagged.

The value for the market_id path parameter should match the id value of the target market.
The last_seen_ts parameter is optional, and will restrict statistics to those after provided timestamp.
The last_seen_ts is inclusive, which means a market history point at last_seen_ts will be returned

:param string market_id: Should be filled with the id of the target market
:param integer last_seen_ts: If provided, restricts history to trades starting from lastSeenTs
"""
        return self._http_op('get', f'/cached/markets/{market_id}/stats_history', dict((x, y) for x, y in [('last_seen_ts', last_seen_ts)] if y is not None))

    def get_exchange_status(self):
        """End-point for getting the exchange status

"""
        return self._http_op('get', f'/exchange/status', None)

    def login_mfa(self):
        """End-point to start a rest session with Kalshi, when you have 2FA enabled.

Before calling this end-point you should call (POST /log_in) using email and password.

"""
        return self._http_op('post', f'/log_in_mfa', None)

    def logout(self):
        """End-point to terminates your session with Kalshi.

"""
        return self._http_op('post', f'/log_out', None)

    def get_markets(self):
        """End-point for listing / discovering markets on Kalshi.

"""
        return self._http_op('get', f'/markets', None)

    def get_market_cached(self, market_id):
        """End-point for getting data about a specific market with data that is cached and so slightly lagged.

The value for the market_id path parameter should match the id value of the target market.

:param string market_id: Should be filled with the id of the target market
"""
        return self._http_op('get', f'/markets/{market_id}', None)

    def get_market_order_book_cached(self, market_id):
        """End-point for getting the orderbook for a market with data that is cached and so slightly lagged.

The value for the market_id path parameter should match the id value of the target market.

:param string market_id: Should be filled with the id of the target market
"""
        return self._http_op('get', f'/markets/{market_id}/order_book', None)

    def get_market_history(self, market_id, last_seen_ts=None):
        """End-point for getting the statistics history for a market.

The value for the market_id path parameter should match the id value of the target market.
The last_seen_ts parameter is optional, and will restrict statistics to those after provided timestamp.
The last_seen_ts is inclusive, which means a market history point at last_seen_ts will be returned

:param string market_id: Should be filled with the id of the target market
:param integer last_seen_ts: If provided, restricts history to trades starting from lastSeenTs
"""
        return self._http_op('get', f'/markets/{market_id}/stats_history', dict((x, y) for x, y in [('last_seen_ts', last_seen_ts)] if y is not None))

    def reset_password(self):
        """End-point to request a password reset email link.

To be used in case you forget your password.

"""
        return self._http_op('post', f'/passwords/reset', None)

    def reset_password_confirm(self, code):
        """End-point to finish the password reset flow.

The code param on the path should be filled with the verification code sent by email.

:param string code: Should be filled with the verification code received on the sign-up email.
"""
        return self._http_op('put', f'/passwords/reset/{code}/confirm', None)

    def user_create(self):
        """End-point for creating an user. A call to this end-point starts the sign-up flow.

"""
        return self._http_op('post', f'/users', None)

    def user_get_profile(self, user_id=None):
        """End-point for retrieving the logged in user's profile.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}', None)

    def user_update_profile(self, user_id=None):
        """End-point for submitting your user profile during sign-up, or updating it after sign-up is complete.

The value for the user_id path parameter should match the user_id value returned either in the response for the last login request (POST /log_in) or for the create user request (POST /users).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('put', f'/users/{user_id}', None)

    def user_get_account_history(self, user_id=None, ShouldReturnDeposits=None, user_id=None, ShouldReturnWithdrawals=None, user_id=None, ShouldReturnOrders=None, user_id=None, ShouldReturnSettlements=None, user_id=None, ShouldReturnTrades=None, user_id=None, Limit=None, user_id=None):
        """End-point for getting the logged in user's important past actions and events related to the user's positions.

This contains entries for user's explicit actions but also for market events.

There will be entries for:

submitting, editing / canceling orders
requesting deposits and withdrawals
trade execution (order matching)
market settlements on markets where you have a position

The value for the user_id path parameter should match the user_id value returned on the response for the
last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param boolean ShouldReturnDeposits: If true the response should include deposit entries
:param boolean ShouldReturnWithdrawals: If true the response should include withdrawal entries
:param boolean ShouldReturnOrders: If true the response should include order entries
:param boolean ShouldReturnSettlements: If true the response should include settlement entries
:param boolean ShouldReturnTrades: If true the response should include trade entries
:param integer Limit: Restricts the response to a return the first "limit" amount of acct history items
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/account/history', dict((x, y) for x, y in [('ShouldReturnDeposits', ShouldReturnDeposits), ('ShouldReturnWithdrawals', ShouldReturnWithdrawals), ('ShouldReturnOrders', ShouldReturnOrders), ('ShouldReturnSettlements', ShouldReturnSettlements), ('ShouldReturnTrades', ShouldReturnTrades), ('Limit', Limit)] if y is not None))

    def user_get_balance(self, user_id=None):
        """End-point for getting the balance of the logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/balance', None)

    def user_list_ledgerx_bank_accounts(self, user_id=None):
        """End-point for getting connected accounts from the clearing house.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/banks/linked_accounts', None)

    def user_link_bank_accounts(self, user_id=None):
        """End-point for submitting to finish bank account linking.

This end-point sends the bank accounts connected by the user in the front-end to our clearing house.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/banks/linked_accounts', None)

    def get_user_deposits(self, user_id=None, page_size=None, user_id=None, page_number=None, user_id=None):
        """End-point for getting all deposits for the logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param integer page_size: Number of deposits in each page.
:param integer page_number: Number of the page to be retrieved.
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/deposits', dict((x, y) for x, y in [('page_size', page_size), ('page_number', page_number)] if y is not None))

    def user_request_deposit(self, user_id=None):
        """End-point for starting deposits on the logged in user's account.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

In order to request deposits you need to have connected at least one account using (POST /user/{user_id}/banks/linked_accounts).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/deposits', None)

    def user_send_email_confirmation(self, user_id=None):
        """End-point for re-sending email verification. To be used in case e-mail verification doesn't arrive or verification code is expired.

The value for the user_id path parameter should match the user_id value returned on the response for the create user request (POST /users).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/email_confirmation', None)

    def user_get_kyc(self, user_id=None):
        """End-point for retrieving your user kyc profile.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/kyc', None)

    def user_update_kyc(self, user_id=None):
        """End-point for submitting / updating your user kyc profile during sign-up.

The value for the user_id path parameter should match the user_id value returned on the response for the create user request (POST /users).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('put', f'/users/{user_id}/kyc', None)

    def user_get_notifications(self, user_id=None, page_size=None, user_id=None, page_number=None, user_id=None):
        """End-point for getting notifications for the current logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param integer page_size: Optional parameter to specify the number of results per page
:param integer page_number: Optional parameter to specify which page of the results should be retrieved
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/notifications', dict((x, y) for x, y in [('page_size', page_size), ('page_number', page_number)] if y is not None))

    def notification_mark_read(self, user_id=None, notification_id, user_id=None):
        """End-point for marking a notification as read.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

The value for the notification_id path parameter should match the notification_id value of the notification to be marked as read.

:param string user_id: user_id should be filled with your user_id provided on log_in
:param string notification_id: notification_id should be filled with the id of the notification to be mark as read
"""
        user_id = user_id or self.user_id
        return self._http_op('put', f'/users/{user_id}/notifications/{notification_id}/read', None)

    def get_notification_preferences(self, user_id=None):
        """End-point for getting e-mail subscription mode for the current user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/notifications/preferences', None)

    def user_orders_get(self, user_id=None, market_id=None, user_id=None, is_yes=None, user_id=None, min_price=None, user_id=None, max_price=None, user_id=None, min_place_count=None, user_id=None, max_place_count=None, user_id=None, min_initial_count=None, user_id=None, max_initial_count=None, user_id=None, min_remaining_count=None, user_id=None, max_remaining_count=None, user_id=None, min_date=None, user_id=None, max_date=None, user_id=None):
        """End-point for getting all orders for the logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param string market_id: Restricts the response to orders in a single market
:param boolean is_yes: Restricts the response to orders in a single direction (yes or no)
:param integer min_price: Restricts the response to orders within a minimum price
:param integer max_price: Restricts the response to orders within a maximum price
:param integer min_place_count: Restricts the response to orders within a minimum place count
:param integer max_place_count: Restricts the response to orders within a maximum place count
:param integer min_initial_count: Restricts the response to orders within a minimum initial count
:param integer max_initial_count: Restricts the response to orders within a maximum initial count
:param integer min_remaining_count: Restricts the response to orders within a minimum remaining resting contracts count
:param integer max_remaining_count: Restricts the response to orders within a maximum remaining resting contracts count
:param string min_date: Restricts the response to orders after a timestamp
:param string max_date: Restricts the response to orders before a timestamp
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/orders', dict((x, y) for x, y in [('market_id', market_id), ('is_yes', is_yes), ('min_price', min_price), ('max_price', max_price), ('min_place_count', min_place_count), ('max_place_count', max_place_count), ('min_initial_count', min_initial_count), ('max_initial_count', max_initial_count), ('min_remaining_count', min_remaining_count), ('max_remaining_count', max_remaining_count), ('min_date', min_date), ('max_date', max_date)] if y is not None))

    def user_order_create(self, user_id=None):
        """End-point for submitting orders in a market.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/orders', None)

    def user_order_cancel(self, user_id=None, order_id, user_id=None):
        """End-point for canceling orders.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).
The value for the order_id should match the id field of the order you want to decrease.
Commonly delete end-points return 204 status with no body content on success.
But we can't completely delete the order, as it may be partially filled already.
So what the delete end-point does is just reducing the order completely zeroing the remaining resting contracts on it.
The zeroed order is returned on the response payload, as a form of validation for the client.

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param string order_id: This order_id should be filled with the id of the order to be decrease
"""
        user_id = user_id or self.user_id
        return self._http_op('delete', f'/users/{user_id}/orders/{order_id}', None)

    def user_order_decrease(self, user_id=None, order_id, user_id=None):
        """End-point for decreasing the number of contracts on orders. This is the only kind of edit we support on orders.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

The value for the order_id should match the id field of the order you want to decrease.

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param string order_id: This order_id should be filled with the id of the order to be decrease
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/orders/{order_id}/decrease', None)

    def user_change_password(self, user_id=None):
        """End-point for updating logged-in user password.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('put', f'/users/{user_id}/password', None)

    def user_create_plaid_link_token(self, user_id=None):
        """End-point for creating a link token. This is required to be able to connect bank accounts via Plaid.

Look at plaid docs (https://plaid.com/docs/api/tokens/#linktokencreate) for more information on the token and how plaid works.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/plaid/link_token', None)

    def user_get_portfolio_history(self, user_id=None):
        """End-point for getting the logged in user's portfolio historical track.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/portfolio/history', None)

    def user_get_market_positions(self, user_id=None):
        """End-point for getting all market positions for the logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/positions', None)

    def user_get_market_position(self, user_id=None, market_id, user_id=None):
        """End-point for getting the market positions for the logged in user, in a specific market.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

The value for the market_id path parameter should match the id value of the target market.

:param string user_id: Should be filled with your user_id provided on log_in
:param string market_id: Should be filled with the id of the target market
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/positions/{market_id}', None)

    def change_subscription(self, user_id=None):
        """End-point for changing e-mail subscription mode for the current user.

This end-point is very useful for users that have a large volume of orders and don't want to be email notified whenever an order is submitted / edited / canceled or matches.

This is specially useful for Market Makers.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('put', f'/users/{user_id}/subscribe', None)

    def user_trades_get(self, user_id=None, market_id=None, user_id=None, order_id=None, user_id=None, MinPrice=None, user_id=None, MaxPrice=None, user_id=None, MinCount=None, user_id=None, max_count=None, user_id=None, min_date=None, user_id=None, max_date=None, user_id=None):
        """End-point for getting all trades for the logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param string market_id: Restricts the response to trades in a specific market.
:param string order_id: Restricts the response to trades related to a specific order.
:param integer MinPrice: Restricts the response to trades within a minimum price.
:param integer MaxPrice: Restricts the response to trades within a maximum price.
:param integer MinCount: Restricts the response to trades within a minimum contracts count.
:param integer max_count: Restricts the response to trades within a maximum contracts count.
:param string min_date: Restricts the response to trades after a timestamp.
:param string max_date: Restricts the response to trades before a timestamp.
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/trades', dict((x, y) for x, y in [('market_id', market_id), ('order_id', order_id), ('MinPrice', MinPrice), ('MaxPrice', MaxPrice), ('MinCount', MinCount), ('max_count', max_count), ('min_date', min_date), ('max_date', max_date)] if y is not None))

    def user_verify(self, user_id=None):
        """End-point for completing email verification during sign-up.

The value for the user_id path parameter should match the user_id value returned on the email verification link query param.

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/verify', None)

    def user_get_watchlist(self, user_id=None):
        """End-point for getting the market watchlist for the logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: Should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/watchlist', None)

    def user_remove_watchlist(self, user_id=None, market_id, user_id=None):
        """End-point for removing a market from the logged in user's watchlist.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

The value for the market_id path parameter should match the id value of the market to be added.

:param string user_id: Should be filled with your user_id provided on log_in
:param string market_id: Should be filled with the id of the target market
"""
        user_id = user_id or self.user_id
        return self._http_op('delete', f'/users/{user_id}/watchlist/{market_id}', None)

    def user_add_watchlist(self, user_id=None, market_id, user_id=None):
        """End-point for adding a market to the logged in user's watchlist.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

The value for the market_id path parameter should match the id value of the market to be added.

:param string user_id: user_id should be filled with your user_id provided on log_in
:param string market_id: market_id should be filled with the id of the market to be added to the watchlist
"""
        user_id = user_id or self.user_id
        return self._http_op('put', f'/users/{user_id}/watchlist/{market_id}', None)

    def get_user_withdrawals(self, user_id=None, page_size=None, user_id=None, page_number=None, user_id=None):
        """End-point for getting all withdrawals for the logged in user.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

:param string user_id: This parameter should be filled with your user_id provided on log_in
:param integer page_size: Number of withdrawals in each page.
:param integer page_number: Number of the page to be retrieved.
"""
        user_id = user_id or self.user_id
        return self._http_op('get', f'/users/{user_id}/withdrawals', dict((x, y) for x, y in [('page_size', page_size), ('page_number', page_number)] if y is not None))

    def user_request_withdrawal(self, user_id=None):
        """End-point for starting deposits on the logged in user's account.

The value for the user_id path parameter should match the user_id value returned on the response for the last login request (POST /log_in).

In order to request deposits you need to have connected at least one account using (POST /user/{user_id}/banks/linked_accounts).

:param string user_id: This parameter should be filled with your user_id provided on log_in
"""
        user_id = user_id or self.user_id
        return self._http_op('post', f'/users/{user_id}/withdrawals', None)

    def send_sign_up_link(self):
        """End-point for sending a link to resume sign-up. To be used in case the user verification e-mail is lost.

"""
        return self._http_op('post', f'/users/resume_sign_up', None)

