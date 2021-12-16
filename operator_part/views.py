from django.shortcuts import render


def operatorForm(request):
    return render(request, 'operator_form.html')

def orderDetails(request):
    return render(request, 'order_details.html')