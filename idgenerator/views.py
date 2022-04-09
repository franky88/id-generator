from django.shortcuts import redirect, render, get_object_or_404
from .models import IdInfo
from django.contrib import messages
import qrcode
import qrcode.image.svg
from io import BytesIO
# from rest_framework import viewsets
# from .serializers import IdInfoSerializer
# from rest_framework import permissions
from .forms import IdInfoForm
from django.contrib.auth.decorators import login_required
# Create your views here.


# class IdInfoViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = IdInfo.objects.all().order_by('-created')
#     serializer_class = IdInfoSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@login_required()
def home(request):
    qcb_ids = IdInfo.objects.all().order_by('-created', '-updated')

    context = {
        'title': 'id generator',
        'ids': qcb_ids,
    }
    return render(request, 'home.html', context)


@login_required()
def add_id(request):
    form = IdInfoForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('idgen:home')
    else:
        form = IdInfoForm()
    context = {
        'title': 'add id',
        'form': form
    }
    return render(request, 'add_id.html', context)


@login_required()
def update_id(request, pk):
    instance = get_object_or_404(IdInfo, pk=pk)
    print(instance.first_name)
    form = IdInfoForm(request.POST or None,
                      request.FILES or None, instance=instance)
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make("https://www.facebook.com/qcbcorp",
                      image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('idgen:details', pk=instance.pk)
    context = {
        'title': 'id details',
        'form': form,
        'instance': instance,
        'svg': stream.getvalue().decode()
    }
    return render(request, 'id_details.html', context)


@login_required()
def delete(request, pk):
    instance = get_object_or_404(IdInfo, pk=pk)
    if request.method == "POST":
        instance.delete()
        messages.add_message(request, messages.SUCCESS,
                             'ID successfully deleted.')
        return redirect('idgen:home')
    context = {
        'title': 'delete',
        'instance': instance
    }
    return render(request, 'delete.html', context)


def view_id(request, pk):
    instance = get_object_or_404(IdInfo, pk=pk)
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make("https://www.facebook.com/qcbcorp",
                      image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    context = {
        'title': 'id preview',
        'instance': instance,
        'svg': stream.getvalue().decode()
    }
    return render(request, 'view_id.html', context)
