//Needs separation of concerns work
function updateStockInfo(stocks) {
    let price_diffs = "{ ";
    let length = stocks.length;

    getCurrentPrices(stocks).then((current_prices) => {
        for (i = 0; i < length; i++) {
            price_diffs = price_diffs + ("\"" + stocks[i]["symbol"] + "\": { " + calculateDifferences(Number(current_prices[i]['last_trade_price']), Number(stocks[i]["day_open_price"]), Number(stocks[i]["week_open_price"]), Number(stocks[i]["month_open_price"])));
            if (i < length - 1) {
                price_diffs = price_diffs + ", ";
            }
        }
        price_diffs = price_diffs + " }";
        json_object = JSON.parse(price_diffs);
        updateTableInfo(json_object);
    });

    tickers = [];
    charts = ['chart', 'chart2', 'chart3']
    if (length >= 3) {
        if (chartTicker != '') {
            updateCurrentDashboardCharts();
            return;
        } else {
            tickers = [stocks[0]['symbol'], stocks[1]['symbol'], stocks[2]['symbol']];
        }
    }
    else if (length == 2) {
        tickers = [stocks[0]['symbol'], stocks[1]['symbol'], 'NFLX'];
    }
    else if (length == 1) {
        tickers = [stocks[0]['symbol'], 'AAPL', 'NFLX'];
    }
    else {
        tickers = ['GOOGL', 'AAPL', 'NFLX'];
    }
    updateAllCharts(tickers, charts);
}

function updateTableInfo(updatedInfo) {
    for (info in updatedInfo) {
        rows = document.getElementsByName(info);
        if (rows.length == 1) {
            columns = rows[0].getElementsByTagName('td');
            columns[2].textContent = updatedInfo[info]['current'];
            columns[3].textContent = updatedInfo[info]['dayDiff'];
            columns[4].textContent = updatedInfo[info]['weekDiff'];
            columns[5].textContent = updatedInfo[info]['monthDiff'];
        }
    }
}

function getCurrentPrices(stocks) {
    let length = stocks.length;
    promises = [];
    for (var i = 0; i < length; i++) {
        if (stocks[i]["quotes_link"]) {
            let quotes_link = stocks[i]["quotes_link"]
            console.log(quotes_link);
            let pricePromise = fetch(quotes_link).then((response) => response.json());
            promises.push(pricePromise);
        }
    }
    return Promise.all(promises);
}

function getDailyHistoricData(ticker) {
    return fetchDailyHistoricData(ticker).then((data) => {
        xaxis = [];
        yaxis = [];
        startPrice = 0.0;
        endPrice = 0.0;
        positiveChange = false;
        for (record in data['historicals'])
        {
            if (record == 0)
            {
                startPrice = data['historicals'][record]['open_price'];
            }
            else if (record == data['historicals'].length - 1)
            {
                endPrice = data['historicals'][record]['open_price'];
            }
            xaxis.push(parseISOStringTime(data['historicals'][record]['begins_at'].split('T')[1]));
            yaxis.push(data['historicals'][record]['open_price']);
        }
        if (Number(startPrice) < Number(endPrice))
        {
            positiveChange = true;
        }
        return { xaxis, yaxis, positiveChange };
    })
}

function updateStockFundamentals(ticker) {
    fetchStockFundamentals(ticker).then((data) => {
        document.getElementById('volume').textContent = "Volume: " + stringifyBigNumber(Number(data['volume']));
        document.getElementById('PE').textContent = "P/E Ratio: " + round(Number(data['pe_ratio']), 3);
        document.getElementById('52High').textContent = "52 Week High: $" + round(Number(data['high_52_weeks']), 2);
        document.getElementById('52Low').textContent = "52 Week Low: $" + round(Number(data['low_52_weeks']), 2);
    })
}

function updateStockPrice(ticker) {
    fetchStockPrice(ticker).then((data) => {
        document.getElementById('stock_price').textContent = round(Number(data['last_trade_price']), 2);
    }) 
}

//Could refactor fetch methods into one method
function fetchStockFundamentals(ticker) {
    url = "https://api.robinhood.com/fundamentals/" + ticker + '/';
    return fetch(url).then(response => response.json());
}

function fetchStockPrice(ticker) {
    url = "https://api.robinhood.com/quotes/" + ticker + '/';
    return fetch(url).then(response => response.json());
}

function fetchDailyHistoricData(ticker) {
    url = "https://api.robinhood.com/quotes/historicals/" + ticker + "/?interval=5minute&span=day&bounds=trading";
    return fetch(url).then((response => response.json()));
}

function calculateDifferences(current, dayOpen, weekOpen, monthOpen)
{
    return " \"current\": \"$" + current + "\", \"dayDiff\": " + round((current - dayOpen), 2) +
        ", \"weekDiff\": " + round((current - weekOpen), 2) +
        ", \"monthDiff\": " + round((current - monthOpen), 2) + " }";
}

function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

function stringifyBigNumber(value) {
    if (value >= 1000000) {
        value = round( (value / 1000000), 3);
        return value + "mil";
    } else if (value >= 10000)
    {
        value = round((value / 1000), 3)
        return value + "k";
    } else
    {
        return value;
    }
}

function parseISOStringTime(s) {
    var b = s.split(':');
    return b[0] + ':' + b[1];
}
