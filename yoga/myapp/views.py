from django.shortcuts import render
from .models import Image


from django import forms

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image',)



def getAngles(img):
    pose = "pose"
    return pose


# Create your views here.
def home(request):
    context = {}
    context['form'] = ImageForm()
    if request.method=="POST":
        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            form.save()
            img_obj = form.instance
            
            ##### write the image loading pose here

            pose = getAngles(img_obj)

            #####
            return render(request, 'home.html', {'form': form, 'img_obj': img_obj, "pose":pose})

    return render(request, 'home.html', context)
