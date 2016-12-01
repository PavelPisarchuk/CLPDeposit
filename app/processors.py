from app.models import now


def unread_messages(request):
    try:
        count = request.user.get_unread_messages_count()
    except:
        count = 0
    return {
        'unread_messages_count': count
    }


def date(request):
    return {
        'today': now()
    }
