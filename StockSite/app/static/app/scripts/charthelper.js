var red = 'rgba(255,99,132,1)'
var green = 'rgba(33,206,153,1)'
var chartTicker = ''
var chart2Ticker = ''
var chart3Ticker = ''

function updateAllCharts(tickers, chartIDs) {
    if (tickers.length == chartIDs.length) 
    {
        for (var i = 0; i < tickers.length; i++)
        {
            getChart(tickers[i], chartIDs[i]);
        }
    }
}

function updateCurrentDashboardCharts() {
    getChart(chartTicker, 'chart');
    getChart(chart2Ticker, 'chart2');
    getChart(chart3Ticker, 'chart3');
}

function getChart(ticker, chartID) {
    $('#' + chartID).replaceWith('<canvas id="' + chartID + '"></canvas>');
    setCurrentChartTickers(ticker, chartID);
    var chart = document.getElementById(chartID);
    getDailyHistoricData(ticker).then((chartData) => {
        var lineColor = red;
        if (chartData['positiveChange'])
        {
            lineColor = green;
        }
        var myChart = new Chart(chart, {
            type: 'line',
            data: {
                labels: chartData['xaxis'],
                datasets: [{
                    label: ticker,
                    data: chartData['yaxis'],
                    borderColor: [
                        lineColor,
                    ],
                    borderWidth: 1,
                    pointRadius: 0,
                    fill: false,
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                },
                tooltipTemplate: "<%if (label){%><%=label%>: <%}%>$<%= value %>"
            }
        });
    });
}

function setCurrentChartTickers(ticker, chartID) {
    if (chartID == 'chart') {
        chartTicker = ticker;
    }
    else if (chartID == 'chart2') {
        chart2Ticker = ticker;
    }
    else if (chartID == 'chart3') {
        chart3Ticker = ticker;
    }
}