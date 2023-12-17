import pandas as pd
from django.core.management.base import BaseCommand
from eligiblity.models import Customer, Loan

class Command(BaseCommand):
    help = 'Populate data from Excel files into the database'

    def handle(self, *args, **options):
        customer_file_path = r'C:\Users\sakshi\Downloads\Backend Internship Assignment\customer_data.xlsx'
        loan_file_path = r'C:\Users\sakshi\Downloads\Backend Internship Assignment\loan_data.xlsx'

        # Read customer data from Excel file
        customer_data = pd.read_excel(customer_file_path)

        # Iterate through customer data and create Customer objects
        for index, row in customer_data.iterrows():
            Customer.objects.create(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
                
            )

        # Read loan data from Excel file
        loan_data = pd.read_excel(loan_file_path)

        # Iterate through loan data and create Loan objects
        for index, row in loan_data.iterrows():
            customer_id = row['Customer']
            customer = Customer.objects.get(customer_id=customer_id)
            Loan.objects.create(
                customer=customer,
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_repayment=row['Monthly Repayment'],
                emis_paid_on_time=row['EMIs paid on time'],
                start_date=row['Date of Approval'],
                end_date=row['End Date']
            )

        self.stdout.write(self.style.SUCCESS('Data successfully ingested into the database'))
