from django.shortcuts import render, get_object_or_404
from labels.models import Label


def labels(request):
    labels_list = Label.objects.all().order_by('name')
    return render(request, "labels/list.html", {"labels": labels_list})


def label_detail(request, label_id: int):
    label = get_object_or_404(Label, pk=label_id)
    # prefetch_related оптимизирует получение обратной связи (артистов)
    artists = label.artists.all().order_by('name')
    return render(request, "labels/detail.html", {"label": label, "artists": artists})
