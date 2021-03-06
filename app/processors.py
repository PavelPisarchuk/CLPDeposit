# -*- coding: utf-8 -*-

from app.models import now, Setting


def unread_messages(request):
    try:
        count = request.user.get_unread_messages_count()
    except:
        count = 0
    return {
        'unread_messages_count': count
    }


def settings(request):
    return {
        'today': now(),
        'processing': Setting.objects.get_or_create(name='processing')[0].value
    }


def alerts(request):
    try:
        return {
            'alerts': request.user.get_alerts()
        }
    except:
        return {
            'alerts': []
        }


def patterns(request):
    return {
        'alpha_rus': "^[А-ЯЁ][а-яё]*$",
    }
