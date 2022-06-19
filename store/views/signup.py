from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        var = request.POST
        first_name = var.get('firstname')
        last_name = var.get('lastname')
        phone = var.get('phoneno')
        email = var.get('email')
        password = var.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
        }

        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

        error_message = self.validateCustomer(customer)

        if (not error_message):
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = 'First name required'
        elif len(customer.first_name) < 3:
            error_message = "Minimum 3 characters"
        elif (not customer.last_name):
            error_message = 'Last name required'
        elif len(customer.last_name) < 3:
            error_message = "Minimum 3 characters"
        elif (not customer.phone):
            error_message = 'Phone required'
        elif len(customer.phone) < 10:
            error_message = "Phone must be 10 characters long"
        elif (not customer.email):
            error_message = 'Email required'
        elif (not customer.password):
            error_message = 'Password required'
        elif len(customer.password) < 8:
            error_message = "Password must be 8 characters long"
        elif customer.isExists():
            error_message = 'Email already registered'

        return error_message
