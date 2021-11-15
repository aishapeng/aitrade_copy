var candleSeries;
var chart;

window.onload = function(){
    get_pnl_chart();
    get_candlestick_chart(); //initialize candlestick chart
    updateKline('{{symbol}}'); //set candlestick data
    resize();
}

// lightweight charts for candlestick chart
function get_candlestick_chart(){
    var chartId = document.getElementById("chart");
    var width = $("#chart").width() - $("#sidebar").width();
    chart = LightweightCharts.createChart(chartId, {
        width: width,
        height: 375,
        layout: {
            backgroundColor: '#fff',//'#f8f9fa',
            textColor: 'rgba(0, 0, 0, 0.9)',
        },
        grid: {
            vertLines: {
                color: 'rgba(197, 203, 206, 0.5)',
            },
            horzLines: {
                color: 'rgba(197, 203, 206, 0.5)',
            },
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
            borderColor: 'rgba(197, 203, 206, 0.8)',
        },
        timeScale: {
            borderColor: 'rgba(197, 203, 206, 0.8)',
            secondsVisible: true,
            fixLeftEdge: true,
        },
        localization: {
                 timeFormatter: businessDayOrTimestamp => {
                     return timeConverter(businessDayOrTimestamp); //or whatever JS formatting you want here
                 },
            },
    });

    candleSeries = chart.addCandlestickSeries({
      upColor: '#4bffb5',
      downColor: '#ff4976',
      borderDownColor: '#ff4976',
      borderUpColor: '#4bffb5',
      wickDownColor: '#838ca1',
      wickUpColor: '#838ca1',
    });
    var data = JSON.parse('{{kline}}');
    candleSeries.setData(data);
}

function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min =  "0" + a.getMinutes();
  var sec =  "0" + a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
  return time;
}

function updateKline(symbol='BTC') {
    var stream = "wss://stream.binance.com:9443/ws/" + symbol.toLowerCase() + "usdt@kline_1h";
    var ws = new WebSocket(stream);

    ws.onmessage = function(e){
        var data = JSON.parse(e.data);
          var candlestick = data.k;
          candleSeries.update({
            time: candlestick.t/1000,
            open: candlestick.o,
            high: candlestick.h,
            low: candlestick.l,
            close: candlestick.c
          });
    }

    ws.onclose = function(){
        // connection closed, discard old websocket and create a new one in 5s
        ws = null
        setTimeout(updateKline(symbol), 5000)
    }
}


// asset doughnut chart
function get_asset_chart(){
    var ctx = document.getElementById("assetChart");
    var assetValue = {}
    {% for coin in coin_list %}
        if ( '{{coin.symbol}}' in {{balances}} ){
            var id = "#{{coin.symbol}}USDT";
            var price = $(id).html();

            assetValue['{{coin.symbol}}'] = parseFloat({{balances}}['{{coin.symbol}}']) * parseFloat(price);
        }
    {% endfor %}
    assetValue['USDT'] = {{usdt}}
    // data
    var assetData = {
      labels: Object.keys(assetValue),
      datasets: [
        {
          data: Object.values(assetValue),
          backgroundColor: ["#ffb319", "#64c9cf", "#d2bfbf", "#ffc6c6", "#96a9ff", "#d4aa86", "#749cc1", "#f2efea", "#2b2926", "#ff4f4f"]
        }
      ]
    };
    //options
    var options = {
        responsive: true,
        title: {
          display: true,
          position: "top",
          text: "Asset Allocation (USD)",
          fontSize: 15,
          fontColor: "#111"
        },
        legend: {
          display: true,
          position: "bottom",
          labels: {
            fontColor: "#333",
            fontSize: 12
          }
        }
    };
    // initialise chart
    var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: assetData,
      options: options
    });
}

// pnl line chart
function get_pnl_chart(){
    var ctx = document.getElementById("pnlChart");
    // data
    var pnlData = {
      labels: Object.keys({{pnl_all}}),
      datasets: [
        {
          label: '',
          data: Object.values({{pnl_all}}),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }
      ]
    };
    // initialise chart
    var myChart = new Chart(ctx, {
      type: 'line',
      data: pnlData,
      options: {
        responsive:true,
        legend: {display: false}
        }
    });
}

setTimeout(function(){
    get_asset_chart();
}, 2500);



