const endpoint = "wss://stream.binance.com:9443/stream?streams=";

// websocket for real time market price
function startWebsocket() {
    var streams = ""
    {% for coin in coin_list %}
            streams += '{{coin.symbol}}'.toLowerCase()+'usdt@ticker/';
    {% endfor %}
    streams = streams.substring(0, streams.length - 1);
    var stream = endpoint + streams;
    var ws = new WebSocket(stream);

    ws.onmessage = function(e){
        var data = JSON.parse(e.data);
        var changePercent = parseFloat(data['data'].P).toFixed(2);
        if  (parseFloat(data['data'].c) > 10){
            var lastPrice = parseFloat(data['data'].c).toFixed(2);
        }
        else{
            var lastPrice = parseFloat(data['data'].c).toFixed(4);
        }

        var idPrice = '#' + data['data'].s;
        var idPercent = '#' + data['data'].s + '-percent';
        $(idPrice).html(lastPrice);
        $(idPercent).html(changePercent+"%");
        if (changePercent.indexOf("-") != -1) {
            $(idPercent).parent().addClass("bg-danger");
        }
        else{
            $(idPercent).html("+"+changePercent+"%");
        }
        get_balance();
    }

    ws.onclose = function(){
        // connection closed, discard old websocket and create a new one in 5s
        ws = null
        setTimeout(startWebsocket, 5000)
    }
}

startWebsocket();

// update user asset value
function get_balance(){
    var sum = 0.0;
    {% for coin in coin_list %}
        if ( '{{coin.symbol}}' in {{balances}} ){
            var id = "#{{coin.symbol}}USDT";
            var price = $(id).html();
            sum += {{balances}}['{{coin.symbol}}'] * price;
            $("#{{coin.symbol}}_balance").html({{balances}}['{{coin.symbol}}']+" {{coin.symbol}}");
        }
        else{
            $("#{{coin.symbol}}_balance").html("0 {{coin.symbol}}");
        }
    {% endfor %}
    sum += {{usdt}};
    $("#sum").html(sum.toFixed(2) +" USD");
}



