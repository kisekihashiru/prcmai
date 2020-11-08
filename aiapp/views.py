from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo


def index(request):
    template = loader.get_template('aiapp/index.html')
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))

def predict(request):
    if not request.method == 'POST':
        return redirect('aiapp:index')

    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('正しく読み込まれませんでした。')

    photo = Photo(image=form.cleaned_data['image'])
    pdata_list, max_pdata = photo.predict()

    template = loader.get_template('aiapp/result.html')

    context = {
        'photo_name': photo.image.name,
        'photo_data': photo.image_src(),
        'predicted': max_pdata[0],
        'percentage': max_pdata[1],
        'class_1_name': pdata_list[0][0],
        'class_1_per': pdata_list[0][1],
        'class_2_name': pdata_list[1][0],
        'class_2_per': pdata_list[1][1],
        'class_3_name': pdata_list[2][0],
        'class_3_per': pdata_list[2][1],
        'class_4_name': pdata_list[3][0],
        'class_4_per': pdata_list[3][1],
        'class_5_name': pdata_list[4][0],
        'class_5_per': pdata_list[4][1],
    }

    return HttpResponse(template.render(context, request))
