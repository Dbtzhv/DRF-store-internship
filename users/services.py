from rest_framework import status
from rest_framework.response import Response


def update_password(user, request):
    user.object = user.get_object()
    serializer = user.get_serializer(data=request.data)

    if serializer.is_valid():
        # Check old password
        if not user.object.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        user.object.set_password(serializer.data.get("new_password"))
        user.object.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        return Response(response)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
