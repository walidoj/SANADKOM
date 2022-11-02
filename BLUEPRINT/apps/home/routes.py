# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from apps.authentication.models import pics,request_loader
from flask import render_template, request,Flask
from flask_login import login_required,current_user
from jinja2 import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy
from apps import db, login_manager
from flask_socketio import SocketIO
from flask_socketio import SocketIO, emit

import logging
from sys import stdout
from camera2 import VideoCamera
from flask import request,redirect
from flask import Flask, render_template, request,url_for
import copy
from flask import Flask, render_template, Response, request, jsonify
from camera2 import VideoCamera
import Funcs as f
from flask import current_app
from .. import socketio
imagelist={"static/images/image1.png","static/images/image2.png"}

original_questions = {
 #Format is 'question':[options]
 'Relating to People':['No evidence of difficulty or abnormality in relating to people.','Mildly abnormal relationships.','Moderately abnormal relationships.','Severely abnormal relationships.'],
 'imitation':['Appropriate imitation','mildly abnormal imitation','moderately abnormal imitation','severely abnormal imitation'],
 'Emotional Response':['Age-appropriate and situation-appropriate emotional response','mildly abnormal emotional response','moderately abnormal emotional response','severely abnormal emotional response'],
 'body use':['age appropriate body use','mildly abnormal body use','moderately abnormal body use','severely abnormal body use'],
 'object use':['Appropriate interest in,or use of toys and other objects','Mildly inappropriate interest in,or use of toys and other objects','Moderately interest in,or use of toys and other objects','Severely interest in,or use of toys and other objects'],
 'Adaption to change':['Age-appropriate adaption to change','Mildly abnormal adaption to change','Moderately abnormal adaption to change','Severely abnormal adaption to change'],
 'Visual Response':['Age-appropriate visual response','Mildly abnormal visual response','Moderately abnormal visual response','Severely abnormal visual response'],
 'Listening Response':["Age-appropriate listening response","Mildly abnormal listening reponse","Moderetly abnormal listening reponse","severely abnormal listening reponse"]
}
questions = copy.deepcopy(original_questions)
import os
@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>', methods=['GET','POST'])
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        if template=="upload_image.html":
            print("his")
            if request.method=='POST':
                print("his2")

        # Serve the file (if exists) from app/templates/home/
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

t = []
#pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
@blueprint.route('/upload_image.html',methods=['GET'])
@login_required
def helloworld():
    if request.method == 'POST':
        def predict():
            print("hi1")

    return render_template('home/upload_image.html')

print("hi")
@blueprint.route('upload_image.html', methods=['POST'])
@login_required
def predict():
    imagefile1= request.files["imagefile1"]
    imagefile2= request.files["imagefile2"]
    imagefile3= request.files["imagefile3"]
    imagepath=[imagefile1.filename,imagefile2.filename,imagefile3.filename]
    imagepath2=[imagefile1, imagefile2, imagefile3]
    zz=0
    for z in imagepath:
        imagepath2[zz].save(z)


        zz=zz+1
    idd = current_user.id
    picss = pics(id=idd, pic1=imagepath[0],pic2=imagepath[1],pic3=imagepath[2])
    db.session.add(picss)
    db.session.commit()

    res= []
    avg=0
    for y in imagepath:
        z=f.autisticpic(y)
        res.append(f.autisticpic(y))
        if z == "Autistic":
            avg = avg+1
        else:
            avg=avg+0
    avg=avg/3
    print(avg)
    if avg > 1/3:
        res="Autistic"
    else:
        res="Non Autistic"
    segment = get_segment(request)




    #return render_template("home/upload_image.html",prediction=res,Croppedpic="face.jpg", segment=segment)
    return redirect(url_for("home_blueprint.vv"))


@blueprint.route('/quiz1')
def quiz():
 questions_shuffled = questions

 #print(pic1)
 return render_template('home/quiz.html', q = questions_shuffled, o = questions,N=imagelist)


@blueprint.route('/quiz', methods=['POST'])
def quiz_answers():
 correct = 0
 for i in questions.keys():
  answered = request.form[i]
  print(answered)
  if original_questions[i][0] == answered:
   correct = correct+1
  elif original_questions[i][1] == answered:
      correct = correct + 2
  elif original_questions[i][2] == answered:
      correct = correct + 3
  elif original_questions[i][3] == answered:
      correct = correct + 4



 #correct = correct * (t[0]+1)
 if correct > 28:
     r = "Your kid have a high possibility of autisim"
 else:
     r = "Your kid have a low possibility of autisim"
 #return '<h1>Your score is: <u>'+str(correct)+'</u></h1>'+r
 return redirect(url_for("home_blueprint.vv"))



Cam = VideoCamera()

@socketio.on('input image', namespace='/test')
@login_required

def test_message(input):
    input = input.split(",")[1]
    Cam.enqueue_input(input)
    #camera.enqueue_input(base64_to_pil_image(input))





@socketio.on('connect', namespace='/test')
@login_required

def test_connect():
    #app.logger.info("client connected")
    print("hi")


@blueprint.route('/video')
@login_required

def vv():
    #data = Cam.data()
    #print(data)


    """Video streaming home page."""
    return render_template('home/video.html')


def gen(Camera,no):

    while True:
        frame = Camera.get_frame()[no]

        yield (b"--frame\r\n"
            b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

@blueprint.route('/video_feed')
@login_required

def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    frame = gen(Cam,0)

    return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route('/video_feed2')
@login_required

def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    frame = gen(Cam,1)

    return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')