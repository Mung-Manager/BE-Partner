from time import process_time_ns


class APIProcessTimeMiddleware:
    """
    이 클래스는 API의 프로세스 시간을 계산하는 미들웨어입니다.
    response에 "Api-Process-Run-Time" 헤더를 추가하며 초 단위로 표시합니다.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the api (and later middleware) are called.
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        # Code to be executed for each request/response after
        # the api is called.
        return response

    def process_request(self, request):
        self.api_process_start_time = process_time_ns()

    def process_response(self, request, response):
        response["Api-Process-Run-Time"] = (process_time_ns() - self.api_process_start_time) / 1e9
