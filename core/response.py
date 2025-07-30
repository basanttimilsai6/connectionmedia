from rest_framework.response import Response



class MyResponse:
    @staticmethod
    def success(data={},message="",status_code=200):
        response_data = {
            "success":True,
            "data":data,
            "message":message
        }

        return Response(data=response_data,status=status_code)
    
    @staticmethod
    def failure(data={},message="",status_code=400):
        response_data = {
                "success":False,
                "data":data,
                "message":message
            }
        return Response(
            data=response_data,
            status=status_code
        )