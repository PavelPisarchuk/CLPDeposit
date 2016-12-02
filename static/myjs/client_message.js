$('#myModalReadMessage').on('show.bs.modal', function (event) {
    $('#deletemessagelForm').find("input[type=submit]").prop("disabled", false);
    var button = $(event.relatedTarget);
    messagetag = '#message_' + button.data('messageid');
    $(this).find('#messageinMessage').text(button.data('message'));
    $(this).find('#headerinMessage').val(button.data('header'));
    $(this).find('#messageid').val(button.data('messageid'));
    $.post('/message/readmsg/', {'num': button.data('messageid')}, function (data) {
        $(messagetag).css({"font-weight": "normal"})
    });
});

$('#myModalReadMessage').submit(function (event) {
    event.preventDefault();
    $('#deletemessagelForm').find("input[type=submit]").prop("disabled", true);
    $.post('/message/delete/', $('#deletemessagelForm').serializeArray(), function (data) {
        if (data['succes'] == false) {
            $('#messageForm').find("input[type=submit]").prop("disabled", false);
            //$('#myModalMessage').find('#errors').text(data['errors']);
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