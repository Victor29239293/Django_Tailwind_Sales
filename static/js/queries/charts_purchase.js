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
    let backgroundColors
    
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


    // Compras Totales por Mes Chart
    const comprasTotalesCtx = document.getElementById('comprasTotalesChart').getContext('2d');
    const comprasTotalesLabels = monthly_purchases.labels;
    console.log(comprasTotalesLabels)
    const comprasTotalesData = monthly_purchases.totals;
    console.log(comprasTotalesData)
    backgroundColors = generateColorList(comprasTotalesData.length);

    const comprasTotalesChart = new Chart(comprasTotalesCtx, {
        type: 'polarArea',
        data: {
            labels: comprasTotalesLabels,
            datasets: [{
                label: 'Compras Totales por Mes',
                data: comprasTotalesData,
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


    // compras Totales de los suppliers
    const comprasTotalesSuppliersCtx = document.getElementById('comprasTotalesProveedores').getContext('2d');
    const comprasTotalesSuppliersLabels = supplier_purchases_data.suppliers;
    const comprasTotalesSuppliersData = supplier_purchases_data.purchases_counts;
    
    // Verifica los valores que se están usando en el gráfico
    console.log(comprasTotalesSuppliersLabels);
    console.log(comprasTotalesSuppliersData);

    backgroundColors = generateColorList(comprasTotalesSuppliersData.length);

    const comprasTotalesSuppliersChart = new Chart(comprasTotalesSuppliersCtx, {
        type: 'line',
        data: {
            labels: comprasTotalesSuppliersLabels,
            datasets: [{
                label: 'Compras a proveedores',
                data: comprasTotalesSuppliersData,
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

    const productosMasCompradosCtx = document.getElementById('productosMasCompradosChart').getContext('2d');
    const productosMasCompradosLabels = product_purchases_data.products;
    const productosMasCompradosData = product_purchases_data.quantities;
    
    // Verifica los valores que se están usando en el gráfico
    console.log(productosMasCompradosLabels);
    console.log(productosMasCompradosData);

    backgroundColors = generateColorList(productosMasCompradosData.length);

    const productosMasCompradosChart = new Chart(productosMasCompradosCtx, {
        type: 'bar',
        data: {
            labels: productosMasCompradosLabels,
            datasets: [{
                label: 'Cantidad Comprada',
                data: productosMasCompradosData,
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