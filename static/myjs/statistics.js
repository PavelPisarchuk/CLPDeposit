$.get('/employee/stats/', function (responce) {
    console.log(responce);
    var options = {
        legend: {
            display: false
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };

    var backgroundColor = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)'
    ];

    new Chart($('#deposit_popularity'), {
        type: 'bar',
        data: {
            labels: responce.deposit_popularity.labels,
            datasets: [{
                label: "Количество вкладов",
                data: responce.deposit_popularity.data,
                backgroundColor: backgroundColor
            }]
        },
        options: options
    });

    new Chart($('#currency_popularity'), {
        type: 'bar',
        data: {
            labels: responce.currency_popularity.labels,
            datasets: [{
                label: "Количество вкладов",
                data: responce.currency_popularity.data,
                backgroundColor: backgroundColor
            }]
        },
        options: options
    });

    new Chart($('#amount_popularity'), {
        type: 'bar',
        data: {
            labels: responce.amount_popularity.labels,
            datasets: [{
                label: "Количество вкладов",
                data: responce.amount_popularity.data,
                backgroundColor: backgroundColor
            }]
        },
        options: options
    });

    $('#loader').css('display', 'none');
    $('#content').css('opacity', '100');
});;