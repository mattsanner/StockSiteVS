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
}

//TODO: Fix foreach loop to include correct info for writing
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

function calculateDifferences(current, dayOpen, weekOpen, monthOpen)
{
    return " \"current\": \"$" + current + "\", \"dayDiff\": " + round((current - dayOpen), 2) +
        ", \"weekDiff\": " + round((current - weekOpen), 2) +
        ", \"monthDiff\": " + round((current - monthOpen), 2) + " }";
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

function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}
