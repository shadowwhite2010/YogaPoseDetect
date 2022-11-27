from django.shortcuts import render
from .models import Image
import numpy as np
import pickle
import cv2
from mediapipe.python.solutions import pose as mp_pose
import os
from django import forms
classifier = pickle.load(open('D:\projects\YogaPoseDetect\yoga\yoga_model\save_model3', 'rb'))

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image',)



def getAngles(item, pt1, pt2, pt3):
    a = item[pt1]
    b = item[pt2]
    c = item[pt3]
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = (np.arccos(cosine_angle))*(180/np.pi)
    return angle

def yoga_predict(img_name):
    img = cv2.imread('D:/projects/YogaPoseDetect/yoga/media/images/'+img_name)
    # img = np.array(img)
    # print(img[0])
    # img = img[:, :, ::-1].copy() 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    with mp_pose.Pose(upper_body_only=False) as pose_tracker:
        result = pose_tracker.process(image=img)
        pose_landmarks = result.pose_landmarks
    if pose_landmarks is not None:
        assert len(pose_landmarks.landmark) == 33, 'Unexpected number of predicted pose landmarks: {}'.format(len(pose_landmarks.landmark))
        pose_landmarks = [[lmk.x, lmk.y, lmk.z] for lmk in pose_landmarks.landmark]
        frame_height, frame_width = img.shape[:2]
        pose_landmarks *= np.array([frame_width, frame_height, frame_width])
        item = pose_landmarks
        arr = np.array([getAngles(item, 13, 11, 12),
          getAngles(item, 24, 12, 14),
          getAngles(item, 15, 13, 11),
          getAngles(item, 12, 14, 16),
          getAngles(item, 11, 23, 25),
          getAngles(item, 12, 24, 26),
          getAngles(item, 23, 25, 27),
          getAngles(item, 24, 26, 28)])
        res = classifier.predict([arr])
        return res[0]
    else:
        return "no"

# Create your views here.
def home(request):
    context = {}
    context['form'] = ImageForm()
    if request.method=="POST":
        form = ImageForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            img_obj = request.FILES['image']
            # if img_obj.name not in os.listdir('D:\projects\YogaPoseDetect\yoga\media\images'):
            form.save()
            img_objj = form.instance
            ##### write the image loading pose here
            print(type(img_obj.name), img_obj.name)
            pose = yoga_predict(img_obj.name)
            pose = pose.capitalize()
            #####
            return render(request, 'home.html', {'form': form, 'img_obj': img_objj, "pose":pose})

    return render(request, 'home.html', context)
