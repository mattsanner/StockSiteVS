function getUpdatedStockInfo(stocks) {
    let length = stocks.length;
    for (var i = 0; i < length; i++)
    {
        for (element in stocks[i])
        {
            console.log(element + ": " + stocks[i][element]);
        }
    }
}