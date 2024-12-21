from django.shortcuts import render


# This is the view for the home page
def home(request):
    return render(request, "home.html")
