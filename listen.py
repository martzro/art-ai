import speech_recognition as sr
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
import tkinter


def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.configure(background='white')
    # Resize to fit screen
    pilImage = pilImage.resize((w, h), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    root.mainloop()


# Initialize the recognizer
r = sr.Recognizer()


# Query api
def speechToImage(parsed):
    data = {"text": parsed}
    url = "http://172.16.20.139:5000/textToImage"

    response = requests.post(url, data)
    url = "http://172.16.20.139:5000/getImage"
    if response.status_code == 200:
        data = {"id": response.content}
        response = requests.post(url, data)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            # Save image
            fileName = datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".jpg"
            img.save(fileName)
            return fileName, img

        # Loop infinitely for user to


# speak
print("Starting")
while (1):
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            if "hey computer" in MyText:
                print('activated...')
                parsed = MyText.replace('hey computer', '').strip()
                print("generating image: ", parsed)
                fileName, img = speechToImage(parsed)
                print("Image Saved: ", fileName)
                showPIL(img)


    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except:
        continue