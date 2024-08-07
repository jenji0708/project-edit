import cv2
import numpy as np
import face_recognition
import os
#from datetime import datetime
from flask import Flask, flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
import json
import pymongo
from pymongo import MongoClient
from netmiko import ConnectHandler
import re
import datetime
import subprocess
from getmac import get_mac_address as gma

UPLOAD_FOLDER = r'C:\Users\ASUS\Downloads\show3\IMAGE_FILES'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


global capture, P
capture=0
switch=1
P = 0

path_face = r'C:\Users\ASUS\Desktop\templeat\show3\img_register'







def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_file():
    return render_template('home.html')

@app.route('/complete_register_addDevice', methods=['GET','POST'])
def complete_register_addDevice():
    return render_template('complete_register_addDevice.html', who = username_register, who_fname = firstname_addDevice, who_lname = lastname_addDevice )


@app.route('/incomplete_register_duplicate', methods=['GET','POST'])
def incomplete_register_duplicate():
    return render_template('incomplete_register_duplicate.html', who = username_register)


@app.route('/complete_register', methods=['GET','POST'])
def complete_register():
    return render_template('complete_register.html', who = username_register,   who_fname = firstname_newUser , who_lname = lastname_newUser)


@app.route('/incomplete_Clock_userNoDataDB')
def incomplete_Clock_userNoDataDB():
    return render_template('incomplete_Clock_userNoDataDB.html')

@app.route('/incomplete_addDevice_fullNumberDevices')
def incomplete_addDevice_fullNumberDevices():
    return render_template('incomplete_addDevice_fullNumberDevices.html')

@app.route('/incomplete_addDevice_haveAlreadyRegistered')
def incomplete_addDevice_haveAlreadyRegistered():
    return render_template('incomplete_addDevice_haveAlreadyRegistered.html')


@app.route('/incomplete_addDevice_disfoundDatainDB')
def incomplete_addDevice_disfoundDatainDB():
    return render_template('incomplete_addDevice_disfoundDatainDB.html')

@app.route('/incomplete_newUser_deny')
def incomplete_newUser_deny():
    return render_template('incomplete_newUser_deny.html')

@app.route('/incomplete_system_error')
def incomplete_system_error():
    return render_template('incomplete_system_error.html')

@app.route('/incomplete_register_unfound_username')
def incomplete_register_unfound_username():
    return render_template('incomplete_register_unfound_username.html')


@app.route('/incomplete_disconnectWifi_with_username')
def incomplete_disconnectWifi_with_username():
    return render_template('incomplete_disconnectWIFI_username.html')

@app.route('/incomplete_disconnectWIFI')
def incomplete_disconnectWIFI():
    return render_template('incomplete_disconnectWIFI.html')


@app.route('/incomplete_NoMacDB')
def incomplete_NoMacDB():
    return render_template('incomplete_NoMacDB.html')

@app.route('/incomplete_NoMacDB_end')
def incomplete_NoMacDB_end():
    return render_template('incomplete_NoMacDB_end.html')

@app.route('/incomplete_Unknown')
def incomplete_Unknown():
    return render_template('incomplete_Unknown.html')


@app.route('/backHome', methods=['POST'])
def backHome():
    homeBtn = request.form.get('data')
    print('user press next button' + homeBtn)

    if homeBtn == 'home' :
         print('Back to home page')
         result = '1'
         

    return result


@app.route('/clockin', methods=['POST'])
def clockin() :

    nextBtn = request.form.get('data')



    if nextBtn == 'next' :
        print('user press next button' + nextBtn)

        if username :
            print ('name = '+name)
            print ('username = '+username)
            connect_WLC()
            if mac_wlc == 0 :
                print("Disconnected MFU's WiFi")
                status = '1'

            else :
                 verifyMac_wlcOnly()
                 status = status_verify

    
                
    result = status
    return result




@app.route('/clockout', methods=['POST'])
def clockout() :

    nextBtn = request.form.get('data')



    if nextBtn == 'next' :
        print('user press next button' + nextBtn)

        if username == username :
            print ('name = '+name)
            print ('username = '+username)
            connect_WLC()

            if mac_wlc == 0 :
                print("Disconnected MFU's WiFi")
                status = '1'
            


            else :
                 verifyMac()
                 status = status_verify

    
                
    result = status
    return result



@app.route('/home', methods=['POST'])
def home() :
    global Btn
    Btn = request.form.get('data')
    print('user press button = ' + Btn)

    if Btn == 'clock in' :
        result = '1'

    if Btn == 'clock out' :
        result = '2'

    if Btn == 'register' :
        result = '3'


    return result


@app.route('/register_face', methods=['GET','POST'])
def register_face():
    return render_template('register_face.html')

@app.route('/register_inputName', methods=['GET','POST'])
def register_inputName():
    return render_template('register_inputName.html')


@app.route('/verify_username_register', methods=['POST'])
def verify_username_register():
    verifyBtn = request.form.get('data')

    if verifyBtn == 'yes' :
        print('user press next button ' + verifyBtn)
        result = '1'
    
    elif verifyBtn == 'no' :
        print('user press next button ' + verifyBtn)
        result = '0' 
    
    return result


