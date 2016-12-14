$(document).ready(function () {

    $('#myModalReadMessage').on('show.bs.modal', function (event) {
        $('#deletemessagelForm').find("input[type=submit]").prop("disabled", false);
        var button = $(event.relatedTarget);
        messagetag = '#read_message_' + button.data('messageid');
        $('#messageinMessage')[0].innerHTML = button.data('message');
        $('#headerinMessage')[0].innerHTML = button.data('header');
        $(this).find('#messageid').val(button.data('messageid'));
        $.post('/message/readmsg/', {'message_id': button.data('messageid')}, function (data) {
            $(messagetag).detach();
        });
    });

    $('#myModalReadMessage').submit(function (event) {
        event.preventDefault();
        $('#deletemessagelForm').find("input[type=submit]").prop("disabled", true);
        $.post('/message/delete/', $('#deletemessagelForm').serializeArray(), function (data) {
            if (data['succes'] == false) {
                $('#messageForm').find("input[type=submit]").prop("disabled", false);
            }
            else {
                $('#myModalReadMessage').modal('hide');
                messagetag = '#message_' + data['msgid'];
                $(messagetag).detach();
                $('#myModalMessage').modal('hide');
                $('#deletemessagelForm')[0].reset();
            }
        });
    });

    $(document).foundation();
    jQuery(function ($) {
    });

});
