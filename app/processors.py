import datetime


def unread_messages(request):
    if request.user.is_authenticated:
        count = request.user.get_unread_messages_count()
    else:
        count = 0
    return {
        'unread_messages_count': count
    }


def date(request):
    request.user
    return {
        'today': datetime.datetime.now()
    }
