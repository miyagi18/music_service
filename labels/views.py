from django.http import HttpResponse


def labels(request):
    return HttpResponse("Список лейблов")


def label_detail(request, label_id):
    return HttpResponse(f"Лейбл {label_id}")
