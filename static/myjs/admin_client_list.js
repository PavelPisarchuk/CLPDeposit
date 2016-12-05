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

    var inProgress = false;
    var loadcount = 15;

    $("#search_full").keyup(function () {
            var search_full = $("#search_full").val();
        loadcount = 15;
        $.get('/client/partiallistsearch/', {
            'full': search_full, 'loadcount': 0
        }, function (data) {
            $('#searchresult').empty();
            $('#searchresult').append(data)
        });
            return false;
    });


    $('#loadnextclient').click(function () {
        var search_full = $("#search_full").val();
        if (search_full != '') {
            $.ajax({
                url: '/client/partiallistsearch/', method: 'GET',
                data: {'loadcount': loadcount, 'full': search_full},
                beforeSend: function () {
                    inProgress = true;
                }
            }).done(function (data) {
                $('#searchresult').append(data);
                loadcount += 15;
                inProgress = false;
            })
        }
        else {
            $.ajax({
                url: '/client/partiallist/', method: 'GET',
                data: {'loadcount': loadcount, 'full': search_full},
                beforeSend: function () {
                    inProgress = true;
                }
            }).done(function (data) {
                $('#searchresult').append(data);
                loadcount += 15;
                inProgress = false;
            })
        }

    });



    $(document).foundation();
    jQuery(function ($) {
    });
});