from asyncio.windows_events import NULL
from contextlib import nullcontext
from django.http import JsonResponse
from django.shortcuts import render

from RailwayApp.form import AdminLoginForm, RailForm, UserForm, UserLoginForm
from RailwayApp.models import AdminLogin, Booking, Rail, Seat, User

from django.core.mail import send_mail 
from django.conf import settings
from django.core import serializers

#admin login
def login(request):
    loginform = AdminLoginForm()
    return render(request, 'login.html', {'form': loginform})


def loginAdmin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    adminLoginForm = AdminLoginForm()

    try:
        user = AdminLogin.objects.get(username = username)
        if(password == user.password):
            request.session['usernameAdmin'] = username
            request.session['idAdmin'] = user.id
            request.session['emailAdmin'] = user.email

            pending = Booking.objects.filter(accept = False).count()
            booked = Booking.objects.filter(accept = True).count()

            return render(request, "admin/index.html", {'username':username, 'pending': pending, 'booked': booked})
        else:
            msg="Invalid Password"
            return render(request, "admin/adminLogin.html", {'form':adminLoginForm,'adminmsg': msg})
    except:
        msg = "Username Invalid!!!!"
        return render(request, "admin/adminLogin.html", {'form':adminLoginForm,'adminmsg': msg})


def adminlogout(request):
    adminLoginForm = AdminLoginForm()
    if request.session.has_key('usernameAdmin'):
        del request.session['usernameAdmin']
        return render(request, "admin/adminLogin.html", {'form':adminLoginForm})


#admin index
def index(request):
    #if request.session.has_key('username'):
    #username = request.session['username']
    pending = Booking.objects.filter(accept = False).count()
    booked = Booking.objects.filter(accept = True).count()
    return render(request, "admin/index.html", {'pending': pending, 'booked': booked})
    #else:
        #return render(request, "login.html")

#add page
def addRail(request):
    addform = RailForm()
    return render(request, 'admin/addRail.html', {'form': addform})

#add post
def addRailPost(request):
    addform = RailForm()
    try:
        name = request.POST.get('name')
        fromAddress = request.POST.get('fromAddress')
        toAddress = request.POST.get('toAddress')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        date = request.POST.get('date')
        time = request.POST.get('time')

        ques = Rail(name = name, fromAddress = fromAddress, toAddress = toAddress, price = price, duration = duration, date = date, time = time)
        ques.save()

        msg = "Rail Added Succesfully!!"
        return render(request, 'admin/addRail.html', {'form': addform, 'msg':msg})
    except:
        msg = "Error Occured!!"
        return render(request, 'admin/addRail.html', {'form': addform, 'msg':msg})


def showRails(request):
    data = Rail.objects.all()
    return render(request, 'admin/show.html', {'data': data})


def edit(request, id):
    edit_rail = Rail.objects.get(id = id)
    return render(request, "admin/edit.html", {'data':edit_rail})


def updateRail(request):
    qid = request.POST.get('id')
    print("rail id: ", qid)
    try:
        # data fetch by id
        que = Rail.objects.get(id=qid)
        que.id = request.POST.get('id')
        que.name = request.POST.get('name')
        que.fromAddress = request.POST.get('fromAddress')
        que.toAddress = request.POST.get('toAddress')
        que.price = request.POST.get('price')
        que.duration = request.POST.get('duration')
        que.date = request.POST.get('date') 
        que.time = request.POST.get('time')
        que.save()
        msg = "Successfully Updated"
        question_all = Rail.objects.all()
        return render(request, 'admin/show.html', {'data': question_all, 'msg': msg})
    except Exception as e:
        msg = str(e) #"Error Cannot Edit"
        edit_ques = Rail.objects.get(id = qid)
        return render(request, 'admin/edit.html', {'data': edit_ques, 'msg': msg})


def deleteRail(request, qid):
    que = Rail.objects.get(id=qid)
    que.delete()
    un = Rail.objects.all()
    return render(request, 'admin/show.html', {'data':un, 'msg':"Deleted Successfully"})

