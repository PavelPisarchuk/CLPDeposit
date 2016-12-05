$(document).ready(function () {

    getcurrencies();

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
            money = data['money'];
            for (i in bills) {
                $('#billtransactelecttocard').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + money[i] + '</option>');
                $('#billtransactelecttocard2').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + money[i] + '</option>')
            }
        });
    });
    $('#myModalOperations').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        $.post('/actions/bill/', {'num': button.data('billid')}, function (data) {
            $('#billoperations').html(data)
        });
    });


    $('#transactForm').submit(function (event) {
        postman('#transactForm', '#myModalTransact', '/bill/billtransact/', event)
    });


});