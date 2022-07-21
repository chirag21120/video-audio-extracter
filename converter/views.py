from django.shortcuts import render
from .forms import UploadFile
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from moviepy.editor import *

# Create your views here.
def converter(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        email = request.POST['email']
        #given_name = file.name
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            fs.save(file.name,file)
            name = str(file.name)
            print(file.name)
            mp3converter(name)
            email_wala_function('audio.mp3',email)
            os.remove("C:/Users/chirag/vscode/django/video/files/"+name)
            os.remove("C:/Users/chirag/vscode/django/video/files/audio.mp3")
            return render(request, "upload.html", {'filename': file.name})


    return render(request,'upload.html')

def email_wala_function(given_name,given_email):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)#yeh is establishing connetion wiht gmail
    smtp.ehlo()
    smtp.starttls()
    #chalo login kara humnei
    #imp point if u want to send from a specifc id then in that id there must be allow acces to less secure apps wali permission on
    smtp.login('test.email.me61@gmail.com', 'test@password')

        # yahan pei we are building our email
        # filhal kei liy yeh essa hai abhi we i wil shape it accourdig to our need in program  
    def message(subject="Python Notification", text="Thank you", attachment=None):
        msg = MIMEMultipart()
        msg['Subject'] = subject

        msg.attach(MIMEText(text)) 
        if attachment is not None:
          
            # Check whether we have the
            # lists of attachments or not!
            if type(attachment) is not list:
            
              # if it isn't a list, make it one
                attachment = [attachment]  
  
            for one_attachment in attachment:
  
                with open(one_attachment, 'rb') as f:
                
                # Read in the attachment
                # using MIMEApplication
                    file = MIMEApplication(f.read(),name=os.path.basename(one_attachment))
                    file['Content-Disposition'] = f'attachment;\
                    filename="{os.path.basename(one_attachment)}"'
               
                msg.attach(file)
            return msg
    # Call the message function
    msg = message("Text file", "Hi there!",r"C:/Users/chirag/vscode/django/video/files/"+given_name)
    #yahan pei we add the path to the fie we wana send 
    # .format y a+ lkarki we will add the string name 

    # to = ["singhsamarjeet09@gmail.com"]
    #multiple bando ko bhi bhej skatei hai cus we made a list
    # Provide some data to the sendmail function!
    smtp.sendmail(from_addr="test.email.me61@gmail.com",to_addrs=given_email, msg=msg.as_string())
  
     # Finally, don't forget to close the connection
    smtp.quit()

def mp3converter(name):
    mp4_file = r"C:/Users/chirag/vscode/django/video/files/"+name
    mp3_file = r"C:/Users/chirag/vscode/django/video/files/audio.mp3"

    videoclip = VideoFileClip(mp4_file)

    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)

    audioclip.close()
    videoclip.close()


