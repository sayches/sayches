from django.shortcuts import render


def handler404(request, exception):
    return render(request, '404.html', locals())