#users
def userRegister(request):
    reg_form = UserForm()
    try:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            msg = "User Registered Successfully!!"
            return render(request, "users/register.html", {'form': reg_form, 'registermsg': msg})
        else:
            msg = "Invalid Form!!"
            return render(request, "users/register.html", {'form': reg_form, 'registermsg': msg})
    except:
        msg = "Error. Cannot Register User!!!"
        return render(request, "users/register.html", {'form': reg_form, 'registermsg': msg})


def loginUser(request):
    loginform = UserLoginForm()
    return render(request, 'users/login.html', {'form': loginform})


def loginUserPost(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    userLoginForm = UserLoginForm()

    try:
        user = User.objects.get(username = username)
        if(password == user.password):
            request.session['username'] = username
            request.session['id'] = user.id
            request.session['email'] = user.email
            request.session['verified'] = user.verified
            #get rail list
            allRails = Rail.objects.all()
            return render(request, "users/userDashboard.html", {'welcome': username, 'data': allRails, 'verified': user.verified })
        else:
            msg="Invalid Password"
            return render(request, "users/login.html", {'form':userLoginForm,'usermsg': msg})
    except:
        msg = "Username Invalid!!!!"
        return render(request, "users/login.html", {'form':userLoginForm,'usermsg': msg})


def userlogout(request):
    loginForm = UserLoginForm()
    if request.session.has_key('username'):
        del request.session['username']
        allRails = Rail.objects.all()
        return render(request, "users/home.html", {'form':loginForm, 'data': allRails})


def userIndex(request):
    allRails = Rail.objects.all()
    return render(request, 'users/home.html', {'data': allRails})


def getDetails(request, id):
    getbyId = Rail.objects.get(id = id)
    return render(request, 'users/userDashDetails.html', {'data': getbyId})


#insert booking into booking table
def bookTicket(request):
    if request.session.has_key('username'):
        username = request.session['username']
        userid = request.session['id']
        
        #get parameter from ajax
        railId = request.GET.get('railId', None)
        date = request.GET.get('date', None)

        getRailbyId = Rail.objects.get(id = railId)
        railName = getRailbyId.name
        fromAddress = getRailbyId.fromAddress
        toAddress = getRailbyId.toAddress
        price = getRailbyId.price

        getUserbyId = User.objects.get(id = userid)
        fullname = getUserbyId.firstname + " " + getUserbyId.lastname
        username = getUserbyId.username
        email = getUserbyId.email
        contact = getUserbyId.contact

        accept = False

        book = Booking(railId = railId, railName = railName, fromAddress = fromAddress, toAddress = toAddress, price = price, \
        userId = userid, fullname = fullname, username = username, email = email, contact = contact, accept = accept, date = date)
        book.save()

        return JsonResponse({"data": "Success"}, status=200)
    else:
        #userLoginForm = UserLoginForm()
        #msg = "You must be logged in!!"
        return JsonResponse({"data": "You must be logged in !!"}, status=200)
       # return render(request, "users/login.html", {'form':userLoginForm,'usermsg': msg})


#insert seat into seat table
def checkTicket(request):
    userid = request.session['id']
        
    #get parameter from ajax
    railId = request.GET.get('railId')
    selected = request.GET.getlist('selected[]')
    date = request.GET.get('date')

    getRailbyId = Rail.objects.get(id = railId)
    
    for i in selected:
        book = Seat(railId = railId, userId = userid, seatNumber = i, date = date)
        book.save()
    
    return JsonResponse({"data": selected}, status=200)


#check seat availability
def isTicketAvailable(request):
    #userid = request.session['id']
        
    #get parameter from ajax
    railId = request.GET.get('railId')
    selected = request.GET.getlist('selected[]')
    date = request.GET.get('date')

    getRailbyId = Rail.objects.get(id = railId)

    getSeat = Seat.objects.filter(railId = railId, date = date)
    # seatNumber = getSeat.seatNumber
    seatcount = getSeat.count()

    seatList = []
    for i in getSeat:
        seat = i.seatNumber
        
        seatList.append(seat)
    
    #newList = list(set(seatList) - set(selected))
    newlist = list(set(seatList).intersection(selected))
    #seatList - selected
    
    return JsonResponse({"data": newlist}, status=200)
 
#booking request
def getAllBooking(request):
    return render(request, 'admin/booking.html')

def getAllBookingRequest(request):
    listBooking = Booking.objects.filter(accept = False).values('id','userId','railId','railName','fromAddress','toAddress','fullname', \
                                                                'username','email','contact','date')
    return JsonResponse({'data': list(listBooking)}, status=200)

def getSeatNumberByUser(request):
    userId = request.GET.get('userId')
    railId = request.GET.get('railId')
    date = request.GET.get('date')
    getSeatById = Seat.objects.filter(userId = userId, railId = railId, date = date).values('id','userId','railId','seatNumber','date')
    return JsonResponse({'data': list(getSeatById)}, status=200)

def approveBooking(request, id):
    getBookingId = Booking.objects.get(id = id)
    print("my id:", id)
    getBookingId.accept = True
    getBookingId.save()
    print("my id:", id)
    sendemail(getBookingId.email)

    listBooking = Booking.objects.filter(accept = False)
    return render(request, 'admin/booking.html', {'data': listBooking})


def sendemail(email):
    send_mail(
        subject = 'Railway Ticket Booking Approved',
        message = 'Your request to book ticket have been approved. Thank You for choosing us.',
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [email],
        fail_silently = False,

        # subject = 'welcome to GFG world'
        # message = f'Hi {user.username}, thank you for registering in geeksforgeeks.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email, ]
        # send_mail( subject, message, email_from, recipient_list )


        # fail_silently takes boolean value. If set False it will raise smtplib.STMPException if the error
        # occurs while sending the email
    )
    return JsonResponse({"success": "Success"}, status=200)


def booked(request):
    listBooking = Booking.objects.filter(accept = True)
    return render(request, 'admin/booked.html', {'data': listBooking})


def availableBooking(request):
    listBooking = Rail.objects.all()
    return render(request, 'users/available.html', {'data': listBooking})


def aboutUs(request):
    return render(request, 'users/aboutus.html')


def booktrains(request):
    listBooking = Rail.objects.all()
    return render(request, 'users/booktrains.html', {'data': listBooking})


def userDashboard(request):
    return render(request, 'users/userDashboard.html')


def getDashDetails(request, id):
    getbyId = Rail.objects.get(id = id)
    verified = request.session['verified']
    return render(request, 'users/details.html', {'data': getbyId, 'verified': verified})


def userProfile(request):
    userId = request.session['id']
    verified = request.session['verified']
    getUser = User.objects.get(id = userId)
    return render(request, 'users/profile.html', {'data': getUser, 'verified': verified})


def userBooking(request):
    userId = request.session['id']
    bookingList = Booking.objects.filter(userId = userId)
    return render(request, 'users/mybookings.html', {'data': bookingList})


def cancelBooking(request, id):
    getData = Booking.objects.get(id = id)

    Seat.objects.filter(railId = getData.railId, userId = getData.userId, date = getData.date).delete()

    getData.delete()

    userId = request.session['id']
    bookingList = Booking.objects.filter(userId = userId)
    return render(request, 'users/mybookings.html', {'data': bookingList})


#send email
def sendVerifyEmail(request):
    if request.method == "GET":
        email = request.GET.get('email', None)
        code = request.GET.get('code', None)
        send_mail(
            subject = 'Email Verification',
            message = code + ' is your verification code.',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [email],
            fail_silently = False,
            # fail_silently takes boolean value. If set False it will raise smtplib.STMPException if the error
            # occurs while sending the email
        )
        return JsonResponse({"success": "Success"}, status=200)
    else:
        return JsonResponse({"error": "form.errors"}, status=400)

#check username exists
def checkUsername(request):
    if request.method == "GET":
        username = request.GET.get('uName', None)
        data = User.objects.filter(username = username)
        if data.count() == 0:
            return JsonResponse({"data": "Success"}, status=200)
        else:
            return JsonResponse({"data": "Error"}, status=200)
    else:
        return JsonResponse({"error": "form.errors"}, status=400)

#update verify ststus
def updateVerifyStatus(request):
    try:
        userId = request.session['id']
        getbyId = User.objects.get(id = userId)
        getbyId.verified = True
        getbyId.save()
        return JsonResponse({"data": "Success"}, status=200)
    except:
        return JsonResponse({"data": "Error"}, status=200)