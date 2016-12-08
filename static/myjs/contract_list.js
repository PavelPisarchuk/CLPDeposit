$(document).ready(function () {

    $('#myModalClose').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        $(this).find('#contract_id').val(button.data('contractid'));
    });


    $('#myModalOperations').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        $('#billoperations').empty();
        $.post('/actions/contract/', {'num': button.data('contractid')}, function (data) {
            $('#billoperations').html(data)
        });
    });

    $('#myModalFill').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        $('#myModalFill').find('#errors').text('');
        $('#clientfillForm').find("input[type=submit]").prop("disabled", false);
        $(this).find('#contract_id').val(button.data('contractid'));
        $('#clientbills').empty();
        $.get('/bill/getuserbillsfromuser/', function (data) {
            $('#clientfillForm').find("input[type=submit]").prop("disabled", false);
            bills = data['bills'];
            money = data['money'];
            for (i in bills)
                $('#clientbills').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + money[i] + '</option>');
        });
    });

    $('#myModalTake').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        $('#myModalTake').find('#errors').text('');
        $('#clienttakeForm').find("input[type=submit]").prop("disabled", false);
        $(this).find('#contract_id').val(button.data('contractid'));
    });


    //======================================================================

    $('#clientfillForm').submit(function (event) {
        event.preventDefault();
        $('#clientfillForm').find("input[type=submit]").prop("disabled", true);
        $.post('/contract/addmoney/', $('#clientfillForm').serializeArray(), function (data) {
            if (data['succes'] == false) {
                $('#myModalFill').find('#errors').text(data['errors']);
                $('#clientfillForm').find("input[type=submit]").prop("disabled", false)
            }
            else {
                newsumma = '#summa_' + data['id'];
                $(newsumma).text(data['newvalue']);
                $('#myModalFill').modal('hide');
                disolve(data);
                $('#clientfillForm')[0].reset();
            }
        });
    });

    $('#closeForm').submit(function (event) {
        event.preventDefault();
        $('#closeForm').find("input[type=submit]").prop("disabled", true);
        $.post('/contract/close/', $('#closeForm').serializeArray(), function (data) {
            if (data['succes'] == false) {
                $('#myModalClose').find('#errors').text(data['errors']);
                $('#closeForm').find("input[type=submit]").prop("disabled", false)
            }
            else {
                contrcact_id = '#contract_' + data['id'];
                $(contrcact_id).html(data['render']);
                $('#myModalClose').modal('hide');
                disolve(data);
                $('#closeForm')[0].reset();
            }
        });
    });

    $('#clienttakeForm').submit(function (event) {
        event.preventDefault();
        $('#clienttakeForm').find("input[type=submit]").prop("disabled", true);
        $.post('/contract/submoney/', $('#clienttakeForm').serializeArray(), function (data) {
            if (data['succes'] == false) {
                $('#myModalTake').find('#errors').text(data['errors']);
                $('#clienttakeForm').find("input[type=submit]").prop("disabled", false)
            }
            else {
                newsumma = '#summa_' + data['id'];
                $(newsumma).text(data['newvalue']);
                $('#myModalTake').modal('hide');
                disolve(data);
                $('#clienttakeForm')[0].reset();
            }
        });
    });

    function disolve(data) {
        $('#lastoperation').text(data['operation']).fadeIn(1);
        setTimeout(function () {
            $('#lastoperation').fadeOut(300)
        }, 3000)
    }

    $(document).foundation();
    jQuery(function ($) {
    });
});
