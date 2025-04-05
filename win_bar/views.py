from django.shortcuts import render


# This is the view for the home page
def home(request):
    return render(request, "home.html")


# 404 handler function
def custom_page_not_found(request, exception=None):
    return render(request, "404.html", status=404)
