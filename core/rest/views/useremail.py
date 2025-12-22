from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.tasks import send_email_task
from core.rest.serializers.useremail import ContactFormSerializer
from core.throttling import SingleAPIViewThrottle


class ContactFormAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [SingleAPIViewThrottle]

    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data["name"]
            email = serializer.validated_data["email"]
            subject = serializer.validated_data["subject"]
            message = serializer.validated_data["message"]
            phone = serializer.validated_data.get("phone", "")
            context = {"name": name, "email": email, "message": message, "phone": phone}
            try:
                send_email_task.delay(
                    subject=f"Contact Form: {subject}",
                    recipient="osmangoni255@gmail.com",
                    template_name="emails/contact_form.html",
                    context=context,
                )

                return Response(
                    {
                        "success": True,
                        "message": "Your message has been sent successfully. We will get back to you soon.",
                    },
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "message": "Failed to send email. Please try again later.",
                        "error": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "success": False,
                "message": "Invalid data provided.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
