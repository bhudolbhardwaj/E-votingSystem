from django.shortcuts import render,HttpResponse
from .models import Candidate,Voter,Official,Voted
import pytesseract
import cv2
from time import sleep
from django.db.models import F

# Scanning image to extract aadhar number from aadhar card
def aadharscanning():
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)
    def process_image(iamge_name, lang_code):
        return pytesseract.image_to_string(iamge_name, lang=lang_code)
    i=0
    aadhar_num = {}
    while i<50:
        i+=1
        try:
            check, frame = webcam.read()
            cv2.waitKey(1)
            img = cv2.resize(frame, (800, 600), fx = 0.1, fy = 0.1)
            img = cv2.rectangle(img, (200,400),(600,475), (0,255,0),2)
            cv2.imshow("Capturing", img)
            img = img[400:475,200:600]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            word = process_image(img, "eng")
            if word=='':
                pass
            else:
                word=''.join(i for i in word if i.isdigit())
                if word in aadhar_num:
                    aadhar_num[word] += 1
                else:
                    aadhar_num[word] = 1
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
    # for key,value in aadhar_num.items():
    #     print(key,'---:---',value)
    final_aadhar_num=max(aadhar_num,key=aadhar_num.get)
    print("\nFinal Result : ",final_aadhar_num)
    cv2.destroyAllWindows()
    return final_aadhar_num

# Rendering main page.
def index(request):
    return render(request,'index.html')

# Officer login after verification.
def officerlogin(request):
    usn,pwd = '',''
    flag = False
    if request.method == "POST":
        usn = request.POST.get('usn')
        pwd = request.POST.get('pwd')
    usn = Official.objects.filter(username=usn)
    pwd = Official.objects.filter(password=pwd)
    if ((len(usn)!=0) and (len(pwd)!=0)):
        flag = True
        return render(request,'register.html',{'flag':flag})
    else:
        return render(request, 'officer.html')
    return render(request, 'officer.html')

# Registering new user
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        district = request.POST.get('district')
        date = request.POST.get('date')
        sex = request.POST.get('sex')
        aadhar = request.POST.get('aadharnum')
        # print(name, mobile, state, date, sex, aadhar)
        test_data = Voter.objects.filter(aadhar_number=aadhar)
        if len(test_data)==0:
            data = Voter(name=name.lower(),district=district.lower(),gender=sex.lower(),mobile=mobile,aadhar_number=aadhar,dob=date)
            data.save()
        else:
            print('Aadhar already registered')
            return HttpResponse('<script> alert("Aadhar already registered") </script>')
    return render(request,'register.html')

# Voter login after scanning aadhar number
def voterlogin(request):
    if request.method == "POST":
        try:
            final_aadhar_num = aadharscanning()
            test_data = Voter.objects.values('id','district','aadhar_number','name').get(aadhar_number=final_aadhar_num)
            # print(test_data)
            voted_candidate = Voted.objects.filter(name='{}{}'.format(test_data['id'],test_data['name']))
            if (test_data) and (len(voted_candidate)==0):
                candidates = Candidate.objects.values('name','party_name','district').filter(district=test_data['district'])
                Voted(name='{}{}'.format(test_data['id'],test_data['name'])).save()
                return render(request, 'voting.html', {'flag':True, 'candidate':candidates,'cname':test_data['name']})
            else:
                return HttpResponse("<h1>You already voted.</h1>")
        except Exception as e:
            print(e)
            cv2.destroyAllWindows()
            return render(request, 'voting.html', {'flag':False})
    return render(request,'voterlogin.html')

#  Voting page after everything either fails or success.
def voting(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Candidate.objects.filter(name=name).update(vote_count=F('vote_count') + 1)
    return render(request,"thankyou.html")