from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from account.models import Profile
from .models import Attendance

import cv2
import numpy as np
import face_recognition
import os
import datetime
import timeago

User = get_user_model()

def verify(request):
    
    path = f'media/profile_images'

    images = []

    class_names = []
    
    name = ''

    my_list = os.listdir(path)

    print(my_list)

    for cls in my_list:
        current_image = cv2.imread(f'{path}/{cls}')
        images.append(current_image)
        class_names.append(cls.rsplit('.', 4)[0])
    # print(images)
    print(class_names)

    def find_encodings(images):
        encode_list = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        return encode_list

    def get_current_user(name=None):
        if name == None:
            attend_status_fail = True
            sys_status = 'Attendance not Captured. Try Again!!'
            context = {'attend_status_fail':attend_status_fail,'sys_status':sys_status,}
            return context
           
        else:
            attend_status_success = True
            sys_status = 'Attendance Captured.'
            user_profile = User.objects.filter(username=f'{name.lower()}')
            for user in user_profile:
                first_name = user.first_name
                last_name = user.last_name
                status = user.profile.status
                attendance_time = user.profile.attendance_time
                lateness = user.profile.lateness_ago
            
            context = {
                    'attend_status_success':attend_status_success,
                    'sys_status':sys_status,
                    'first_name':first_name,
                    'last_name':last_name,
                    'status':status,
                    'attendance_time':attendance_time,
                    'lateness':lateness,
                    }
        return context   
     
    def add_attendance(user_id, fullname, email, designation, status, late=False, lateness=None):
        attendance = Attendance.objects.create(
                        user_id = user_id,
                        fullname = fullname,
                        email = email,
                        designation = designation,
                        status = status,
                        late = late,
                        lateness = lateness,
                       
                    )
        attendance.save()
        print("Attendance recorded!!!")
        
    def mark_attendance(name):
         
        print(f'\n Taking Attendance for {name} !!')   
       
        current_date_and_time = datetime.datetime.now()
        print('Now          :', current_date_and_time)
        added_time = datetime.timedelta(minutes=1)
        new_time_line = current_date_and_time + added_time
        print ('New Time     :', new_time_line)
        
         # get current user details before marking attendance
        user_profile = User.objects.filter(username=f'{name.lower()}')
        for user in user_profile:
            user_id = user.id
            fullname = user.last_name + " " + user.first_name
            email = user.email
            designation = user.designation.title
            lateness_benchmark_time = datetime.datetime.strptime(user.designation.lateness_benchmark, '%H:%M:%S').time()
            lateness_benchmark =  datetime.datetime.combine(datetime.datetime.now(), lateness_benchmark_time)
            # status = user.profile.status
            # attendance_time = user.profile.attendance_time
            ban_time = user.profile.ban_time
            
            
        my_profile = Profile.objects.filter(username=f'{name.lower()}')
        for p in my_profile:
            status = p.status
            ban_time = p.ban_time
        
        if status == 'Signed Out': 
            if ban_time == None or current_date_and_time > ban_time:
              
                print()
               
                if current_date_and_time > lateness_benchmark:
                    
                    late = True
                    lateness_ago = timeago.format(lateness_benchmark, current_date_and_time)
                    late_duration = lateness_ago.rsplit(' ', 3)[0]
                    late_duration_2 = lateness_ago.rsplit(' ', 3)[1]
                    lateness = late_duration + ' ' + late_duration_2
                    print(f"You are late ooo..You passed you lateness benchmark  {lateness_ago}.")
                    
                    my_profile.update(status='Signed In', ban_time=new_time_line, attendance_time=current_date_and_time, lateness_ago=lateness_ago)
                    add_attendance(user_id, fullname, email, designation, "Signed In", late, lateness)
                
                if current_date_and_time < lateness_benchmark:
                    
                    late = False                    
                    my_profile.update(status='Signed In', ban_time=new_time_line, attendance_time=current_date_and_time, lateness_ago=None)
                    add_attendance(user_id, fullname, email, designation, "Signed In")
                    
        elif status == 'Signed In':
            if current_date_and_time > ban_time:
                my_profile.update(status='Signed Out', ban_time=new_time_line, attendance_time=current_date_and_time, lateness_ago=None)
                add_attendance(user_id, fullname, email, designation, "Signed Out")
         
        # get current user details after marking attendance       
        
              
        print(f'Currently {status} with ban time at {ban_time}')
                        


    encode_list_known = find_encodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, image = cap.read()
        image_small = cv2.resize(image, (0,0), None, 0.25, 0.265)
        image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)
        
        faces_in_current_frame = face_recognition.face_locations(image_small)
        encodings_of_current_frame = face_recognition.face_encodings(image_small, faces_in_current_frame)
        
        for encode_face, face_loc in zip(encodings_of_current_frame, faces_in_current_frame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face, tolerance=0.49)
            face_dist = face_recognition.face_distance(encode_list_known, encode_face)
            print(face_dist)
            match_index = np.argmin(face_dist)
            
            if matches[match_index]:
                name = class_names[match_index].upper()
                time = datetime.datetime.now()
                print(name)
                details = name + " - " + str(time)
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0),2)
                cv2.rectangle(image, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
                cv2.putText(image, details, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                
                mark_attendance(name)
                
            elif not matches[match_index]:
                name = "Unknown"
                # print(name)    
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(image, (x1,y1), (x2,y2), (0,0,255),2)
                cv2.rectangle(image, (x1,y2-35), (x2,y2), (0,0,255), cv2.FILLED)
                cv2.putText(image, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                
        cv2.imshow('Attendance Cam', image)
        key = cv2.waitKey(1)
        if key == 13:
            break
        
        
        # Release handle to the webcam
    cap.release()
    cv2.destroyAllWindows()
    if name == 'Unknown' or name =='':
        context = get_current_user()
    else:
        context = get_current_user(name.lower())
    return render(request, 'index.html', context)