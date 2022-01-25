from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from Seeker.models import *
from Seeker.views import p_comment
from .models import *
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from random import *

# Create your views here.
count=0

@csrf_exempt
def sign_in(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Company":
            cid = Company.objects.get(user_id = uid)
            j_all = Job.objects.all()
            context = {
                'uid':uid,
                'cid':cid,
                'j_all':j_all
            }
            return render(request,"Company/index.html",{'context':context})

        elif uid.role == "Seeker":
            sid = Seeker.objects.get(user_id = uid)
            f_id = Following.objects.filter(seeker_id=sid)
            s_follow = f_id.count()
            
            job_follow =[]

            for i in f_id:
                cid = Company.objects.get(id=i.company_id.id)
                job = Job.objects.filter(company_id=cid).order_by('-id')[:2]
                job_follow.append(job)
            
            print('==========================',job)
            print('==========================',job_follow)


            context={
                'uid':uid,
                'sid':sid,
                's_follow':s_follow,
                'job_follow':job_follow,
            }
            return render(request,"Seeker/s-index.html",{'context':context})
    if "user" in request.POST:
        email = request.POST['email']
        pswd = request.POST['password']
        cpswd = request.POST['cpassword']
        s_pic = request.FILES['profile_pic']
        role = "Seeker"

        if pswd==cpswd:
            uid = User.objects.create(email = email, password=cpswd, role = role)
            sid = Seeker.objects.create(
                user_id = uid,
                sname = request.POST['name'],
                city = request.POST['country'],
                s_pic = s_pic
            )       
        if sid:
            msg = "Thank You for Register"
            send_mail("Welcome To Workwise",msg,"anjali.20.learn@gmail.com",[email])
            # context={
            #     'uid':uid,
            #     'sid':sid
            # }
            return render(request,"Company/sign-in.html",)
    elif "company" in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        role = "Company"

        if password == cpassword:
            uid = User.objects.create(email = email, password = password, role = role)
            cid = Company.objects.create(
                user_id = uid,
                cname = request.POST['cname'],
                city = request.POST['city'],
                id_proof = request.FILES['id_proof'],
                c_pic = request.FILES['c_profile']
            )
            msg = "You are Successfully Register"
            send_mail("Register",msg,"anjali.20.learn@gmail.com",[email])
            return render(request,"Company/sign-in.html")
        else:
            e_msg = "Invalid Email or Password"
            return render(request,"Company/sign-in.html",{'e_msg':e_msg})

    elif "sign-in" in request.POST:
        global count
        if request.POST:
            try:
                email = request.POST['email']
                password = request.POST['password']
                
                uid = User.objects.get(email = email)
                if uid:
                    if uid.password == password: 
                        if uid.role == "Company":
                            count=0
                            cid = Company.objects.get(user_id = uid)
                            j_all =Job.objects.all()
                            context = {
                                'uid':uid,
                                'cid':cid,
                                'j_all':j_all
                            }
                            request.session['email'] = uid.email
                            return render(request,"Company/index.html",{'context':context})
                        elif uid.role == "Seeker":
                            count=0
                            sid = Seeker.objects.get(user_id = uid)
                            
                            context={
                                'uid':uid,
                                'sid':sid
                            }
                            request.session['email'] = uid.email
                            return render(request,"Seeker/s-index.html",{'context':context})
                    else:                        
                        emsg = "Invalaid Password"
                        return render(request,"Company/sign-in.html",{'emsg':emsg})
                else:
                    return render(request,"Company/sign-in.html")
            except:
                emsg = "Invalid Email or Password"
                return render(request,"Company/sign-in.html",{'emsg':emsg})                
        else:        
            return render(request,"Company/sign-in.html")
    else:
        return render(request,"Company/sign-in.html")

def index(request):
    return redirect('sign-in')

def profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        j_all = Job.objects.all()
        p_all = Project.objects.all()

        followers = Following.objects.filter(company_id=cid).count()
        all_link = Link.objects.get(user_id=uid)
        context = {
            'uid':uid,
            'cid':cid,
            'j_all':j_all,
            'p_all': p_all,
            'followers':followers,
            'all_link':all_link,
        }
        return render(request,"Company/c-profile.html",{'context':context})

def logout(request):
    if "email" in request.session:
        del request.session['email']
        return redirect('sign-in')

    else:
        return redirect('sing-in')


def add_jobs(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)

        jid = Job.objects.create(
            company_id = cid,
            jpost = request.POST['jpost'],
            jtags = request.POST['jtags'],
            jsalary = request.POST['jsalary'],
            jduration = request.POST['jduration'],
            jdesc = request.POST['jdesc']
        )
        return redirect('sign-in')    
    else:
        return redirect('sign-in')

def my_jobs(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        j_all = Job.objects.filter(company_id = cid)
        context ={
            'uid':uid,
            'cid':cid,
            'j_all':j_all
        }
        return render(request,"Company/jobs.html",{'context':context})
    else:
        return redirect('sign-in')

def all_jobs(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        j_all = Job.objects.exclude(company_id = cid)
        context = {
            'uid':uid,
            'cid':cid,
            'j_all':j_all
        }
        return render(request,"Company/all-jobs.html",{'context':context})
    else:
        return redirect('sign-in')

def add_project(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        pid = Project.objects.create(
            company_id = cid,
            p_post = request.POST['p_post'],
            ptags = request.POST['ptags'],
            salary_start = request.POST['price1'],
            salary_end = request.POST['price2'],
            pduration = request.POST['pduration'],
            pdesc = request.POST['pdesc']
        )
        return redirect('sign-in')    
    else:
        return redirect('sign-in')

def my_project(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid  = Company.objects.get(user_id = uid)
        p_all = Project.objects.filter(company_id = cid)
        context = {
            'uid':uid,
            'cid':cid,
            'p_all':p_all
        }
        return render(request,"Company/my-projects.html",{'context':context})
    else:
        return redirect('sign-in')

def all_project(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        p_all = Project.objects.exclude(company_id = cid)
        context = {
            'uid':uid,
            'cid':cid,
            'p_all':p_all
        }
        return render(request,"Company/all-projects.html",{'context':context})
    else:
        return redirect('sign-in')

def forgot_password(request):
    if request.POST:
        email = request.POST['email']
        otp = randint(1111,9999)
        uid = User.objects.get(email = email)
        try:
            if uid:
                uid.otp = otp
                uid.save()
                cid = Company.objects.get(user_id = uid)
                msg1 = "Dear"+cid.cname+","
                msg = "\nYour otp is :"+str(otp)+", and is valid for 2 minutes."
                send_mail("WorkWise - OTP",msg1+msg,"anjali.20.learn@gmail.com",[email])
                return render(request,"Company/otp.html",{'email':email})
        except:
            e_msg = "email does not exist"
            return render(request,"Company/forgot-password.html",{'e_msg':e_msg})
    else:
        return render(request,"Company/forgot-password.html")


def otp(request):
    if request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        uid = User.objects.get(email = email)
        if uid:
            if str(uid.otp) == otp and uid.email == email:
                return render(request,"Company/reset-password.html",{'email':email})
            else:
                e_msg = "invalid otp"
                return render(request,"Company/otp.html",{'e_msg':e_msg})
    else:
        e_msg = "Time Out"
        return render(request,"Company/forgot_password.html",{'e_msg':e_msg})

def reset_password(request):
    if request.POST:
        email = request.POST['email']
        npassword = request.POST['npassword']
        cpassword = request.POST['cpassword']
        uid = User.objects.get(email = email)
        if uid:
            if npassword == cpassword:
                uid.password = cpassword
                uid.is_verified = True
                uid.save()
                return redirect('sign-in')
            else:
                e_msg = "!! newpassword & confirmpassword does not match !!"
                return render(request,"Company/reset-password.html",{'e_msg':e_msg})
    else:
        return redirect('forgot_password')

@csrf_exempt
def proj_com(request):
    if "email" in request.session:
        pid = Project.objects.get(id = request.POST['id'])
        print('============',pid)
        ask = request.POST['ask']

        p_comment = Comment.objects.filter(project_id=pid)

        pro=[]
        for i in p_comment:
            pro.append(i.value)
        
        seek=[]
        for i in p_comment:
            seek.append(i.seeker_id.sname)
        
        return JsonResponse({'ask':ask,'pro':pro,'seek':seek})

    
    else:
        return redirect('sign-in')


@csrf_exempt
def job_com(request):
    if "email" in request.session:
        jid = Job.objects.get(id=request.POST['id'])
        ask = request.POST['ask']

        comm =  Jcomment.objects.filter(job_id=jid)
        j_comm = list(comm.values())

        seek=[]
        for i in comm:
            seek.append(i.seeker_id.sname)


        return JsonResponse({'ask':ask,'j_comm':j_comm,'seek':seek})

    else:
        return redirect('sing-in')

def c_social_link(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Company.objects.get(user_id=uid)

        context={
            'ud':uid,
            'cid':cid,
        }
        return render(request,"Company/c-social-link.html",{'context':context})
    
    else:
        return redirect('sign-in')

def c_add_link(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        cid = Company.objects.get(user_id=uid)

        
        u_link = Link.objects.filter(user_id=uid)

        if u_link:
            pass
        else:
            u_link = Link.objects.create(user_id=uid)
        
        ulink = Link.objects.get(user_id=uid)

        if request.POST['facebook']!='':            
            ulink.facebook = request.POST['facebook']
            # print('========',ulink.facebook)
            ulink.save()

        if request.POST['twitter']!='': 
            print('================')           
            ulink.twitter = request.POST['twitter']
            ulink.save()

        if request.POST['pinterest']!='':            
            ulink.pinterest = request.POST['pinterest']
            ulink.save()

        if request.POST['instagram']!='':            
            ulink.instagram = request.POST['instagram']
            ulink.save()
        
        if request.POST['youtube']!='':            
            ulink.youtube = request.POST['youtube']
            ulink.save()

        return redirect('c-social-link')

    else: 
        return redirect('sign-in')

def c_change_pass(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id=uid)

        cpass = request.POST['cpassword']

        if uid.password==cpass:
            npass = request.POST['npassword']
            uid.password = npass
            uid.save()
        else:
            pass

        return redirect('profile')
    
    else:
        return redirect('sign-in')

def c_change_img(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)

        cprofle = request.FILES['cprofle']
        cid.c_pic = cprofle
        cid.save()

        return redirect('profile')

    else:
        return redirect('sign-in')


def c_notification(request):
    if "email" in request.session:
        pass

    else:
        return redirect('sign-in')



