$(document).ready(function () {
    $('#currencyselect').empty();
    $.get('/bill/getcurrency/', function (data) {
        currid = data['currency'];
        currname = data['currencyname'];
        for (i in currid)
            $('#currencyselect').append('<option selected value=' + currid[i] + '>' + currname[i] + '</option>');
    })
});
$('#myModalTransact').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $('#errors').text('');
    $('#transactForm')[0].reset();
    $('#billtransactelecttocard').empty();
    $('#billtransactelecttocard2').empty();
    $('#transactForm').find("input[type=submit]").prop("disabled", true);
    $.get('/bill/getuserbillsfromuser/', function (data) {
        $('#transactForm').find("input[type=submit]").prop("disabled", false);
        bills = data['bills'];
        for (i in bills) {
            $('#billtransactelecttocard').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + '</option>');
            $('#billtransactelecttocard2').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + '</option>')
        }
    });
});
$('#myModalOperations').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $(this).find('#messageinMessage').text(button.data('message'));
    $(this).find('#headerinMessage').val(button.data('header'));
    $(this).find('#messageid').val(button.data('messageid'));
    $.post('/actions/bill/', {'num': button.data('billid')}, function (data) {
        operations = data['operations'];
        money = data['money'];
        dates = data['dates'];
        $('#billoperations').empty();
        $('#billoperations').append('<tr><td>Тип операции</td><td>Дата</td><td>Сумма</td></tr>');
        for (i in operations)
            $('#billoperations').append('<tr> <td>' + operations[i] + '</td>' +
                '  <td>' + dates[i] + ' </td>  <td>' + money[i] + '</td> </tr>')
    });
});


$('#transactForm').submit(function (event) {
    event.preventDefault();
    $('#transactForm').find("input[type=submit]").prop("disabled", true);
    $.post('/bill/billtransact/', $('#transactForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#errors').text(data['errors']);
            $('#transactForm').find("input[type=submit]").prop("disabled", false)
        }
        else {
            $('#myModalTransact').modal('hide');
            $('#lastoperation').text(data['operation']).fadeIn(1);
            setTimeout(function () {
                $('#lastoperation').fadeOut(300)
            }, 3000);
            $('#errors').text('');
            $('#transactForm')[0].reset();
        }
    });
});