@app.route('/verify_username_addDevice_yes', methods=['POST'])
def verify_username_addDevice_yes():
    verifyBtn = request.form.get('data')

    if verifyBtn == 'yes' :
        print('user press next button ' + verifyBtn)

        addDevice_Function()

        result = result_addDevice2
        print(result)
        
    
        return result
    

@app.route('/addDevice_fromClockPage', methods=['POST'])
def addDevice_fromClockPage():
    verifyBtn = request.form.get('data')

    if verifyBtn == 'yes' :
        print('user press next button ' + verifyBtn)

        addDevice_verify_username()

        result = result_addDevice 
        print(result)
        
    
        return result


@app.route('/verify_username_addDevice_no', methods=['POST'])
def verify_username_addDevice_no():
    verifyBtn = request.form.get('data')
    
    if verifyBtn == 'no' :
        print('user press next button ' + verifyBtn)
        result = '0' 
    
    return result


@app.route('/register_FIndUsername_output_addDevice', methods=['GET','POST'])
def register_FIndUsername_output_addDevice() :
    return render_template('register_FIndUsername_output_addDevice.html', who = username_register)


@app.route('/register_FIndUsername_output', methods=['GET','POST'])
def register_FIndUsername_output() :
    return render_template('register_FIndUsername_output.html', who = username_register)


@app.route('/register_option')
def register_option():
    return render_template('register_option.html')


@app.route('/new_User', methods=['POST'])
def newUser() :

    newUserBtn = request.form.get('data')

    if newUserBtn == 'newUser' :
        verify_newUser()

        result = result_newUser 

            
        return result


@app.route('/complete_clockin', methods=['GET','POST'])
def complete_clockin() :

    return render_template('complete_clockin.html', who = name, who_fname = firstname_user , who_lname = lastname_user)


@app.route('/complete_clockout', methods=['GET','POST'])
def complete_clockout() :

    return render_template('complete_clockout.html', who = name,  who_fname = firstname_user , who_lname = lastname_user)


@app.route('/facescan_in', methods=['GET','POST'])
def facescan_in() :

    return render_template('facescan_in.html')


