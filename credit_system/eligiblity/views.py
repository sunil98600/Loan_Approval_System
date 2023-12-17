from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,Loan
from .serializers import CustomerSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
import pandas as pd


class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            monthly_salary = serializer.validated_data['monthly_salary']
            approved_limit = round(36 * monthly_salary, -5)  # Round to the nearest lakh
            serializer.save(approved_limit=approved_limit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class CheckLoanEligibility(APIView):
        # Define a function to calculate credit score
    def calculate_credit_score(customer_id):
        # Read loan data from the Excel file
        loan_data = pd.read_excel('loan_data.xlsx')

        # Filter loan data for the specific customer_id
        customer_loans = loan_data[loan_data['customer id'] == customer_id]

        # Criteria for credit score calculation
        loans_paid_on_time = sum(customer_loans['EMIs paid on time'])
        num_loans_taken = len(customer_loans)
        current_year_loans = customer_loans[customer_loans['start date'].dt.year == pd.Timestamp.now().year]
        loan_approved_volume = sum(customer_loans['loan amount'])
    
        # Sum of current loans of the customer
        sum_current_loans = sum(customer_loans['loan amount'])
    
        # Fetch customer's approved limit
        customer_approved_limit = 360000 * Customer.monthly_salary # Assuming the approved limit calculation

        # Calculate credit score based on criteria
        if sum_current_loans > Customer.approved_limit:
            credit_score = 0
        else:
        # Your credit score calculation logic based on the given criteria
        # Use the calculated variables (loans_paid_on_time, num_loans_taken, current_year_loans, loan_approved_volume)
        # to calculate the credit score
        # Replace this with your actual credit score calculation logic
            credit_score = 70  # Placeholder value for demonstration

        return credit_score
    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        # Convert annual interest rate to monthly and decimal form
        monthly_interest_rate = (interest_rate / 12) / 100

        # Convert tenure from years to months
        tenure_in_months = tenure * 12

        # Calculate monthly installment using EMI formula
        numerator = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure_in_months
        denominator = (1 + monthly_interest_rate) ** tenure_in_months - 1
        monthly_installment = numerator / denominator

        # Round the monthly installment to 2 decimal places
        monthly_installment = round(monthly_installment, 2)

        return monthly_installment


    def post(self, request):
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')
        
        
        # Retrieve customer and their related loan history
        customer = Customer.objects.get(pk=customer_id)
        loans_history = Loan.objects.filter(customer=customer)
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate credit_rating based on the provided criteria
        credit_rating = self.calculate_credit_score(customer, loans_history)
        monthly_installment = self.calculate_monthly_installment(loan_amount, interest_rate, tenure)

        # Check eligibility based on credit_rating
        if credit_rating > 50:
            loan_approved = True
            corrected_interest_rate = interest_rate  # No correction needed
        elif 50 > credit_rating > 30:
            if interest_rate > 12:
                loan_approved = True
                corrected_interest_rate = interest_rate  # No correction needed
            else:
                loan_approved = False
                corrected_interest_rate = 12  # Minimum interest rate for this range
        elif 30 > credit_rating > 10:
            if interest_rate > 16:
                loan_approved = True
                corrected_interest_rate = interest_rate  # No correction needed
            else:
                loan_approved = False
                corrected_interest_rate = 16  # Minimum interest rate for this range
        else:
            loan_approved = False
            corrected_interest_rate = None  # No loans for credit_rating < 10

        # Check if sum of all current EMIs > 50% of monthly salary
        total_emis = sum(loan.monthly_repayment for loan in loans_history)
        if total_emis > 0.5 * customer.monthly_salary:
            loan_approved = False
            corrected_interest_rate = None  # Don't approve any loans if EMIs exceed 50% of salary

        # Perform calculations and checks for loan eligibility
        # Implement your logic here based on the given criteria
        
        # Return response with the calculated interest rate and eligibility decision
        response_data = {
            'customer_id': customer_id,
            'approval': True,  # Decision based on your logic
            'interest_rate': interest_rate,  # Calculate or adjust interest rate based on criteria
            'corrected_interest_rate': corrected_interest_rate ,  # Corrected rate based on criteria
            'tenure': tenure,
            'monthly_installment':monthly_installment,  # Calculated installment based on rates
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    

class CreateLoan(APIView):
    def create_loan(request):
      if request.method == 'POST':
        # Assuming the request body is in JSON format
        data = request.POST  # Use request.POST or request.body depending on your request data
        
        # Retrieving data from the request body
        customer_id = data.get('customer_id')
        loan_amount = data.get('loan_amount')
        interest_rate = data.get('interest_rate')
        tenure = data.get('tenure')
        
        # Check customer eligibility (you can define your own logic here)
        customer = get_object_or_404(Customer, id=customer_id)
        is_eligible = customer.CheckLoanEligibility(loan_amount, interest_rate, tenure)
        
        if is_eligible:
            # If eligible, create the loan
            new_loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                tenure=tenure
                # Add other fields as needed
            )
            
            response_body = {
                'loan_id': new_loan.id,
                'customer_id': customer_id,
                'loan_approved': True,
                'message': 'Loan approved!',
                'monthly_installment': new_loan.installment
                # Add other response fields as needed
            }
        else:
            response_body = {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': 'Loan not approved. Customer is not eligible for the requested loan.'
                # You can customize the message based on eligibility criteria
            }
        
        return JsonResponse(response_body)
      else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
    
    

   


class ViewLoanDetails(APIView):
    @api_view(['GET'])
    def view_loan(request, loan_id):
      try:
        loan = Loan.objects.get(id=loan_id)
        customer = Loan.customer
        customer_data = CustomerSerializer(customer).data
        loan_data = {
            'loan_id': loan_id,
            'customer': customer_data,
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.monthly_repayment,
            'tenure': loan.tenure,
        }
        return Response(loan_data)
      except Loan.DoesNotExist:
        return Response({'error': 'Loan does not exist'}, status=404)

    @api_view(['GET'])
    def view_loans_by_customer(request, customer_id):
      try:
        loans = Loan.objects.filter(customer_id=customer_id)
        loan_data = []
        for loan in loans:
            loan_info = {
                'loan_id': loan.id,
                'loan_amount': loan.loan_approved,
                'interest_rate': loan.interest_rate,
                'monthly_installment': loan.monthly_installment,
                'repayments_left': loan.repayments_left,
            }
            loan_data.append(loan_info)
        return Response(loan_data)
      except Customer.DoesNotExist:
        return Response({'error': 'Customer does not exist'}, status=404)

