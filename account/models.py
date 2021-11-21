from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from binance.client import Client
from dashboard.models import AssetHistory, OrderHistory
import decimal


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password, publicKey, secretKey):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        if not password:
            raise ValueError("Users must have a password.")
        if not publicKey:
            raise ValueError("Users must have a public key.")
        if not secretKey:
            raise ValueError("Users must have a secret key.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            publicKey=publicKey,
            secretKey=secretKey
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, publicKey, secretKey):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            publicKey=publicKey,
            secretKey=secretKey
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    publicKey = models.CharField(max_length=100, unique=True)
    secretKey = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    trade_btc = models.BooleanField(default=False)
    trade_eth = models.BooleanField(default=False)
    trade_xrp = models.BooleanField(default=False)
    trade_ltc = models.BooleanField(default=False)
    trade_bch = models.BooleanField(default=False)
    trade_ada = models.BooleanField(default=False)
    trade_bnb = models.BooleanField(default=False)
    trade_link = models.BooleanField(default=False)
    trade_dot = models.BooleanField(default=False)
    trade_xlm = models.BooleanField(default=False)
    balance_btc = models.FloatField(default=0)
    balance_eth = models.FloatField(default=0)
    balance_xrp = models.FloatField(default=0)
    balance_ltc = models.FloatField(default=0)
    balance_bch = models.FloatField(default=0)
    balance_ada = models.FloatField(default=0)
    balance_bnb = models.FloatField(default=0)
    balance_link = models.FloatField(default=0)
    balance_dot = models.FloatField(default=0)
    balance_xlm = models.FloatField(default=0)
    balance_usdt = models.FloatField(default=1000)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'  # will be used to login
    REQUIRED_FIELDS = ['username', 'password', 'publicKey', 'secretKey']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_client(self):
        try:
            self.client = Client(self.publicKey, self.secretKey)
            return 1
        except:
            return 0

    def get_balances(self):
        # try:
            # result = self.client.get_account()
        balances = {}
        if self.balance_btc > 0:
            balances['BTC'] = self.balance_btc

        if self.balance_eth > 0:
            balances['ETH'] = self.balance_eth

        if self.balance_xrp > 0:
            balances['XRP'] = self.balance_xrp

        if self.balance_ltc > 0:
            balances['LTC'] = self.balance_ltc

        if self.balance_bch > 0:
            balances['BCH'] = self.balance_bch

        if self.balance_ada > 0:
            balances['ADA'] = self.balance_ada

        if self.balance_bnb > 0:
            balances['BNB'] = self.balance_bnb

        if self.balance_link > 0:
            balances['LINK'] = self.balance_link

        if self.balance_dot > 0:
            balances['DOT'] = self.balance_dot

        if self.balance_xlm > 0:
            balances['XLM'] = self.balance_xlm

        if self.balance_usdt > 0:
            balances['USDT'] = self.balance_usdt

        if len(balances) == 0:
            balances['BTC'] = 0
            # balances['BTC'] = self.balance_btc
            #
            # balances['ETH'] = self.balance_eth
            #
            # balances['XRP'] = self.balance_xrp
            #
            # balances['LTC'] = self.balance_ltc
            #
            # balances['BCH'] = self.balance_bch
            #
            # balances['ADA'] = self.balance_ada
            #
            # balances['BNB'] = self.balance_bnb
            #
            # balances['LINK'] = self.balance_link
            #
            # balances['DOT'] = self.balance_dot
            #
            # balances['XLM'] = self.balance_xlm

        return balances

        # except:
        #     return 0

    def get_trade_quantity(self):
        self.count = 0
        self.quantity = 0
        # if (self.get_client()):
        if self.trade_btc:
            self.count += 1
        if self.trade_eth:
            self.count += 1
        if self.trade_xrp:
            self.count += 1
        if self.trade_ltc:
            self.count += 1
        if self.trade_bch:
            self.count += 1
        if self.trade_dot:
            self.count += 1
        if self.trade_link:
            self.count += 1
        if self.trade_ada:
            self.count += 1
        if self.trade_xlm:
            self.count += 1
        if self.trade_bnb:
            self.count += 1

        # result = self.client.get_asset_balance(asset='USDT')
        # balance = float(result['free'])
        balance = self.balance_usdt
        if self.count > 0:
            self.quantity = balance // self.count
        # else:
        #     return 0

    def trade(self, symbol, price, action):
        if self.count > 0:
            if symbol == "BTC" and self.trade_btc:
                self.order(symbol, price, action)

            if symbol == "ETH" and self.trade_eth:
                self.order(symbol, price, action)

            if symbol == "XRP" and self.trade_xrp:
                self.order(symbol, price, action)

            if symbol == "ADA" and self.trade_ada:
                self.order(symbol, price, action)

            if symbol == "LTC" and self.trade_ltc:
                self.order(symbol, price, action)

            if symbol == "BCH" and self.trade_bch:
                self.order(symbol, price, action)

            if symbol == "DOT" and self.trade_dot:
                self.order(symbol, price, action)

            if symbol == "LINK" and self.trade_link:
                self.order(symbol, price, action)

            if symbol == "BNB" and self.trade_bnb:
                self.order(symbol, price, action)

            if symbol == "XLM" and self.trade_xlm:
                self.order(symbol, price, action)

    def order(self, symbol, price, action):
        def round_down(value, decimals):
            with decimal.localcontext() as ctx:
                d = decimal.Decimal(value)
                ctx.rounding = decimal.ROUND_DOWN
                return round(d, decimals)

        try:
            if action == 1:
                if self.quantity > 11:
                    quantity = self.quantity / float(price)
                    if quantity > 50:
                        quantity = int(quantity)
                    elif quantity > 5:
                        quantity = round_down(quantity, 2)
                    else:
                        quantity = round_down(quantity, 4)

                    quantity = float(quantity)

                    if symbol == "BTC":
                        self.balance_btc += quantity

                    if symbol == "ETH":
                        self.balance_eth += quantity

                    if symbol == "XRP":
                        self.balance_xrp += quantity

                    if symbol == "ADA":
                        self.balance_ada += quantity

                    if symbol == "LTC":
                        self.balance_ltc += quantity

                    if symbol == "BCH":
                        self.balance_bch += quantity

                    if symbol == "DOT":
                        self.balance_dot += quantity

                    if symbol == "LINK":
                        self.balance_link += quantity

                    if symbol == "BNB":
                        self.balance_bnb += quantity

                    if symbol == "XLM":
                        self.balance_xlm += quantity

                    self.balance_usdt -= self.quantity
                    self.save()

                    o = OrderHistory(
                        user=self.id,
                        symbol=symbol,
                        price=price,
                        quantity=quantity,
                        type='BUY'
                    )
                    o.save()
                    # order = self.client.order_market_buy(
                    #     symbol=symbol + 'USDT',
                    #     quantity=quantity)
                    # orderId = order["orderId"]
                    # self.count -= 1
                    #
                    # while True:
                    #     currentOrder = self.client.get_order(symbol=symbol + 'USDT', orderId=orderId)
                    #     if currentOrder['status'] == 'FILLED':
                    #         o = OrderHistory(
                    #             user=self.id,
                    #             symbol=symbol,
                    #             price=order['fills'][0]['price'],
                    #             quantity=order['executedQty'],
                    #             type='BUY'
                    #         )
                    #         o.save()
                    #         break

            if action == 2:
                # result = self.client.get_asset_balance(asset=symbol)
                # balance = float(result['free'])
                if symbol == "BTC":
                    balance = self.balance_btc

                if symbol == "ETH":
                    balance = self.balance_eth

                if symbol == "XRP":
                    balance = self.balance_xrp

                if symbol == "ADA":
                    balance = self.balance_ada

                if symbol == "LTC":
                    balance = self.balance_ltc

                if symbol == "BCH":
                    balance = self.balance_bch

                if symbol == "DOT":
                    balance = self.balance_dot

                if symbol == "LINK":
                    balance = self.balance_link

                if symbol == "BNB":
                    balance = self.balance_bnb

                if symbol == "XLM":
                    balance = self.balance_xlm

                if balance * float(price) > 11:
                    if balance > 50:
                        balance = int(balance)
                    elif balance > 5:
                        balance = round_down(balance, 2)
                    else:
                        balance = round_down(balance, 4)

                    balance = float(balance)

                    if symbol == "BTC":
                        self.balance_btc -= balance

                    if symbol == "ETH":
                        self.balance_eth -= balance

                    if symbol == "XRP":
                        self.balance_xrp -= balance

                    if symbol == "ADA":
                        self.balance_ada -= balance

                    if symbol == "LTC":
                        self.balance_ltc -= balance

                    if symbol == "BCH":
                        self.balance_bch -= balance

                    if symbol == "DOT":
                        self.balance_dot -= balance

                    if symbol == "LINK":
                        self.balance_link -= balance

                    if symbol == "BNB":
                        self.balance_bnb -= balance

                    if symbol == "XLM":
                        self.balance_xlm -= balance

                    self.balance_usdt += balance * float(price)
                    self.save()

                    o = OrderHistory(
                        user=self.id,
                        symbol=symbol,
                        price=price,
                        quantity=balance,
                        type='SELL'
                    )
                    o.save()
                    # order = self.client.order_market_sell(
                    #     symbol=symbol + 'USDT',
                    #     quantity=balance)
                    # orderId = order["orderId"]
                    # while True:
                    #     currentOrder = self.client.get_order(symbol=symbol + 'USDT', orderId=orderId)
                    #     if currentOrder['status'] == 'FILLED':
                    #         o = OrderHistory(
                    #             user=self.id,
                    #             symbol=symbol,
                    #             price=order['fills'][0]['price'],
                    #             quantity=order['executedQty'],
                    #             type='SELL'
                    #         )
                    #         o.save()
                    #         break

        except Exception as e:
            print("Error", e)

    def save_pnl(self, price_list):
        # self.get_client()
        # balances = self.get_balances()
        # if balances == 0:
        #     return
        #
        # try:
        #     usdt = balances['USDT']
        # except:
        #     usdt = 0
        #
        # sum = 0
        # for key in balances:
        #     if str(key) in price_list:
        #         sum += balances[str(key)] * float(price_list[str(key)])
        sum = 0
        sum += self.balance_btc
        sum += self.balance_eth
        sum += self.balance_xrp
        sum += self.balance_ada
        sum += self.balance_ltc
        sum += self.balance_bnb
        sum += self.balance_bch
        sum += self.balance_link
        sum += self.balance_dot
        sum += self.balance_xlm
        sum += self.balance_usdt

        asset = AssetHistory(
            user=self.id,
            value=sum
        )
        asset.save()

    def get_pnl_last(self):
        try:
            pnl = AssetHistory.objects.filter(user=self.id).order_by('-time').first()
            return pnl.value
        except:
            return 0

    def get_pnl_all(self):
        pnl_dict = {}
        try:
            pnl = AssetHistory.objects.filter(user=self.id)
            for p in pnl:
                pnl_dict[str(p.time.date())] = str(p.value)
            return pnl_dict
        except:
            return pnl_dict

    def get_order_history(self, *args):
        order_list = []
        order_count = OrderHistory.objects.filter(user=self.id).count()

        if args:
            orders = OrderHistory.objects.filter(time__range=[args[0], args[1]], user=self.id).order_by('-time')
        elif order_count > 50:
            orders = OrderHistory.objects.filter(user=self.id).order_by('-time')[:50]
        elif order_count > 0:
            orders = OrderHistory.objects.filter(user=self.id).order_by('-time')
        else:
            return order_list

        for i, order in enumerate(orders):
            o = {}
            o['date'] = order.time.date()
            o['time'] = order.time.time()
            o['symbol'] = order.symbol
            o['price'] = str(round(order.price, 4))
            o['quantity'] = str(round(order.quantity, 4))
            o['type'] = order.type
            order_list.append(o)

        return order_list
