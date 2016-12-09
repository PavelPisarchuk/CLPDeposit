$(document).ready(function () {
    getcurrencies();

    $('#myModalInfo').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        modal_event('', this, event);
        $('#myModalInfo').find('#userinfo').empty();
        $.get('/client/info/', {'user_id': Number(button.data('contentid'))}, function (data) {
            $('#myModalInfo').find('#userinfo').html(data)
        });
    });
    $('#myModalUserBills').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        modal_event('', this, event);
        $('#myModalUserBills').find('#userinfo').empty();
        $.get('/bill/userbillinfo/', {'user_id': Number(button.data('contentid'))}, function (data) {
            $('#myModalUserBills').find('#userinfo').html(data)
        });
    });

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

    var nextloadlen = 0;
    var startloadlen = 0;
    var currloadlen = 0;
    $.get('/client/getlistlen/', function (data) {
        nextloadlen = Number(data['next_len']);
        startloadlen = Number(data['start_len']);
        currloadlen += startloadlen;
        return false
    });

    $("#search_full").keyup(function (eventObject) {
        var search_full = $("#search_full").val();
        if ((eventObject.which != 13 && search_full != '') || inProgress == true)
            return false;

        currloadlen = startloadlen;
        $.get('/client/partiallistsearch/', {
            'full': search_full, 'loadcount': 0
        }, function (data) {
            $('#searchresult').empty();
            $('#searchresult').append(data)
        });
        return false;
    });

    $('body').on('click', '#getBillActions', function (event) {
        $.post('/actions/bill/', {'num': $(this).data('billid')}, function (data) {
            $('body').find('#_operations').html(data);
            $('body').find("#collapseThree").collapse('show');
        });
    });
    $('body').on('click', '#getContractActions', function (event) {
        $.post('/actions/contract/', {'num': $(this).data('billid')}, function (data) {
            $('body').find('#_operations').html(data);
            $('body').find("#collapseThree").collapse('show');
        });
    });


    $('#data_scroll').scroll(function () {
        if (this.scrollHeight - this.scrollTop < this.clientHeight + (this.scrollTop)) {

            var search_full = $("#search_full").val();
            if (inProgress == true)
                return false;
            if (search_full != '') {
                $.ajax({
                    url: '/client/partiallistsearch/', method: 'GET',
                    data: {'loadcount': currloadlen, 'full': search_full},
                    beforeSend: function () {
                        inProgress = true;
                        $('#loadnextclient').text('Загрузка')
                    }
                }).done(function (data) {
                    $('#searchresult').append(data);
                    currloadlen += nextloadlen;
                    inProgress = false;
                    $('#loadnextclient').text('Загрузть ещё')
                })
            }
            else {
                $.ajax({
                    url: '/client/partiallist/', method: 'GET',
                    data: {'loadcount': currloadlen, 'full': search_full},
                    beforeSend: function () {
                        inProgress = true;
                        $('#loadnextclient').text('Загрузка')
                    }
                }).done(function (data) {
                    $('#searchresult').append(data);
                    currloadlen += nextloadlen;
                    inProgress = false;
                    $('#loadnextclient').text('Загрузть ещё')
                })
            }

        }

    });

    $(document).foundation();
    jQuery(function ($) {
    });
});