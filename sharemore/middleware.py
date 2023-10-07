# # middleware.py

# from threading import local

# _user = local()

import threading
request_cfg = threading.local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        request_cfg.user = request.user
        print(request_cfg.user, type(request_cfg.user), request_cfg.user.username)
        response = self.get_response(request)
        print(response)
        return response
        
    @classmethod
    def get_user(cls, request):
        request_cfg.user = request.user
        return request_cfg.user
    
        # _user.value = request.user
        # response = self.get_response(request)
        # return response
        
    # @classmethod
    # def get_user(cls):
    #     return _user.value


        # response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.



        return response