// Función para generar colores aleatorios
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Función para generar una lista de colores
function generateColorList(length) {
    const colors = [];
    for (let i = 0; i < length; i++) {
        colors.push(getRandomColor());
    }
    return colors;
}


document.addEventListener('DOMContentLoaded', function() {
    // Total Chart
    const totalCtx = document.getElementById('totalChart').getContext('2d');
    const totalLabels = chart_data.labels
    const totalData = chart_data.totals
    const totalChart = new Chart(totalCtx, {
        type: 'line',
        data: {
            labels: totalLabels,
            datasets: [{
                label: 'Total',
                data: totalData,
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });


    // Ventas Totales por Mes Chart
    const ventasTotalesCtx = document.getElementById('ventasTotalesChart').getContext('2d');
    const ventasTotalesLabels = monthly_sales.labels;
    console.log(ventasTotalesLabels)
    const ventasTotalesData = monthly_sales.totals;
    console.log(ventasTotalesData)
    let backgroundColors = generateColorList(ventasTotalesData.length);

    const ventasTotalesChart = new Chart(ventasTotalesCtx, {
        type: 'doughnut',
        data: {
            labels: ventasTotalesLabels,
            datasets: [{
                label: 'Ventas Totales por Mes',
                data: ventasTotalesData,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });


    // Ventas Totales de los clientes
    const ventasTotalesClientesCtx = document.getElementById('ventasTotalesClientes').getContext('2d');
    const ventasTotalesClientesLabels = customer_sales_data.customers;
    console.log(ventasTotalesClientesLabels)
    const ventasTotalesClientesData = customer_sales_data.sales_counts;
    console.log(ventasTotalesClientesData)
    backgroundColors = generateColorList(ventasTotalesClientesData.length);
    const ventasTotalesClientesChart = new Chart(ventasTotalesClientesCtx, {
        type: 'bar',
        data: {
            labels: ventasTotalesClientesLabels,
            datasets: [{
                label: 'Ventas por Cliente',
                data: ventasTotalesClientesData,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });


    // Ventas por Hora del Día Chart
    const ventasPorHoraCtx = document.getElementById('ventasPorHoraChart').getContext('2d');
    const ventasPorHoraLabels = sales_by_hour_data.labels;
    const ventasPorHoraData = sales_by_hour_data.totals;

    const ventasPorHoraChart = new Chart(ventasPorHoraCtx, {
        type: 'bar',  // Cambia a 'line' para un gráfico de línea
        data: {
            labels: ventasPorHoraLabels,
            datasets: [{
                label: 'Ventas por Hora del Día',
                data: ventasPorHoraData,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });


    const productosMasVendidosCtx = document.getElementById('productosMasVendidosChart').getContext('2d');
    const productosMasVendidosLabels = product_sales_data.products;
    const productosMasVendidosData = product_sales_data.quantities;

    console.log(productosMasVendidosLabels);
    console.log(productosMasVendidosData);

    backgroundColors = generateColorList(productosMasVendidosData.length);

    const productosMasVendidosChart = new Chart(productosMasVendidosCtx, {
        type: 'bar',
        data: {
            labels: productosMasVendidosLabels,
            datasets: [{
                label: 'Cantidad Vendida',
                data: productosMasVendidosData,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});