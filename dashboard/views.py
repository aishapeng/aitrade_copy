from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm
from .models import Cryptocurrency
from .api_request import get_kline
from datetime import datetime


def home_view(request):
    welcome_msg = "The bridge to the world of cryptocurrency. AiTrade is an automated cryptocurrency trading bot. " \
                  "The aim of this project is to expose the idea and usage of cryptocurrency. At the same time, " \
                  "utilising the power of machine learning to earn profits for all audience. This is a leading platform" \
                  "that leverages bleeding-edge technology to navigate in the volatile crypto markets. Uncovering the " \
                  "potential of fintech."
    how_it_works = "An artificial intelligence model was trained using historical prices data of the cryptocurrencies. " \
                   "Technical indicators are then applied on the data and fed to the model. By interacting with the environment" \
                   "thousands of times repeatedly, the model eventually learned the characteristics of the markets to make " \
                   "profitable trades. To use this platform, you just have to create an account and bind your Binance API to " \
                   "the account."
    context = {
        'welcome_msg': welcome_msg,
        'how_it_works': how_it_works,
    }
    return render(request, 'dashboard/home.html', context)


def getting_started_view(request):
    binance_msg = "Binance is a cryptocurrency exchange which is currently the largest exchange in the world. As of now, " \
                  "AiTrade only supports the Binance exchange. In order to use our service, a Binance account is required. "
    api_msg = "Creating an API allows us to connect you to Binance’s servers. It allows us to automatically place trades for you, " \
              "and allow you to monitor you asset allocation, asset balance, order history, and profit and loss analysis. "
    context = {
        'binance_msg': binance_msg,
        'api_msg': api_msg,
    }
    return render(request, 'dashboard/gettingstarted.html', context)


def help_view(request):
    form = ContactForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email_message = form.cleaned_data['message']
            msg = "From: " + form.cleaned_data['email'] + "\n" + email_message
            subject = "AiTrade Help: " + form.cleaned_data['name']
            send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL], fail_silently=True)
            sent = True
            context = {
                'form': form,
                'sent': sent
            }
        else:
            context['form'] = form
    return render(request, 'dashboard/help.html', context)


def index(request, symbol="BTC"):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if request.method == 'GET' and 'start' in request.GET:
        order_start = request.GET.get('start', datetime.today().strftime('%Y-%m-%d'))
        order_end = request.GET.get('end', datetime.today().strftime('%Y-%m-%d'))
        order_list = user.get_order_history(order_start, order_end)
    else:
        order_list = user.get_order_history()

    # Order history paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(order_list, 8)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    # user.get_client()  # connect to Binance api
    balances = user.get_balances()
    usdt = user.balance_usdt
    # try:
    #     usdt = round(balances['USDT'], 2)
    # except:
    #     usdt = 0

    pnl_last = user.get_pnl_last()
    pnl_all = user.get_pnl_all()
    kline = get_kline(symbol)
    coin_list = Cryptocurrency.objects.all()

    context = {
        'symbol': symbol,
        'coin_list': coin_list,
        'balances': mark_safe(balances),
        'usdt': usdt,
        'kline': mark_safe(kline),
        'pnl_last': pnl_last,
        'pnl_all': mark_safe(pnl_all),
        'orders': orders,
        'trade_btc': user.trade_btc,
        'trade_eth': user.trade_eth,
        'trade_xrp': user.trade_xrp,
        'trade_ltc': user.trade_ltc,
        'trade_bch': user.trade_bch,
        'trade_ada': user.trade_ada,
        'trade_bnb': user.trade_bnb,
        'trade_link': user.trade_link,
        'trade_dot': user.trade_dot,
        'trade_xlm': user.trade_xlm,
    }

    if request.POST:
        tradeCoin = request.POST['symbol']
        isTrade = request.POST['trade']
        if tradeCoin == 'BTC':
            user.trade_btc = isTrade
        if tradeCoin == 'ETH':
            user.trade_eth = isTrade
        if tradeCoin == 'XRP':
            user.trade_xrp = isTrade
        if tradeCoin == 'LTC':
            user.trade_ltc = isTrade
        if tradeCoin == 'BCH':
            user.trade_bch = isTrade
        if tradeCoin == 'ADA':
            user.trade_ada = isTrade
        if tradeCoin == 'BNB':
            user.trade_bnb = isTrade
        if tradeCoin == 'LINK':
            user.trade_link = isTrade
        if tradeCoin == 'DOT':
            user.trade_dot = isTrade
        if tradeCoin == 'XLM':
            user.trade_xlm = isTrade
        user.save()

    return render(request, 'dashboard/index.html', context)
