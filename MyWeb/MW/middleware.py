from django.http import HttpResponseForbidden

class AaccessRestrictionMiddleware:

    def __init__(self, get_response):
        self.wite_ip = ['127.0.0.1']


    def __call__(self, request):
        ip = request.META['REMOTE_ADDR']
        if ip not in self.wite_ip:
            return HttpResponseForbidden('该IP禁止访问！！')
        response = self.get_response(request)
        return response