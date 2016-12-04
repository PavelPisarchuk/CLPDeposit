$(document).ready(function () {
    getcurrencies()
});

function getcurrencies() {
    $('#currencyselect').empty();
    $.get('/bill/getcurrency/', function (data) {
        currid = data['currency'];
        currname = data['currencyname'];
        $('#currencyselect').empty();
        $('#currencyselect2').empty();
        for (i in currid) {
            $('#currencyselect').append('<option selected value=' + currid[i] + '>' + currname[i] + '</option>');
            $('#currencyselect2').append('<option selected value=' + currid[i] + '>' + currname[i] + '</option>');
        }
    })
}

$('#myModalNewBill').on('show.bs.modal', function (event) {
    $('#myModalNewBill').find('#errors').text('');
    var button = $(event.relatedTarget);
    $(this).find('#contentname').text(button.data('contentname'));
    $(this).find('#userid').val(button.data('contentid'));
    $('#addbillForm').find("input[type=submit]").prop("disabled", false)
});
$('#myModalMessage').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $('#myModalMessage').find('#errors').text('');
    $(this).find('#contentname').text(button.data('contentname'));
    $(this).find('#userid').val(button.data('contentid'));
    $('#messageForm').find("input[type=submit]").prop("disabled", false)
});
$('#myModalFill').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $('#myModalFill').find('#errors').text('');
    $('#addonbillForm').find("input[type=submit]").prop("disabled", false);
    $(this).find('#contentname').text(button.data('contentname'));
    $('#billfillselecttocard').empty();
    $.get('/bill/getuserbills/', {'num': Number(button.data('contentid'))}, function (data) {
        bills = data['bills'];
        for (i in bills)
            $('#billfillselecttocard').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + '</option>')
    });
});

//==================================================================

$('#myModalFill').submit(function (event) {
    event.preventDefault();
    $('#addonbillForm').find("input[type=submit]").prop("disabled", true);
    $.post('/bill/addonbill/', $('#addonbillForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#myModalFill').find('#errors').text(data['errors']);
            $('#addonbillForm').find("input[type=submit]").prop("disabled", false)
        }
        else {
            $('#myModalFill').modal('hide');
            disolve(data);
            $('#addonbillForm')[0].reset();
        }
    });
});
$('#myModalNewBill').submit(function (event) {
    event.preventDefault();
    $('#addbillForm').find("input[type=submit]").prop("disabled", true);
    $.post('/bill/addbill/', $('#addbillForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#addbillForm').find("input[type=submit]").prop("disabled", false);
            $('#myModalNewBill').find('#errors').text(data['errors']);
        }
        else {
            $('#myModalNewBill').modal('hide');
            disolve(data);
            $('#addbillForm')[0].reset();
        }
    });
});
$('#myModalMessage').submit(function (event) {
    event.preventDefault();
    $('#messageForm').find("input[type=submit]").prop("disabled", true);
    $.post('/message/send/', $('#messageForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#messageForm').find("input[type=submit]").prop("disabled", false);
            $('#myModalMessage').find('#errors').text(data['errors']);
        }
        else {
            $('#myModalMessage').modal('hide');
            disolve(data);
            $('#messageForm')[0].reset();

        }
    });
});

$(function () {
    $("#search_full").keyup(function () {
        var search_full = $("#search_full").val();
        $.post('/client/search/', {
            'full': search_full
        }, function (data) {
            $('#searchresult').html(data)
        });
        return false;
    });
});


function disolve(data) {
    $('#lastoperation').text(data['operation']).fadeIn(1);
    setTimeout(function () {
        $('#lastoperation').fadeOut(300)
    }, 3000)
}