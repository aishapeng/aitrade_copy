// check if coin pairs are traded
{% if request.user.trade_btc %}
    $('#indicateBTC').html("ACTIVE");
    $('#indicateBTC').addClass("text-primary").removeClass("text-muted");
    $('#tradeBTC').prop( "checked", true );
{% endif %}
{% if request.user.trade_eth %}
    $('#indicateETH').html("ACTIVE");
    $('#indicateETH').addClass("text-primary").removeClass("text-muted");
    $('#tradeETH').prop( "checked", true );
{% endif %}
{% if request.user.trade_xrp %}
    $('#indicateXRP').html("ACTIVE");
    $('#indicateXRP').addClass("text-primary").removeClass("text-muted");
    $('#tradeXRP').prop( "checked", true );
{% endif %}
{% if request.user.trade_ltc %}
    $('#indicateLTC').html("ACTIVE");
    $('#indicateLTC').addClass("text-primary").removeClass("text-muted");
    $('#tradeLTC').prop( "checked", true );
{% endif %}
{% if request.user.trade_bch %}
    $('#indicateBCH').html("ACTIVE");
    $('#indicateBCH').addClass("text-primary").removeClass("text-muted");
    $('#tradeBCH').prop( "checked", true );
{% endif %}
{% if request.user.trade_ada %}
    $('#indicateADA').html("ACTIVE");
    $('#indicateADA').addClass("text-primary").removeClass("text-muted");
    $('#tradeADA').prop( "checked", true );
{% endif %}
{% if request.user.trade_bnb %}
    $('#indicateBNB').html("ACTIVE");
    $('#indicateBNB').addClass("text-primary").removeClass("text-muted");
    $('#tradeBNB').prop( "checked", true );
{% endif %}
{% if request.user.trade_link %}
    $('#indicateLINK').html("ACTIVE");
    $('#indicateLINK').addClass("text-primary").removeClass("text-muted");
    $('#tradeLINK').prop( "checked", true );
{% endif %}
{% if request.user.trade_dot %}
    $('#indicateDOT').html("ACTIVE");
    $('#indicateDOT').addClass("text-primary").removeClass("text-muted");
    $('#tradeDOT').prop( "checked", true );
{% endif %}
{% if request.user.trade_xlm %}
    $('#indicateXLM').html("ACTIVE");
    $('#indicateXLM').addClass("text-primary").removeClass("text-muted");
    $('#tradeXLM').prop( "checked", true );
{% endif %}

//checkbox toggle to start/stop trading coin pairs
function startTrade(){
    var balance = parseFloat($('#usdt').html());
    var coinBalance = parseFloat($("#{{symbol}}_balance").html());
    var coinValue = coinBalance *  $("#{{symbol}}USDT").html();
    if( (document.getElementById('trade{{symbol}}').checked) && (balance < 100) &&  (coinValue < 100)){
        alert("To start trading a coin pair, must have at least 100 USDT balance!");
        $('#trade{{symbol}}').prop( "checked", false );
        return;
    }

    if($('#trade{{symbol}}').prop('checked')){
        $('#indicate{{symbol}}').html("ACTIVE");
        $('#indicate{{symbol}}').addClass("text-primary").removeClass("text-muted");
        $.post("{% url 'dashboard' %}",
          {
            "csrfmiddlewaretoken": "{{ csrf_token }}",
            "symbol": "{{symbol}}",
            "trade": "True"
          });
    }else{
        $('#indicate{{symbol}}').html("INACTIVE");
        $('#indicate{{symbol}}').addClass("text-muted").removeClass("text-primary");
        $.post("{% url 'dashboard' %}",
          {
            "csrfmiddlewaretoken": "{{ csrf_token }}",
            "symbol": "{{symbol}}",
            "trade": "False"
          });
    }
}

// Set user pnl
function get_pnl(){
    var current =  parseFloat($("#sum").html());
    var pnl = current - parseFloat({{pnl_last}});
    if (pnl > 0){
        $(".pnl").html("+ $"+pnl.toFixed(2));
        $(".pnl").addClass("text-success");
    } else{
        $(".pnl").html("- $"+(pnl.toFixed(2))*-1);
        $(".pnl").addClass("text-danger");
    }
}
// Wait 2s for websocket data
setTimeout(get_pnl, 2000);

// Show selected pair order history
function showSelected(){
    if($('#showSelected').prop('checked')){
        $("#historyList li").filter(function() {
          $(this).toggle($(this).children().children(".symbol").text().indexOf('{{symbol}}') > -1);
        });
    }else{
        $("#historyList li").show();
    }
}

// Responsive sidebar and candlestick chart
window.onresize = resize;
function resize() {
  if (window.matchMedia("(max-width: 1000px)").matches) {
        $('#sidebar').removeClass('show');
    } else {
        $('#sidebar').addClass('show');
    }
  var width = $("#chart").width();
  chart.resize(width, 350);
}

var show = false;
function toggleSidebar(){
    console.log(show);
    if (show == true){
        $('#sidebar').collapse('hide');
        show = false;
    } else {
        $('#sidebar').collapse('show');
        show = true;
    }
}

function reformatDate(dateStr)
{
  dArr = dateStr.split("-");  // ex input "2021-01-18"
  return dArr[1]+ "-" +dArr[2]+ "-" +dArr[0]; //ex out: "18-01-2021"
}

$(function() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if (urlParams.has('start')) {
        var startDate = reformatDate(urlParams.get('start'));
        var endDate = reformatDate(urlParams.get('end'));
        $('input[name="daterange"]').daterangepicker({ startDate: startDate, endDate: endDate });
    }
    $('input[name="daterange"]').daterangepicker({
        opens: 'right'
        }, function(start, end, label) {
        $('#order-filter').append('<input type="hidden" name="start" value='+start.format('YYYY-MM-DD')+' />');
        $('#order-filter').append('<input type="hidden" name="end" value='+end.format('YYYY-MM-DD')+' />');
        $("#order-filter").submit();
    });
});


