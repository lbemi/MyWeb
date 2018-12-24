def getuserip(request):
    ip = request.META['REMOTE_ADDR']
    if ip == '127.0.0.1':
        return {'user_type':'本机用户'}
    return {'user_type':'外部用户(%s)'%ip}