@app.route('/facescan_out', methods=['GET','POST'])
def facescan_out() :

    return render_template('facescan_out.html')


   
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_face')
def video_feed_face():

    return Response(TakePhoto4(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    global username, name

    IMAGE_FILES = []
    filename = []
    username_img = []
    dir_path = r'D:\WLAN time face recorder syst\Image'
 
    for imagess in os.listdir(dir_path):
        img_path = os.path.join(dir_path, imagess)
        img_path = face_recognition.load_image_file(img_path)  # reading image and append to list
        IMAGE_FILES.append(img_path)
        A = imagess.split(".", 1)[0]
        B = A.split("_")
        filename.append(B[0])
        username_img.append(B[1])

    def encoding_img(IMAGE_FILES):
        encodeList = []
        for img in IMAGE_FILES:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList



    encodeListknown = encoding_img(IMAGE_FILES)
    # print(len('sucesses'))

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgc = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        # converting image to RGB from BGR
        imgc = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        fasescurrent = face_recognition.face_locations(imgc)
        encode_fasescurrent = face_recognition.face_encodings(imgc, fasescurrent)

        # faceloc- one by one it grab one face location from fasescurrent
        # than encodeFace grab encoding from encode_fasescurrent
        # we want them all in same loop so we are using zip
        for encodeFace, faceloc in zip(encode_fasescurrent, fasescurrent):
            matches_face = face_recognition.compare_faces(encodeListknown, encodeFace)
            face_distence = face_recognition.face_distance(encodeListknown, encodeFace)
            # print(face_distence)
            # finding minimum distence index that will return best match
            matchindex = np.argmin(face_distence)

            if matches_face[matchindex]:
                name = filename[matchindex].upper()
                username = username_img[matchindex]
                
                # print(name)
                y1, x2, y2, x1 = faceloc
                # multiply locations by 4 because we above we reduced our webcam input image by 0.25
                # y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 253, 35), 2)
                # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 253, 35), 2, cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                  # taking name for attendence function above
            else :
                    name = 'Unknown'
                    username_unknown = name
                    
                    # print(name)
                    y1, x2, y2, x1 = faceloc
                    # multiply locations by 4 because we above we reduced our webcam input image by 0.25
                    # y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), 2, cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                    
        
        #username = name
        # cv2.imshow("campare", img)
        # cv2.waitKey(0)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27:
            break




def takeAttendence(username):
    time = 1
    Datetime = datetime.datetime.now()
    dateAttendace = Datetime.strftime("%x")
    timeAttendace = Datetime.strftime("%X")
  

    with open('attendence.csv', 'r+') as f:
                mypeople_list = f.readlines()
                nameList = []
                for line in mypeople_list:
                    entry = line.split(',')
                    nameList.append(entry[0])

                if time == 1 :              
                    f.writelines(f'\n{username},{firstname_user},{lastname_user},{Btn},{dateAttendace},{timeAttendace}')
                    print(username+ ' attendance record complete')

            
def takeAttendence_Json(username) :
    time = 1
    Datetime = datetime.datetime.now()
    dateAttendace = Datetime.strftime("%x")
    timeAttendace = Datetime.strftime("%X")

    attendance_dict =	{ 
        "Username": username,
        "Firstname": firstname_user,
        "Lastname": lastname_user,
        "Status": Btn,
        "Date": dateAttendace,
        "Time": timeAttendace,

    }
    print(attendance_dict)

    


    with open("attendance_dict.json", "w") as outfile:
        json.dump(attendance_dict, outfile)
    
    print("Save to Json already.")



def register_Json(username_register) :


    register_dict =	{ 
        "Username": username_register,
        "Firstname" : firstname_newUser,
        "Lastname" : lastname_newUser,
        "Mac Address 1": mac_register,
    }
    print(register_dict)

    


    with open("register_dict.json", "w") as outfile:
        json.dump(register_dict, outfile)
    
    print("Save register to Json already.")


def findMac_database() :
    global mactListDB, result_findMac_database, firstname_user, lastname_user, info_UserListDB

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["nutdb"]
    mycol = mydb["information_user2"]

    find_db = mycol.find_one({"Username": username})
    print("Database connectting")


    print(find_db)


    if (find_db is None) :
        print("The system not found your information.")
        result_findMac_database = '0'
    
    else :
        mactListDB = list(find_db.values())
        mactListDB = mactListDB[4:]
        print(mactListDB)

        info_UserListDB = list(find_db.values())
        firstname_user = info_UserListDB[2]
        lastname_user = info_UserListDB[3]
        print(firstname_user)
        print(lastname_user)

        result_findMac_database = '1'


def connect_WLC() :
    global mac_wlc, error_connectWLC, number_of_client
    command = 'show wireless client username '
    
    try:
        with ConnectHandler(ip = '172.30.99.56',
                        port = 22,  
                        username = 'admin',
                        password = 'CITS@WLC2023',
                        device_type = 'cisco_wlc_ssh') as ch :
        
            find_mac_wlc = (ch.send_command(command+username))

    except ConnectionRefusedError as err:
        print(f"Connection Refused: {err}")
        error_connectWLC = 1
    except TimeoutError as err:
        print(f"Connection Refused: {err}")
        error_connectWLC = 1
    except Exception as err:
        print(f"Oops! {err}")
        error_connectWLC = 1
    else :
        error_connectWLC = 0
        

    
 

    if error_connectWLC == 1 :
        print("please connect to mfu wifi")
        mac_wlc = 0
    
    else :
        print("WLC connectting")
        print(find_mac_wlc)

        

        

        with open("find_mac_wlc.json", "w") as outfile:
            outfile.write(find_mac_wlc)


        with open('find_mac_wlc.json') as user_file:
            file_contents = user_file.read()
        


        data = file_contents



        #collect find mac address from wlc to mac_adrr.json
        split_data = re.findall(r'\S+', data)
        print(split_data)


        number_of_client = split_data[3]
        
        print(number_of_client)
     

        


        if number_of_client == '1' :
            print('Mac 1 = '+split_data[14])
            mac_dict = {
            'username' : username,
            'Mac Address 1' : split_data[14]
            }
            print(mac_dict)
            json_mac = json.dumps(mac_dict) 
            print(json_mac)

            with open("mac_adrr.json", "w") as outfile:
                json.dump(mac_dict, outfile)
            
            mac_wlc = 1


        elif number_of_client == '2' :
            print('Mac 1 = '+split_data[14])
            print('Mac 2 = '+split_data[21])
            mac_dict = {
            'username' : username,
            'username' :  '6331501067',
            'Mac Address 1' : split_data[14],
            'Mac Address 2' : split_data[21]
            }
            print(mac_dict)
            json_mac = json.dumps(mac_dict) 
            print(json_mac)

            with open("mac_adrr.json", "w") as outfile:
                json.dump(mac_dict, outfile)

            mac_wlc = 1

        elif number_of_client == '3' :
            print('Mac 1 = '+split_data[14])
            print('Mac 2 = '+split_data[21])
            print('Mac 3 = '+split_data[28])
            mac_dict = {
            'username' : username,
            'Mac Address 1' : split_data[14],
            'Mac Address 2' : split_data[21],
            'Mac Address 3' : split_data[28]
            }
            print(mac_dict)
            json_mac = json.dumps(mac_dict) 
            print(json_mac)

            with open("mac_adrr.json", "w") as outfile:
                json.dump(mac_dict, outfile)

            mac_wlc = 1

        elif number_of_client == '4' :
            print('Mac 1 ='+split_data[14])
            print('Mac 2 ='+split_data[21])
            print('Mac 3 ='+split_data[28])
            print('Mac 4 ='+split_data[35])
            mac_dict = {
            'username' : username,
            'Mac Address 1' : split_data[14],
            'Mac Address 2' : split_data[21],
            'Mac Address 3' : split_data[28],
            'Mac Address 4' : split_data[35],
            }
            print(mac_dict)
            json_mac = json.dumps(mac_dict) 
            print(json_mac)

            with open("mac_adrr.json", "w") as outfile:
                json.dump(mac_dict, outfile)

            mac_wlc = 1

        elif number_of_client == '5' :

            print('Mac 1 ='+split_data[14])
            print('Mac 2 ='+split_data[21])
            print('Mac 3 ='+split_data[28])
            print('Mac 4 ='+split_data[35])
            print('Mac 5 ='+split_data[42])
            mac_dict = {
            'username' : username,
            'Mac Address 1' : split_data[14],
            'Mac Address 2' : split_data[21],
            'Mac Address 3' : split_data[28],
            'Mac Address 4' : split_data[35],
            'Mac Address 5' : split_data[42],
            }
            print(mac_dict)
            json_mac = json.dumps(mac_dict) 
            print(json_mac)

            with open("mac_adrr.json", "w") as outfile:
                json.dump(mac_dict, outfile)

            mac_wlc = 1

        else :
            print("Please connect to wifi's office!")
            mac_wlc = 0







def findMac_cmd() :
    global mac_cmd

    # x = subprocess.Popen('netsh wlan show interfaces | find "Physical address"', shell=True, stdout=subprocess.PIPE).stdout.read()

    # print(x)

    # y = x.split()

    # print(len(y))
    # print(y[-1])

    # a = y[-1]


    # encoding = 'utf-8'
    # b  = str(a, encoding)

    z = gma()
    print('z = '+ z)

    c = z.replace(":","")
    # c = b.replace(":","")
    #print(c)


    #print(d)

    def Convert(string):
        list1 = []
        list1[:0] = string
        return list1


    e = Convert(c)
    #print(e)

    e1 = e[0:4]
    e2 = e[4:8]
    e3 = e[8:]

    x1 = ''.join(e1)
    x2 = ''.join(e2)
    x3 = ''.join(e3)
    #print(x1)
    #print(x2)
    #print(x3)

    f = [x1,'.',x2,'.',x3]
    #print(f)
    g = ''.join(f)
    mac_cmd = g
    print("Mac address = "+mac_cmd)



def findMac_wlc() :
 

    global mac_wlc_1
    global mac_wlc_2
    global mac_wlc_3
    global mac_wlc_4
    global mac_wlc_5
    global number_mac_connectting
    global List_macWLC

    List_macWLC = []


    with open('mac_adrr.json') as user_file:
        mac_adrr_json = user_file.read()


        f = open('mac_adrr.json')
        data2 = json.load(f)
        print(data2)
        print(type(data2))

        mac_from_wlc = list(data2.values())
       


    print(mac_from_wlc)
    print(len(mac_from_wlc))


    number_mac_from_wlc = len(mac_from_wlc)
    print(type(number_mac_from_wlc))

    number_mac_connectting = number_mac_from_wlc.__str__()
    print(number_mac_connectting)
    print(type(number_mac_connectting))


#mac address in wlc maximum 5 mac 
    #found 1 mac in wlc
    if number_mac_connectting == '2' :
            mac_wlc_1 = mac_from_wlc[1]
            List_macWLC = [mac_wlc_1]

            print("Mac 1 in WLC =  "+mac_wlc_1)
                               
    #found 2 mac in wlc
    elif number_mac_connectting == '3' :
            mac_wlc_1 = mac_from_wlc[1]
            mac_wlc_2 = mac_from_wlc[2]
            List_macWLC = [mac_wlc_1,mac_wlc_2]

            print("Mac 1 in WLC =  "+mac_wlc_1)
            print("Mac 2 in WLC = "+mac_wlc_2)

    #found 3 mac in wlc
    elif number_mac_connectting == '4' :
            mac_wlc_1 = mac_from_wlc[1]
            mac_wlc_2 = mac_from_wlc[2]
            mac_wlc_3 = mac_from_wlc[3]
            List_macWLC = [mac_wlc_1, mac_wlc_2, mac_wlc_3]

            print("Mac 1 in WLC = "+mac_wlc_1)
            print("Mac 2 in WLC = "+mac_wlc_2)
            print("Mac 3 in WLC = "+mac_wlc_3)

    #found 4 mac in wlc
    elif number_mac_connectting == '5' :
            mac_wlc_1 = mac_from_wlc[1]
            mac_wlc_2 = mac_from_wlc[2]
            mac_wlc_3 = mac_from_wlc[3]
            mac_wlc_4 = mac_from_wlc[4]
            List_macWLC = [mac_wlc_1, mac_wlc_2, mac_wlc_3, mac_wlc_4]

            print("Mac 1 in WLC = "+mac_wlc_1)
            print("Mac 2 in WLC = "+mac_wlc_2)
            print("Mac 3 in WLC = "+mac_wlc_3)
            print("Mac 4 in WLC = "+mac_wlc_4)

    #found 5 mac in wlc
    elif number_mac_connectting == '6' :
            mac_wlc_1 = mac_from_wlc[1]
            mac_wlc_2 = mac_from_wlc[2]
            mac_wlc_3 = mac_from_wlc[3]
            mac_wlc_4 = mac_from_wlc[4]
            mac_wlc_5 = mac_from_wlc[5]  
            List_macWLC = [mac_wlc_1, mac_wlc_2, mac_wlc_3, mac_wlc_4, mac_wlc_5]

            print("Mac 1 in WLC = "+mac_wlc_1)
            print("Mac 2 in WLC = "+mac_wlc_2)
            print("Mac 3 in WLC = "+mac_wlc_3)
            print("Mac 4 in WLC = "+mac_wlc_4)
            print("Mac 5 in WLC = "+mac_wlc_5)


def verifyMac_wlcOnly() :
    global status_verify
    findMac_cmd()
    findMac_wlc()

    if (number_of_client != '0') :
        print("You are connectting MFU's WiFi")
        takeAttendence(username)
        takeAttendence_Json(username)
        attendance_database()
        
        status_verify = '2'
    
    else :
        print("disconnected MFU's WiFi.")
        status_verify = '1'








def verifyMac() :
    global status_verify


    findMac_cmd()
    findMac_wlc()

    if mac_cmd in List_macWLC :
        print(mac_cmd)
        print(type(mac_cmd))
        print("You are connectting MFU's WiFi")
        findMac_database()

        if (result_findMac_database == '0') :
            status_verify = '6'
        
        else :         
            if mac_cmd in mactListDB :
                print("This device is yours.")
                takeAttendence(username)
                takeAttendence_Json(username)
                attendance_database()
                status_verify = '2'
                
            else :
                print("Please connect to MFU's wifi with your username.")
                status_verify = '6'
                
            
        
        
        
    else :
        print("disconnected MFU's WiFi.")
        status_verify = '1'
     


def register_connect_WLC() :
    
    

    command = f'show wireless client mac-address {mac_register} detail'
    command1 = 'show wireless client mac-address'
    command2 = ' detail'  
    
    with ConnectHandler(ip = '172.30.99.56',
                        port = 22,  
                        username = 'admin',
                        password = 'CITS@WLC2023',
                        device_type = 'cisco_wlc_ssh') as ch :
        
        find_register_WLC = (ch.send_command(command))


    print("WLC connectting")
    print(find_register_WLC)

    

    with open("find_register_WLC.json", "w") as outfile:
        outfile.write(find_register_WLC)


def verify_numberUsernameRegister() :
        global number_username_register,result_register_findUsername,result_register_findUsername_verify, username_register
        
        print("verify_numberUsernameRegister()......working") 
        print(username_register)
        number_username_register = len(username_register)

        print(number_username_register)

        if (number_username_register == 11) :
            print("The system found username register.")

            username_register
            username_register = username_register.strip()
            print("username_register................")
            print(username_register)


            result_register_findUsername_verify = '1'
        
        else :
            print("unfound username.")
            result_register_findUsername_verify = '2'



def verify_numberUsername_addDevice() :
        global number_username_register,result_register_findUsername,result_register_findUsername_verify, username_register
        global result_verify_numberUsername_addDevice

        print("verify_numberUsername_addDevice()......working") 
        print(username_register)
        number_username_register = len(username_register)

        print(number_username_register)

        if (number_username_register == 10) :
            print("Verify username addDevice")

            result_verify_numberUsername_addDevice = '1'
        
        else :
            print("Unfound username register.")
            result_register_findUsername_verify = '2'



def register_findUsername() :
    global result_register_findUsername, username_register
    find = 'Client Username '
    find2 ='Client Username'

    with open('find_register_WLC.json') as user_file:
        file_contents = user_file.read()
    
    data = file_contents


    A = data.split('\n')

    number_query = len(A)


    if number_query > 10 : 
        print("You are connecting MFU's Wifi.")   

        B1 = A[1].split(':')
        B2 = A[2].split(':')
        B3 = A[3].split(':')
        B4 = A[4].split(':')
        B5 = A[5].split(':')
        B6 = A[6].split(':')
        B7 = A[7].split(':')
        B8 = A[8].split(':')
        B9 = A[9].split(':')
        B10 = A[10].split(':')
        B11 = A[11].split(':')
        B12 = A[12].split(':')
        B13 = A[13].split(':')
        B14 = A[14].split(':')
        B15 = A[15].split(':')


        if find == B1[0] :
                username_register = B1[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

        elif find == B2[0] :
            username_register = B2[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify
        
        elif find  == B3[0] :
            username_register = B3[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify
        
        elif find  == B4[0] :
            username_register = B4[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify
        
        elif find  == B5[0] :
            username_register = B5[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find  == B6[0] :
            username_register = B6[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find == B7[0] :
            username_register = B7[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find == B8[0] :
            username_register = B8[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find == B9[0] :
            username_register = B9[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find == B10[0] :
            username_register = B10[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find  == B11[0] :
            username_register = B11[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find == B12[0] :
            username_register = B12[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        elif find  == B13[0] :
            username_register = B13[-1]
            print('username register =',username_register)
            result_register_findUsername = result_register_findUsername_verify

        elif find == B14[0] :
            username_register = B14[-1]
            print('username register =',username_register)
            verify_numberUsernameRegister()   
            result_register_findUsername = result_register_findUsername_verify

        elif find == B15[0] :
            username_register = B15[-1]
            print('username register =',username_register)   
            verify_numberUsernameRegister()
            result_register_findUsername = result_register_findUsername_verify

        else :

            if find2 == B1[0] :
                username_register = B1[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B2[0] :
                username_register = B2[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify
            
            elif find2  == B3[0] :
                username_register = B3[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify
            
            elif find2  == B4[0] :
                username_register = B4[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify
            
            elif find2  == B5[0] :
                username_register = B5[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2  == B6[0] :
                username_register = B6[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B7[0] :
                username_register = B7[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B8[0] :
                username_register = B8[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B9[0] :
                username_register = B9[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B10[0] :
                username_register = B10[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2  == B11[0] :
                username_register = B11[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B12[0] :
                username_register = B12[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify

            elif find2  == B13[0] :
                username_register = B13[-1]
                print('username register =',username_register)
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B14[0] :
                username_register = B14[-1]
                print('username register =',username_register)
                verify_numberUsernameRegister()   
                result_register_findUsername = result_register_findUsername_verify

            elif find2 == B15[0] :
                username_register = B15[-1]
                print('username register =',username_register)   
                verify_numberUsernameRegister()
                result_register_findUsername = result_register_findUsername_verify
            
            else :
                print('unfound username register1')
                result_register_findUsername = '0'


    else :
        print("Disconnect to MFU's Wifi.") 
        result_register_findUsername = '0' 


        
def addDevice_findUsername() :
    global result_register_findUsername, username_register
    find = 'Client Username '
    find2 ='Client Username'

    with open('find_register_WLC.json') as user_file:
        file_contents = user_file.read()
    
    data = file_contents


    A = data.split('\n')

    number_query = len(A)


    if number_query > 10 : 
        print("You are connecting MFU's Wifi.")   

        B1 = A[1].split(':')
        B2 = A[2].split(':')
        B3 = A[3].split(':')
        B4 = A[4].split(':')
        B5 = A[5].split(':')
        B6 = A[6].split(':')
        B7 = A[7].split(':')
        B8 = A[8].split(':')
        B9 = A[9].split(':')
        B10 = A[10].split(':')
        B11 = A[11].split(':')
        B12 = A[12].split(':')
        B13 = A[13].split(':')
        B14 = A[14].split(':')
        B15 = A[15].split(':')


        if find == B1[0] :
                username_register = B1[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'


        elif find == B2[0] :
            username_register = B2[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'
        
        elif find  == B3[0] :
            username_register = B3[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'
        
        elif find  == B4[0] :
            username_register = B4[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'
        
        elif find  == B5[0] :
            username_register = B5[-1]
            username_register = username_register.strip()            
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find  == B6[0] :
            username_register = B6[-1]
            username_register = username_register.strip()        
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find == B7[0] :
            username_register = B7[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find == B8[0] :
            username_register = B8[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find == B9[0] :
            username_register = B9[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find == B10[0] :
            username_register = B10[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find  == B11[0] :
            username_register = B11[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find == B12[0] :
            username_register = B12[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find  == B13[0] :
            username_register = B13[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find == B14[0] :
            username_register = B14[-1]
            username_register = username_register.strip()
            print('username register =',username_register)
            result_register_findUsername = '1'

        elif find == B15[0] :
            username_register = B15[-1]
            username_register = username_register.strip()
            print('username register =',username_register)   
            result_register_findUsername = '1'

        else :

            if find2 == B1[0] :
                username_register = B1[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B2[0] :
                username_register = B2[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'
            
            elif find2  == B3[0] :
                username_register = B3[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'
            
            elif find2  == B4[0] :
                username_register = B4[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'
            
            elif find2  == B5[0] :
                username_register = B5[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2  == B6[0] :
                username_register = B6[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B7[0] :
                username_register = B7[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B8[0] :
                username_register = B8[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B9[0] :
                username_register = B9[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B10[0] :
                username_register = B10[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2  == B11[0] :
                username_register = B11[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B12[0] :
                username_register = B12[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2  == B13[0] :
                username_register = B13[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B14[0] :
                username_register = B14[-1]
                username_register = username_register.strip()
                print('username register =',username_register)
                result_register_findUsername = '1'

            elif find2 == B15[0] :
                username_register = B15[-1]
                username_register = username_register.strip()
                print('username register =',username_register)   
                result_register_findUsername = '1'
            
            else :
                print('unfound username register1')
                result_register_findUsername = '0'


    else :
        print("Disconnect to MFU's Wifi.") 
        result_register_findUsername = '0' 


def verify_newUser() :  
    global mac_register, result_newUser

    print("findMac_cmd()......working")  
    findMac_cmd()
    mac_register = mac_cmd
    
    print("register_connect_WLC()......working")
    register_connect_WLC()
    
    print("register_findUsername()......working")
    register_findUsername()

    if (result_register_findUsername == '0') :
        result_newUser = '0'
    
    elif (result_register_findUsername == '2') :
        result_newUser = '2'
    
    else :
        verify_newUser_duplicate()
        if (result_newUser_duplicate == '3') :
            result_newUser = '3'
        
        else : 
            result_newUser = '1'






def verify_addDevice() :  
    global mac_register

    print("findMac_cmd()......working")  
    findMac_cmd()
    mac_register = mac_cmd
    
    print("register_connect_WLC()......working")
    register_connect_WLC()
    
    print("addDevice_findUsername()......working")
    addDevice_findUsername()








def find_database_newUser() :
 
    global find_db_register

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["nutdb"]
    mycol = mydb["information_user2"]

    find_db_register = mycol.find_one({"Username": username_register})
    print("Database connectting")


    print(find_db_register)


def verify_newUser_duplicate() :
    global result_newUser_duplicate
    find_database_newUser()

    if (find_db_register is None) :
        print("Welcome New User")
        result_newUser_duplicate = '1'

    else :
        print("Unable to register new users. because the system already has your name")
        result_newUser_duplicate = '3'






def verify_addDevice_duplicate() :
    global result_addDevice_duplicate
    find_database_newUser()

    if (find_db_register is None) :
        print("Welcome Add device")
        result_addDevice_duplicate = '1'

    else :
        print("Unable to register new users. because the system already has your name")
        result_addDevice_duplicate = '0'
       


    



def TakePhoto4() :
        camera = cv2.VideoCapture(0)  
        
        global frame_capture
        global frame2
        global capture
        
            # Center coordinates
        center_coordinates = (350, 250)
        axesLength = (170, 140)
            
            # Radius of circle
        radius = 200
        angle = 90
        startAngle = 0
            
        endAngle = 360
            # Red color in BGR
        color = (0, 255, 0)
            
            # Line thickness of -1 px
        thickness = 2
        while True:
            check, frame = camera.read()
            frame_capture = check, frame = camera.read()
            frame_circle  = check, frame2 = camera.read()
            frame_circle
            frame_capture

            
            circle = cv2.ellipse(frame2, center_coordinates, axesLength,
                    angle, startAngle, endAngle, color, thickness) #circle


                # print(check) #prints true as long as the webcam is running
                # print(frame) #prints matrix values of each framecd 
                
            # if(capture):
                    

            if(capture == 1) :
                        now = datetime.datetime.now()
                        p = os.path.sep.join(['img_register',f'{firstname_newUser} {lastname_newUser}_{username_register}_1.jpg'])
                        cv2.imwrite(p, frame)
                        
                    
            
                    # key = cv2.waitKey(20)
                    


            # except Exception as e:
            #     pass
            A = ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            A
            frame = buffer.tobytes()

            B = ret, buffer2 = cv2.imencode('.jpg', cv2.flip(frame2,1))
            B
            frame2 = buffer2.tobytes()
            yield (b'--frame2\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            key = cv2.waitKey(20)
            if key == 27:
                break
          


@app.route('/register_capture', methods=['POST'])
def register_capture() :
    
    global switch,camera,P
    
    captureBtn = request.form.get('data')

    if captureBtn == 'capture' :

        print('user press next button1 ' + captureBtn)
        global capture
        capture=1

        register_newUser()


        result = '1'


        return result
    
   







def attendance_database() :
    # Making Connection
    myclient = MongoClient("mongodb://localhost:27017/")

    # database
    db = myclient["nutdb"]


    Collection = db["attendance"]

    with open('attendance_dict.json') as file:
        file_data = json.load(file)	

    if isinstance(file_data, list):
        Collection.insert_many(file_data)
    else:
        Collection.insert_one(file_data)
    
    print("save to database already.")



def register_database() :
    # Making Connection
    myclient = MongoClient("mongodb://localhost:27017/")

    # database
    db = myclient["nutdb"]


    Collection = db["information_user2"]

    with open('register_dict.json') as file:
        file_data = json.load(file)	

    if isinstance(file_data, list):
        Collection.insert_many(file_data)
    else:
        Collection.insert_one(file_data)
    
    print("save register to database already.")


def register_newUser() :

    register_Json(username_register)
    print("register_Json()......working")

    register_database() 
    print("register_database()......working") 






@app.route('/add_device', methods=['POST'])
def add_device() :

    newUserBtn = request.form.get('data')

    if newUserBtn == 'addDevice' :
        print('user press next button ' + newUserBtn)        

        addDevice_verify_username()

        result = result_addDevice 
        print(result)

            
        return result


def addDevice_verify_username() :
    global mac_register , result_addDevice
    global mactListDB_addDevice, result_verifyMac_addDevice_duplicate
    global result_addDevice

    print("findMac_cmd()......working")  
    findMac_cmd()
    mac_register = mac_cmd
    
    print("register_connect_WLC()......working")
    register_connect_WLC()

    print("addDevice_findUsername()......working")
    addDevice_findUsername()

    if (result_register_findUsername == '0') :
        print("Disconnected to WiFi")
        result_addDevice = result_register_findUsername
    
    else :
        verify_numberUsername_addDevice()

        if (result_verify_numberUsername_addDevice == '1') :

            result_addDevice = '1'
        
        else :
            result_addDevice = '2'



def addDevice_Function() :
    global mac_register , result_addDevice2, firstname_addDevice, lastname_addDevice
    global mactListDB_addDevice, result_verifyMac_addDevice_duplicate, result_verify_AddDeviceDB, find_db

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["nutdb"]
    mycol = mydb["information_user2"]
    coll = mydb["information_user2"]



    find_db = mycol.find_one({"Username": username_register})
    find_db

    print(find_db)
    print("Database connectting")
    print(username_register)
    print(type(username_register))


    if (find_db is None) :
            

        print("Please register a new user!")
            
        result_verifyMac_addDevice_duplicate = '2'
        global result_addDevice2
        result_addDevice2 = result_verifyMac_addDevice_duplicate
    

    else :
        ListDB = list(find_db.values())
        firstname_addDevice = ListDB[2]
        lastname_addDevice = ListDB[3]
        print(firstname_addDevice)
        print(lastname_addDevice)

        print("verify_AddDeviceDB().......working")

        verify_AddDeviceDB()   

        result_addDevice2 = result_verify_AddDeviceDB
        print(result_addDevice2)

        





def delete_db() :
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["nutdb"]
        coll = mydb["information_user2"]

        myQuery = {"Username": username_register}

        coll.delete_one(myQuery)
    
def insert_db() :
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["nutdb"]
        coll = mydb["information_user2"]

        with open('update_db.json') as file:
            file_data = json.load(file)	
            
        if isinstance(file_data, list):
            coll.insert_many(file_data)
        else:
            coll.insert_one(file_data)

    
def verifyMac_addDevice_duplicate() :
        global result_verifyMac_addDevice_duplicate , result_addDevice, result_addDevice2

        if(mac_register in mactListDB_addDevice) :
            print("This device has registered already.")
            result_verifyMac_addDevice_duplicate = '3'
            
        
        else :
            AddDevice_process()
            
            result_verifyMac_addDevice_duplicate = result_AddDevice_process
            


def AddDevice_process() :
        global result_AddDevice_process
        if (number_mac == 1) :
            
            number = '2'
            # find_db[word_mac] = mac_new
            word_mac = f'Mac Address {number}'
            find_db[word_mac] = mac_register
            print(find_db)
            
            update_db = find_db


            with open("update_db.json", "w") as outfile:
                json.dump(find_db, outfile)
            
            
            delete_db()
            insert_db()
            result_AddDevice_process = '1'

        elif (number_mac == 2) :
            
            number = '3'
            # find_db[word_mac] = mac_new
            word_mac = f'Mac Address {number}'
            find_db[word_mac] = mac_register
            print(find_db)
            
            update_db = find_db

            with open("update_db.json", "w") as outfile:
                json.dump(update_db, outfile)
            
            delete_db()
            insert_db()

            result_AddDevice_process = '1'

        elif (number_mac == 3) :
            
            number = '4'
            # find_db[word_mac] = mac_new
            word_mac = f'Mac Address {number}'
            find_db[word_mac] = mac_register
            print(find_db)
            
            update_db = find_db

            with open("update_db.json", "w") as outfile:
                json.dump(update_db, outfile)
            
            delete_db()
            insert_db()
            result_AddDevice_process = '1'

        elif (number_mac == 4) :
            
            number = '5'
            # find_db[word_mac] = mac_new
            word_mac = f'Mac Address {number}'
            find_db[word_mac] = mac_register
            print(find_db)
            
            update_db = find_db

            with open("update_db.json", "w") as outfile:
                json.dump(update_db, outfile)
            
            delete_db()
            insert_db() 
            result_AddDevice_process = '1'  

        
        else :
            print("registered the full number of devices.")
            result_AddDevice_process = '4'





def verify_AddDeviceDB() :
        global result_verifyMac_addDevice_duplicate, number_mac, result_addDevice2
        global result_verify_AddDeviceDB, mactListDB_addDevice
         
        print("The system found your information.")

        find_db.pop('_id')
        print(find_db)

        mactListDB_addDevice = list(find_db.values())
        mactListDB_addDevice = mactListDB_addDevice[3:]

        print(mactListDB_addDevice)

        print(len(mactListDB_addDevice))

        number_mac = len(mactListDB_addDevice)

        

            

        verifyMac_addDevice_duplicate()
        if (result_verifyMac_addDevice_duplicate == '1') :
            result_verify_AddDeviceDB = '1'

        
        elif (result_verifyMac_addDevice_duplicate == '3') :
            result_verify_AddDeviceDB = '3'
        
        elif (result_verifyMac_addDevice_duplicate == '4') :
            result_verify_AddDeviceDB = '4'


        else :
            result_verify_AddDeviceDB = '99'



@app.route('/inputName', methods=['GET', 'POST']) 
def inputName() :
    global firstname_newUser, lastname_newUser

    if request.method == "POST":
       # getting input with name = fname in HTML form
        firstname_newUser = request.form.get("fname")
       # getting input with name = lname in HTML form
        lastname_newUser = request.form.get("lname")

        print("new user = ", firstname_newUser, lastname_newUser)
        return render_template("register_face.html")
    
    # return render_template("register_face.html")
            


        
    

if __name__ == "__main__":
    app.run(debug=True)