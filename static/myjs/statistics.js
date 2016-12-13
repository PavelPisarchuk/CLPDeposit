$.get('/employee/stats/', function (responce) {
    if (responce.deposit_popularity) {
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
            "#73afeb",
            "#99e785",
            "#FFCE56",
            "#FF6384",
            "#dfa9d9",
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

        new Chart($('#bad_popularity'), {
            type: 'bar',
            data: {
                labels: responce.bad_popularity.labels,
                datasets: [{
                    label: "Количество вкладов",
                    data: responce.bad_popularity.data,
                    backgroundColor: backgroundColor
                }]
            },
            options: options
        });

        $('#loader').css('display', 'none');
        $('#content').css('opacity', '100');
    }
    else {
        $('#loader')[0].innerHTML = 'Нет данных о вкладах'
    }

});