$(document).ready(function () {

    getcurrencies();

    $('#myModalContracts').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        modal_event('', this, event);
        $('#myModalContracts').find('#contracts').empty();
        $.get('/bill/usercontracts/', {'billid': Number(button.data('billid'))}, function (data) {
            $('#myModalContracts').find('#contracts').html(data)
        });
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
        event.preventDefault();
        $('#transactForm').find("input[type=submit]").prop("disabled", true);
        $.post('/bill/billtransact/', $('#transactForm').serializeArray(), function (data) {
            if (data['succes'] == false) {
                $('#myModalTransact').find('#errors').text(data['errors']);
                $('#transactForm').find("input[type=submit]").prop("disabled", false)
            }
            else {
                newsummato = '#summa_' + data['to'][0];
                newsummafrom = '#summa_' + data['from'][0];
                $(newsummafrom).text(data['from'][1]);
                $(newsummato).text(data['to'][1]);
                $('#myModalTransact').modal('hide');
                disolve(data);
                $('#transactForm')[0].reset();
            }
        });

        //postman('#transactForm', '#myModalTransact', '/bill/billtransact/', event)
    });


});