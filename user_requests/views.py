from django.shortcuts import render, get_object_or_404
from user_requests.models import Request


def requests_list(request):
    # select_related для связей user и found_artist
    requests_qs = Request.objects.select_related(
        'user', 'found_artist').all().order_by('-created_at')
    return render(request, "user_requests/list.html", {"requests": requests_qs})


def request_detail(request, request_id: int):
    req = get_object_or_404(Request.objects.select_related(
        'user', 'found_artist'), pk=request_id)
    return render(request, "user_requests/detail.html", {"req": req})
