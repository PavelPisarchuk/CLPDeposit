$('#myModalOperations').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $(this).find('#messageinMessage').text(button.data('message'));
    $(this).find('#headerinMessage').val(button.data('header'));
    $(this).find('#messageid').val(button.data('messageid'));
    $.post('/actions/contract/', {'num': button.data('contractid')}, function (data) {
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

$('#myModalFill').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $('#myModalFill').find('#errors').text('');
    $('#clientfillForm').find("input[type=submit]").prop("disabled", false);
    $(this).find('#contractid').val(button.data('contractid'))
});

$('#clientfillForm').submit(function (event) {
    event.preventDefault();
    $('#clientfillForm').find("input[type=submit]").prop("disabled", true);
    $.post('/contract/addmoney/', $('#clientfillForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#errors').text(data['errors']);
            $('#clientfillForm').find("input[type=submit]").prop("disabled", false)
        }
        else {
            $('#myModalFill').modal('hide');
            disolve(data);
            $('#clientfillForm')[0].reset();
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
