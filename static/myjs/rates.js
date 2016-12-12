$(document).ready(function () {

    $('#myModalRate').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        $.get('/rate/history/', {
            'pk1': button.data('pk1'),
            'pk2': button.data('pk2')
        }, function (responce) {
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
            };;;;;;;
            $('#target')[0].innerHTML = '<canvas id="chartContainer" width="400" height="200"></canvas>';;;;;;;
            new Chart($('#chartContainer'), {
                type: 'line',
                data: {
                    labels: responce.labels,
                    datasets: [{
                        pointHitRadius: 0,
                        data: responce.data
                    }]
                },
                options: options
            });
            $('#title')[0].innerHTML = responce.title;
        })
    });

    $.get('/rate/api/', function (data) {
        console.log(data);
        console.log(data.cur);
        for (i in data.cur) {
            $('.currency_select').append('<option>' + data.cur[i] + '</option>')
        }
        var money_input = $('#money_input')[0],
            output = $('#res')[0];
        var render = function () {
            var value = money_input.value;
            var res = value * data.rates[$('#from')[0].value][$('#to')[0].value];
            res = res.toFixed(2);
            if (res)
                output.value = res;
            else
                output.value = value;
        };
        $('.currency_select').change(render);
        $('#money_input').on('input', render)
    });

});
