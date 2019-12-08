from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .forms import TransformationForm


def unleash_outline(request):
    if request.method == 'POST':
        form = TransformationForm(request.POST, request.FILES)
        if form.is_valid():
            transformation_instance = form.save(commit=False)
            transformation_instance.file = request.FILES['file']
            file_type = transformation_instance.file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type != 'opml':
                return render(request, 'outlines_unleashed/error.html')
            transformation_instance.save()
            return render(request, 'outlines_unleashed/result.html', {'transformation': transformation_instance})
    else:
        form = TransformationForm
        context = {"form": form, }
        return render(request, 'outlines_unleashed/unleash_outline.html', context)


def result(request):
    return render(request, 'outlines_unleashed/result.html')