$(document).ready(function () {

    $('#myModalRate').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        $.get('/rate/history/', {
            'pk1': button.data('pk1'),
            'pk2': button.data('pk2')
        }, function (responce) {
            console.log(responce);
            $("#chartContainer").CanvasJSChart({
                height: 200,
                axisY: {
                    title: responce.title,
                    includeZero: false
                },
                axisX: {
                    labelFontSize: 10,
                    labelAutoFit: true,
                    interval: 2
                },
                data: [{
                    type: 'stepLine',
                    toolTipContent: "{x}/{y}",
                    dataPoints: responce.dataPoints
                }]
            });
            $(".canvasjs-chart-canvas")[0].style.width = '100%';
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
