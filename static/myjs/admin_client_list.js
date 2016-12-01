$(document).ready(function () {
    $('#currencyselect').empty();
    $('#currencyselect').append('<option disabled selected value="Загрузка...">Загрузка...</option>');
    $.get('/bill/getcurrency/', function (data) {
        currid = data['currency'];
        currname = data['currencyname'];
        $('#currencyselect').empty();
        for (i in currid)
            $('#currencyselect').append('<option selected value=' + currid[i] + '>' + currname[i] + '</option>');
    })
});
$('#myModalChangeUser').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $(this).find('#contentname').text(button.data('contentname'));
    $(this).find('#userfirstname').val(button.data('first'));
    $(this).find('#userlastname').val(button.data('last'));
    $(this).find('#userfathername').val(button.data('father'));
    $(this).find('#userid').val(button.data('contentid'));
    $('#changeuserForm').find("input[type=submit]").prop("disabled", false)
});
$('#myModalNewBill').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $(this).find('#contentname').text(button.data('contentname'));
    $(this).find('#userid').val(button.data('contentid'));
    $('#addbillForm').find("input[type=submit]").prop("disabled", false)
});
$('#myModalMessage').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $(this).find('#contentname').text(button.data('contentname'));
    $(this).find('#userid').val(button.data('contentid'));
    $('#messageForm').find("input[type=submit]").prop("disabled", false)
});
$('#myModalFill').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $('#fillerrors').text('');
    $('#addonbillForm').find("input[type=submit]").prop("disabled", false);
    $(this).find('#contentname').text(button.data('contentname'));
    $('#billfillselecttocard').empty();
    $('#billfillselecttocard').append('<option disabled selected value="Загрузка...">Загрузка...</option>');
    $.get('/bill/getuserbills/', {'num': Number(button.data('contentid'))}, function (data) {
        bills = data['bills'];
        $('#billfillselecttocard').empty();
        for (i in bills)
            $('#billfillselecttocard').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + '</option>')
    });
});
$('#myModalNewCard').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    $('#addcarderrors').text('');
    $('#addcardForm').find("input[type=submit]").prop("disabled", false);
    $(this).find('#contentname').text(button.data('contentname'));
    $('#billselecttocard').empty();
    $('#billselecttocard').append('<option disabled selected value="Загрузка...">Загрузка...</option>');
    $.get('/bill/getuserbills/', {'num': Number(button.data('contentid'))}, function (data) {
        bills = data['bills'];
        $('#billselecttocard').empty();
        for (i in bills)
            $('#billselecttocard').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + '</option>')
    });
});

//==================================================================


$('#myModalChangeUser').submit(function (event) {
    event.preventDefault();
    $('#changeuserForm').find("input[type=submit]").prop("disabled", true);
    $.post('/employee/edituser/', $('#changeuserForm').serializeArray(), function (data) {
        if (data['succes'] == false)
            $('#changeuserForm').find("input[type=submit]").prop("disabled", false);
        else {
            $('#myModalChangeUser').modal('hide');
            fullname = '#client_' + data['id'];
            $(fullname).text(data['newfull']);
            partname = '#client_name_' + data['id'];
            $(partname).data("first", data["newfirst"]);
            $(partname).data("last", data["newlast"]);
            $(partname).data("father", data["newfather"]);
            $('#lastoperation').text(data['operation']).fadeIn(1);
            setTimeout(function () {
                $('#lastoperation').fadeOut(300)
            }, 3000);
            $('#changeuserForm')[0].reset();
        }
    });
});
$('#myModalFill').submit(function (event) {
    event.preventDefault();
    $('#addonbillForm').find("input[type=submit]").prop("disabled", true);
    $.post('/bill/addonbill/', $('#addonbillForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#fillerrors').text(data['errors']);
            $('#addonbillForm').find("input[type=submit]").prop("disabled", false)
        }
        else {
            $('#myModalFill').modal('hide');
            $('#fillerrors').text('');
            $('#lastoperation').text(data['operation']);
            $('#lastoperation').text(data['operation']).fadeIn(1);
            setTimeout(function () {
                $('#lastoperation').fadeOut(300)
            }, 3000);
            $('#addonbillForm')[0].reset();

        }
    });
});
$('#myModalNewBill').submit(function (event) {
    event.preventDefault();
    $('#addbillForm').find("input[type=submit]").prop("disabled", true);
    $.post('/bill/addbill/', $('#addbillForm').serializeArray(), function (data) {
        if (data['succes'] == false)
            $('#addbillForm').find("input[type=submit]").prop("disabled", false);
        else {
            $('#myModalNewBill').modal('hide');
            $('#lastoperation').text(data['operation']).fadeIn(1);
            setTimeout(function () {
                $('#lastoperation').fadeOut(300)
            }, 3000)
        }
        $('#addbillForm')[0].reset();

    });
});
$('#myModalNewCard').submit(function (event) {
    event.preventDefault();
    $('#addcardForm').find("input[type=submit]").prop("disabled", true);
    $.post('/bill/addcard/', $('#addcardForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#addcarderrors').text(data['errors']);
            $('#addcardForm').find("input[type=submit]").prop("disabled", false)
        }
        else {
            $('#myModalNewCard').modal('hide');
            $('#addcarderrors').text('');
            $('#lastoperation').text(data['operation']).fadeIn(1);
            setTimeout(function () {
                $('#lastoperation').fadeOut(300)
            }, 3000)
        }
        $('#addcardForm')[0].reset();

    });
});
$('#myModalMessage').submit(function (event) {
    event.preventDefault();
    $('#messageForm').find("input[type=submit]").prop("disabled", true);
    $.post('/message/send/', $('#messageForm').serializeArray(), function (data) {
        if (data['succes'] == false)
            $('#messageForm').find("input[type=submit]").prop("disabled", false);
        else {
            $('#myModalMessage').modal('hide');
            $('#lastoperation').text(data['operation']).fadeIn(1);
            setTimeout(function () {
                $('#lastoperation').fadeOut(300)
            }, 3000)
        }
        $('#messageForm')[0].reset();
    });
});
