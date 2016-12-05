$(document).ready(function () {
    getcurrencies();

    $('#myModalNewBill').on('show.bs.modal', function (event) {
        modal_event('#addbillForm', this, event)
    });
    $('#myModalMessage').on('show.bs.modal', function (event) {
        modal_event('#messageForm', this, event)
    });
    $('#myModalFill').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        modal_event('#addonbillForm', this, event);
        $('#billfillselecttocard').empty();
        $.get('/bill/getuserbills/', {'num': Number(button.data('contentid'))}, function (data) {
            bills = data['bills'];
            for (i in bills)
                $('#billfillselecttocard').append('<option selected value=' + bills[i] + '>Счёт номер ' + bills[i] + '</option>')
        });
    });

    //==================================================================

    $('#myModalFill').submit(function (event) {
        postman('#addonbillForm', '#myModalFill', '/bill/addonbill/', event)
    });

    $('#myModalNewBill').submit(function (event) {
        postman('#addbillForm', '#myModalNewBill', '/bill/addbill/', event)
    });
    $('#myModalMessage').submit(function (event) {
        postman('#messageForm', '#myModalMessage', '/message/send/', event)
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

    $(document).foundation();
    jQuery(function ($) {
    });
});