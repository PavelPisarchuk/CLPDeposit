import datetime


def unread_messages(request):
    return {
        'unread_messages_count': request.user.get_unread_messages_count()
    }


def date(request):
    request.user
    return {
        'today': datetime.datetime.now()
    }
