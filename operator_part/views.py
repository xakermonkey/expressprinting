from django.shortcuts import render


def operatorForm(request):
    return render(request, 'operator_form.html')