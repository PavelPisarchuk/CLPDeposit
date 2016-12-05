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
            $.get('/client/search/', {
                'full': search_full
            }, function (data) {
                $('#searchresult').html(data)
            });
            return false;
        });


    });

    /*
     var inProgress = false;
     var loadcount=25;
     $(window).scroll(function() {
     if($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !inProgress) {
     var search_full = $("#search_full").val();
     $.ajax({
     url: '/client/partiallist/',method: 'GET',
     data: {'loadcount' : loadcount,'full':search_full},
     beforeSend: function() {inProgress = true;}
     }).done(function(data) {
     loadcount+=25;
     inProgress=false;
     })

     }

     })*/

    $(document).foundation();
    jQuery(function ($) {
    });
});