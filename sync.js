import { createChart, CrosshairMode } from 'lightweight-charts';

export const createChartWithSeries = (container, lineData, candlestickData, color, buySellMarkers) => {
    const chart = createChart(container, {
        timeScale: {
            borderColor: 'rgba(197, 203, 206, 1)',
        },
        rightPriceScale: {
            autoScale: true,
            scaleMargins: {
                top: 0.1,
                bottom: 0.1,
            },
        },
        crosshair: {
            mode: CrosshairMode.Normal,
        },
    });

    const lineSeries = chart.addLineSeries({
        priceFormat: {
            precision: 8,
        },
        color: color,
    });

    lineSeries.setData(lineData);

    const candlestickSeries = chart.addCandlestickSeries({
        upColor: 'rgba(255, 144, 0, 1)',
        downColor: '#000',
        borderDownColor: 'rgba(255, 144, 0, 1)',
        borderUpColor: 'rgba(255, 164, 0, 1)',
        wickDownColor: 'rgba(255, 144, 0, 1)',
        wickUpColor: 'rgba(255, 144, 0, 1)',
    });

    candlestickSeries.setData(candlestickData);

    if (buySellMarkers) {
        candlestickSeries.setMarkers(buySellMarkers);
    }

    return {
        chart,
        lineSeries,
        candlestickSeries
    };
};

const synchronizeCharts = (charts) => {
    const onVisibleTimeRangeChanged = (targetChart, otherCharts) => {
        return (newVisibleRange) => {
            otherCharts.forEach(chart => {
                if (chart) {
                    chart.timeScale().setVisibleRange(newVisibleRange);
                }
            });
        };
    };

    const onCrosshairMove = (targetChart, otherCharts) => {
        return (param) => {
            otherCharts.forEach(chart => {
                if (chart) {
                    chart.setCrosshairPosition(param);
                }
            });
        };
    };

    charts.forEach((chart, index, arr) => {
        const otherCharts = arr.filter((_, i) => i !== index);

        if (chart) {
            chart.timeScale().subscribeVisibleTimeRangeChange(onVisibleTimeRangeChanged(chart, otherCharts));
            chart.subscribeCrosshairMove(onCrosshairMove(chart, otherCharts));
        }
    });
};

export { synchronizeCharts };

const updateChartsWithNewData = (charts, newData) => {
    charts.forEach((chartData) => {
        const { chart, lineSeries, candlestickSeries } = chartData;
        
        if (newData.lineData) {
            lineSeries.setData(newData.lineData);
        }

        if (newData.candlestickData) {
            candlestickSeries.setData(newData.candlestickData);
        }
        
        if (newData.buySellMarkers) {
            candlestickSeries.setMarkers(newData.buySellMarkers);
        }
    });
};

// Example usage

// Initialize charts
const chart1Data = createChartWithSeries(document.getElementById('chart1'), initialLineData1, initialCandlestickData1, 'blue', initialBuySellMarkers1);
const chart2Data = createChartWithSeries(document.getElementById('chart2'), initialLineData2, initialCandlestickData2, 'green', initialBuySellMarkers2);

// Synchronize charts
synchronizeCharts([chart1Data.chart, chart2Data.chart]);

// Update charts dynamically
const fetchDataAndUpdateCharts = () => {
    // Fetch new data (replace this with your actual data fetching logic)
    const newData = fetchNewData();

    // Update charts with new data
    updateChartsWithNewData([chart1Data, chart2Data], newData);
};

// Fetch and update every minute
setInterval(fetchDataAndUpdateCharts, 60000);