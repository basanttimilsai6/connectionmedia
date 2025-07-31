from core.response import MyResponse


class NotificationServices:
    @staticmethod
    def get_notifications(request,Model):
        try:
            notifications = (
                    Model.objects
                    .filter(user=request.user)
                    .only('id', 'message', 'is_read', 'created_at')  # Optimized field fetching
                    .order_by('-created_at')
                )
            return notifications
        except Exception as e:
            return MyResponse.failure(message="Failed to retrieve notifications.", status_code=500)
        

    @staticmethod
    def filter_notifications(request,Model):
        try:
            return Model.objects.filter(user=request.user)
        except Exception as e:
            return MyResponse.failure(message="Failed to retrieve notifications.", status_code=500)
        