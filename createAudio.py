import pyttsx3              # for converting text to speech
import pygame               # for playing audio files

import os.path as path



# initializing audio libraries
pygame.mixer.init()
engine = pyttsx3.init()

# basic audio settings
voices = engine.getProperty('voices') # available voices
engine.setProperty('voice', voices[1].id) # change the voice
engine.setProperty('rate', 150) # Decrease the Speed Rate x2


audiosLoc = "audioFiles/"



def createAudio(textList, audioPath):
    fullText = " ".join(textList)
    # audioPath = (audiosLoc+audioName+".wav")
    if not path.exists(audioPath):
        engine.save_to_file(fullText, audioPath)
        engine.runAndWait()
        print("created")
    else:
        print(audioPath, "exists")



basePerform = "You have performed"



poseList = [("Warrior Pose 1", "warrior1"),
            ("Warrior Pose 2", "warrior2"),
            ("Mountain Pose", "mountain"),
            ("Goddess Pose", "goddess"),
            ("Downward dog Pose", "downdog"),

            ]


# for pose,naming in poseList:
#     createAudio([basePerform, pose], naming)

secText = "seconds completed"

for i in range(15,181,15):
    createAudio([str(i),secText], f"{audiosLoc}{str(i)}sec.wav")




# python createAudio.py
# 