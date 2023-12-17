from rest_framework import serializers
from .models import Customer, Loan  # Import your relevant models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer  # Set the model to be serialized
        fields = '__all__'  # Use '__all__' to include all fields, or specify fields explicitly

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan  # Set the model to be serialized
        fields = '__all__'  # Use '__all__' to include all fields, or specify fields explicitly
