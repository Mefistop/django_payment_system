from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    payer_inn = serializers.CharField(max_length=12)
    document_number = serializers.CharField(max_length=50)
    document_date = serializers.DateTimeField()

    def validate_payer_inn(self, value):
        if len(value) != 10 and len(value) != 12:
            raise serializers.ValidationError("Invalid INN format")
        return value