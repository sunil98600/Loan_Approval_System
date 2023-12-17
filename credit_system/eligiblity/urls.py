from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterCustomer.as_view(),name='RegisterCustomer'),
    path('check-eligibility/', views.CheckLoanEligibility.as_view(),name='CheckLoanEligibility'),
    path('create-loan/', views.CreateLoan.as_view(),name='CreateLoan'),
    path('view-loan/<int:loan_id>/', views.ViewLoanDetails.as_view(),name='ViewLoanDetails'),
]
