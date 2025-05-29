from django.http import JsonResponse
from django.db import transaction
from rest_framework.views import APIView
from .models import Payment, Organization, BalanceLog
from .serializers import PaymentSerializer

class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({"error": "Invalid data"}, status=400)

        data = serializer.validated_data
        operation_id = data["operation_id"]

        if Payment.objects.filter(operation_id=operation_id).exists():
            return JsonResponse({"message": "Duplicate operation"}, status=200)

        with transaction.atomic():
            organization, _ = Organization.objects.get_or_create(inn=data["payer_inn"], defaults={"balance": 0})
            payment = Payment.objects.create(
                operation_id=operation_id,
                amount=data["amount"],
                payer_inn=data["payer_inn"],
                document_number=data["document_number"],
                document_date=data["document_date"]
            )
            previous_balance = organization.balance
            organization.balance += data["amount"]
            organization.save()

            BalanceLog.objects.create(
                organization=organization,
                previous_balance=previous_balance,
                new_balance=organization.balance,
                payment=payment
            )
            print(BalanceLog.objects.filter(payment=payment).get())
        return JsonResponse({"message": "Payment processed successfully"}, status=200)


class BalanceView(APIView):
    def get(self, request, inn, *args, **kwargs):
        try:
            organization = Organization.objects.get(inn=inn)
            return JsonResponse({"inn": inn, "balance": str(organization.balance)}, status=200)
        except Organization.DoesNotExist:
            return JsonResponse({"error": "Organization not found"}, status=404)
