$(document).ready(function () {
    $('#msg').bind('click', function () {
        $.get('/message/updatemsg/', function (data) {
            if (data['data'] == true)
                $("#newmsg").text(data['count']);
            else
                $("#newmsg").text("")

        });
    });

});
