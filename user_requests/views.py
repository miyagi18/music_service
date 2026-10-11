from django.http import HttpResponse


def requests_list(request):
    return HttpResponse("Список заявок")


def request_detail(request, request_id):
    return HttpResponse(f"Заявка {request_id}")