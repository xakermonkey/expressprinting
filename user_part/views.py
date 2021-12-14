from django.shortcuts import render


def userForm(request):
    return render(request, 'user_form.html')