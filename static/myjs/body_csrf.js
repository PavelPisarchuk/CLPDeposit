function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function modal_event(form_id, _this, event) {
    $(_this).find('#errors').text('');
    var button = $(event.relatedTarget);
    $(_this).find('#contentname').text(button.data('contentname'));
    $(_this).find('#userid').val(button.data('contentid'));
    $(form_id).find("input[type=submit]").prop("disabled", false)
}


function postman(form_id, modal_id, url, event) {
    event.preventDefault();
    $(form_id).find("input[type=submit]").prop("disabled", true);
    $.post(url, $(form_id).serializeArray(), function (data) {
        if (data['succes'] == false) {
            $(modal_id).find('#errors').text(data['errors']);
            $(form_id).find("input[type=submit]").prop("disabled", false)
        }
        else {
            $(modal_id).modal('hide');
            disolve(data);
            $(form_id)[0].reset();
        }
    });
}

function disolve(data) {
    $('#lastoperation').text(data['operation']).fadeIn(1);
    setTimeout(function () {
        $('#lastoperation').fadeOut(300)
    }, 3000)
}

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

$(document).ready(function () {

});