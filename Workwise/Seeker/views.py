from json.encoder import JSONEncoder
from typing import KeysView
from django.shortcuts import redirect, render
from django.http import JsonResponse
from Company.models import *
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def s_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        j_all = Job.objects.all()
        s_follow = Following.objects.filter(seeker_id=sid).count()

        all_link = Link.objects.get(user_id=uid)

        p_bid = ProjectBid.objects.filter(seeker_id=sid)


        context = {
            'uid':uid,
            'sid':sid,
            'j_all': j_all,
            'all_link':all_link,
            's_follow':s_follow,
            'p_bid':p_bid,
        }
        return render(request,"Seeker/s-profile.html",{'context':context})
    else:
        return redirect('sign-in')


def s_all_job(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        j_all = Job.objects.all()

        saved = SavedJob.objects.filter(seeker_id = sid)
        save_job = []

        for s in saved:
            save_job.append(s.job_id.id)

        a_job = ApplyJob.objects.filter(seeker_id = sid)
        apply_job = []
        for i in a_job:
            apply_job.append(i.job_id.id)
        # print('=====================',apply_job)

        like_job = []

        liked = JobLike.objects.filter(seeker_id=sid)

        for i in liked:
            like_job.append(i.job_id.id)
        # print('============',like_job)

        context = {
            'uid':uid,
            'sid':sid,
            'j_all':j_all,
            'save_job':save_job,
            'like_job':like_job,
            'apply_job': apply_job,
        }
        return render(request,"Seeker/s-all-jobs.html",{'context':context})
    else:
        return redirect('sign-in')

@csrf_exempt
def job_like(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        id = request.POST['id']
        mydata = request.POST['mydata']

        jid = Job.objects.get(id=id)
        j_like = JobLike.objects.filter(job_id=jid, seeker_id=sid)

        a=0 

        if j_like:
            a=1
            j_like.delete()

        else:
            j_like = JobLike.objects.create(job_id=jid, seeker_id=sid)
        print('===========',a)
        return JsonResponse({'a':a,'mydata':mydata})
    
    else:
        return redirect('sign-in')

@csrf_exempt
def js_like(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id=uid)
        id = request.POST['id']
        mylike = request.POST['mylike']
        js_id = SavedJob.objects.get(id=id)
        jid = js_id.job_id.id
        print('======================',jid)
        js_like = JobLike.objects.filter(job_id=jid,seeker_id=sid)
        a=0

        if js_like:
            a=1
            js_like.delete()
        else:
            js_like = JobLike.objects.create(job_id=jid,seeker_id=sid)

        return JsonResponse({'a':a,'mylike':mylike})

    else:
        return redirect('sign-in')


@csrf_exempt
def apply_job(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        id = request.POST['id']
        jid = Job.objects.get(id = id)
        mydata = request.POST['mydata']
        j_id = ApplyJob.objects.filter(job_id = id, seeker_id = sid)
         
        if j_id:
            pass
        else:       
            jname = jid.jpost
            value = "You Successfully Apllied for "+jname+" from Job"
            nid = Notification.objects.create(seeker_id=sid,value=value)
            j_id = ApplyJob.objects.create(job_id = jid, seeker_id = sid)
        
        return JsonResponse({'mydata':mydata})

@csrf_exempt
def save_apply_job(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id=uid)
        id = request.POST['id']

        
        j_id = SavedJob.objects.get(id=id)
        jid = j_id.job_id

        job_app = ApplyJob.objects.filter(job_id=jid,seeker_id=sid)

        if job_app:
            pass
        else:
            jname = j_id.job_id.jpost
            value = "You Successfully Applied for "+jname+" from Saved Job"
            nid = Notification.objects.create(seeker_id=sid,value=value)
            job_app = ApplyJob.objects.create(job_id=jid,seeker_id=sid)

        return JsonResponse({'msg':'success'})

    else:
        return redirect('sign-in')


@csrf_exempt
def save_job(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        j_id = request.POST['id']
        mydata = request.POST['mydata']
        jid = Job.objects.get(id = j_id)
        jall = SavedJob.objects.filter(job_id = jid, seeker_id = sid)
        a=0
        if jall:
            a=1
            jall.delete()
        else:
            jsid = SavedJob.objects.create(job_id = jid, seeker_id = sid)
        
        return JsonResponse({'a':a,'mydata':mydata})
    else:
        return redirect('sign-in')

@csrf_exempt
def saved_job(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        id = request.POST['id']
        mydata = request.POST['mydata']
        job_id = SavedJob.objects.filter(id =id, seeker_id=sid)
        a=0
        if job_id:
            if job_id[0].status=="Saved":
                a=1
                job_id[0].status = "Unsaved"
                job_id[0].save()
            elif job_id[0].status == "Unsaved":
                job_id[0].status = "Saved"
                job_id[0].save()
        else:
            pass
        return JsonResponse({'a':a,'mydata':mydata}) 

    else:
        return redirect('sign-in')

def save_all_job(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        j_all = SavedJob.objects.filter(seeker_id = sid,status="Saved")

        saved = ApplyJob.objects.filter(seeker_id=sid)        

        apply_job = []

        for i in saved:
            apply_job.append(i.job_id.id)
        print('============',apply_job)
        like_data=[]

        liked = JobLike.objects.filter(seeker_id=sid)

        for i in liked:
            like_data.append(i.job_id.id)

        context={
            'uid':uid,
            'sid':sid,
            'apply_job':apply_job,
            'like_data':like_data,
            'j_all':j_all
        }
        return render(request,"Seeker/s-save-all-jobs.html",{'context':context})
    else:
        return redirect('sign-in')

def s_all_projects(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        p_all = Project.objects.all()                                                               
        
        view_sid = SavedProject.objects.filter(seeker_id = sid)

        # print(p_all)
        # print(view_sid)
        
        saved = SavedProject.objects.filter(seeker_id = sid, status="Saved")
        # print("----------->SAVED",saved)
        # print("------------>projects",p_all)
        
        saved_data = []

        for s in saved:
            saved_data.append(s.project_id.id)

        liked = ProjectLike.objects.filter(seeker_id = sid)

        liked_data = []
            
        for l in liked:
            liked_data.append(l.project_id.id)
        
         
        bid_pro = []

        bid_p = ProjectBid.objects.all()        

        for i in bid_p:
            bid_pro.append(i.project_id.id)


        #print("---> saved_data",saved_data)

        # for p in p_all:
        #     if p.id in saved_data:
        #         print("saved")
        #     else:
        #         print("NOT SAVED")

        context = {
            'uid':uid,
            'sid':sid,
            'p_all':p_all,
            'view_sid':view_sid,
            'saved_data':saved_data,
            'liked_data':liked_data,
            'bid_pro':bid_pro,
        }
        return render(request,"Seeker/s-all-projects.html",{'context':context})
    else:
        return redirect('sign-in')

@csrf_exempt
def save_project(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        p_id = request.POST['id']
        iddata = request.POST['iddata']
        pid = Project.objects.get(id = p_id)
        print('----',pid)
        pall = SavedProject.objects.filter(project_id = pid, seeker_id=sid)
        print('=======',pall)
        a=0
        if pall:
            a=1
            pall.delete()
        else:
            spid = SavedProject.objects.create(project_id = pid, seeker_id = sid)
        return JsonResponse({'a':a,'iddata':iddata})
    else:
        return redirect('sign-in')

@csrf_exempt
def saved_project(request):
    if "email" in request.session:
        # print('=*******')
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        p_id = request.POST['id']
        mydata = request.POST['mydata']
        project_id = SavedProject.objects.filter(id=p_id,seeker_id = sid)

        a=0
        if project_id:
           
            if(project_id[0].status == "Saved"):
                a=1
                project_id[0].status = "Unsaved"
                project_id[0].save()
            elif(project_id[0].status == "Unsaved"):
                project_id[0].status = "Saved"
                project_id[0].save()
        else:
            project_id = SavedProject.objects.create(project_id=p_id, seeker_id=sid)
        return JsonResponse({'a':a,'mydata':mydata})
    else:
        return redirect('sign-in')

@csrf_exempt  
def project_like(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        id = request.POST['id']
        mylike = request.POST['mylike']
        pid = Project.objects.get(id=id)
        p_like = ProjectLike.objects.filter(project_id = pid, seeker_id = sid)

        a=0
        if p_like:  
            a=1
            p_like.delete()
        else:
            name = pid.p_post
            value = "Your like on "+name+" from Projects" 
            nid = Notification.objects.create(seeker_id=sid,value=value)
            p_like = ProjectLike.objects.create(project_id = pid, seeker_id = sid)
        
        return JsonResponse({'a':a,'mylike':mylike})

    else:
        return redirect('sign-in')    

@csrf_exempt
def ps_like(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        sid = Seeker.objects.get(user_id=uid)
        id=request.POST['id']
        mydata=request.POST['mydata']
        psid = SavedProject.objects.get(id=id)
        pro_id = psid.project_id


        p_like = ProjectLike.objects.filter(project_id=pro_id,seeker_id=sid)

        a=0
        if p_like:
            a=1
            p_like.delete()
        else:
            pname = pro_id.p_post
            value = "Your like on "+pname+" from Saved Projects"
            nid = Notification.objects.create(seeker_id=sid,value=value)
            p_like = ProjectLike.objects.create(project_id=pro_id,seeker_id=sid)

        return JsonResponse({'a':a,'mydata':mydata})
    
    else:
        return redirect('sign-in')


@csrf_exempt  
def bid_project(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        
        id = request.POST['id']
        mydata = request.POST['mydata']
        pid = Project.objects.get(id = id)
        p_bid = ProjectBid.objects.filter(project_id=pid,seeker_id=sid)

        if p_bid:
            pass
        else:
            pname = pid.p_post
            value = "You Successfully Applied for "+pname+" from Projects"
            nid = Notification.objects.create(seeker_id=sid,value=value)
            p_bid = ProjectBid.objects.create(project_id = pid, seeker_id=sid)
        
        return JsonResponse({'msg':'success'})

    else:
        return redirect('sign-in')

@csrf_exempt
def bid_sproject(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        sid = Seeker.objects.get(user_id=uid)

        ps_id = SavedProject.objects.get(id=request.POST['id'])
        p_id = ps_id.project_id 
        print('===============',p_id)

        p_bid = ProjectBid.objects.filter(project_id=p_id,seeker_id=sid)

        if p_bid:
            pass
        else:
            pname = ps_id.project_id.p_post
            value = "You Successfully Applied for "+pname+" from Saved Projects"
            nid = Notification.objects.create(seeker_id=sid,value=value)
            p_bid = ProjectBid.objects.create(project_id=p_id,seeker_id=sid)

        return JsonResponse({'msg':'success'})
    
    else:
        return redirect('sign-in')

def save_all_project(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
        p_all = SavedProject.objects.filter(seeker_id = sid, status='Saved')

        p_like = ProjectLike.objects.filter(seeker_id=sid)

        liked_data = [] 

        for i in p_like:
            liked_data.append(i.project_id.id)

        bid_pro = []
        b_all = ProjectBid.objects.all()

        for i in b_all:
            bid_pro.append(i.project_id.id)

        print('============================',bid_pro)

        context={
            'uid':uid,
            'sid':sid,
            'liked_data':liked_data, 
            'p_all':p_all,
            'bid_pro':bid_pro,
        }
        return render(request,"Seeker/s-save-all-projects.html",{'context':context})
    else:
        return redirect('sign-in')

def com_all(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)

        c_all = Company.objects.all()

        s_follow = []

        c_follow = Following.objects.filter(seeker_id=sid)

        for i in c_follow:
            s_follow.append(i.company_id.id)
        
        print('==================',s_follow)

        context={
            'uid':uid,
            'sid':sid,
            's_follow':s_follow,
            'c_all':c_all,
        }

        return render(request,"Seeker/companies.html",{'context':context})
    else:
        return redirect('sign-in')

@csrf_exempt
def p_comment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.filter(user_id=uid)
        s_id = list(sid.values())
        id = request.POST['id']
        cbox = request.POST['cbox']
        ask = request.POST['ask']
        pid = Project.objects.get(id=id)
        # print('================',pid)
        # print('=============',sid)
        p_comment = Comment.objects.filter(project_id=pid)
        # print('=======================',p_comment[0].seeker_id.s_pic)

        pro=[]
        for i in p_comment:
            pro.append(i.value)

        seek=[]
        for i in p_comment:
            seek.append(i.seeker_id.sname)
        pcomm = list(p_comment.values())

        return JsonResponse({'cbox':cbox,'ask':ask,'pcomm':pcomm,'pro':pro,'seek':seek})
    
    else:
        return redirect('sign-in')

@csrf_exempt
def send_comm(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        sid = Seeker.objects.get(user_id=uid)
        cbox = request.POST['cbox']
        intext = request.POST['intext']
        pid = Project.objects.get(id=request.POST['id'])        
        mess = request.POST['mess']
        pname = pid.p_post
        value = "Your Comment on "+pname+" from Projects"
        nid = Notification.objects.create(seeker_id=sid,value=value)

        p_comm = Comment.objects.create(project_id=pid,seeker_id=sid,value=mess)
        return JsonResponse({'cbox':cbox,'intext':intext})
    else:
        return redirect('sign-in')


@csrf_exempt
def ps_comment(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        sid = Seeker.objects.get(user_id=uid)

        id = request.POST['id']
        cbox = request.POST['cbox']
        ask = request.POST['ask']
        psid = SavedProject.objects.get(id=id)
        pid = psid.project_id.id
        p_id = Project.objects.get(id=pid)
        p_all = Comment.objects.filter(project_id=p_id)
        p_comm = list(p_all.values())

        seek=[]

        for i in p_all:
            seek.append(i.seeker_id.sname)

        return JsonResponse({'p_comm':p_comm,'ask':ask,'seek':seek})

    else:
        return redirect('sign-in')

@csrf_exempt
def ps_send_com(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id=uid)
        cbox = request.POST['cbox']
        mess_id = request.POST['mid']
        mess = request.POST['mess']
        ps_id = SavedProject.objects.get(id=request.POST['id'])
        pid = ps_id.project_id.id
        p_id = Project.objects.get(id=pid)

        p_comm = Comment.objects.create(project_id=p_id,seeker_id=sid,value=mess)

        pname = p_id.p_post
        value = "Your Comment on "+pname+" from Saved Projects"
        nid = Notification.objects.create(seeker_id=sid,value=value)

        return JsonResponse({'cbox':cbox,'mess_id':mess_id})

    else:
        return redirect('sing-in')

@csrf_exempt
def j_comment(request):
    if "email" in request.session:
        jid = Job.objects.get(id = request.POST['id'])
        ask = request.POST['ask']

        j_comm = Jcomment.objects.filter(job_id=jid)
        
        print('=======================',j_comm)
        seek=[]
        for i in j_comm:
            seek.append(i.seeker_id.sname)
        # print('====================',seek)
        j_comm = list(j_comm.values())

        return JsonResponse({'ask':ask,'j_comm':j_comm,'seek':seek})

    else:
        return redirect('sign-in')

@csrf_exempt
def j_send_comment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id=uid)
        cbox = request.POST['cbox']
        mess_id = request.POST['mid']
        mess = request.POST['mess']
         
        jid = Job.objects.get(id=request.POST['id'])

        j_comm = Jcomment.objects.create(job_id=jid,seeker_id=sid,value=mess)

        return JsonResponse({'cbox':cbox,'mess_id':mess_id})

    else:
        return redirect('sing-in')

@csrf_exempt
def c_follow(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id=uid)

        myfollow = request.POST['myfollow']
        cid = Company.objects.get(id=request.POST['id'])

        c_follow = Following.objects.filter(seeker_id=sid,company_id=cid)

        status="true"
        if c_follow:
            status="false"
            c_follow.delete()
        else:
            c_follow = Following.objects.create(seeker_id=sid,company_id=cid)

        return JsonResponse({'status':status,'myfollow':myfollow})
    
    else:
        return redirect('sign-in')

def page(request):
    return render(request,"Seeker/my-profile-feed.html")


@csrf_exempt
def search(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)
    
        val = request.POST['search']
        cname = Company.objects.filter(cname=val)
    
        s_follow = []

        c_follow = Following.objects.filter(seeker_id=sid)

        for i in c_follow:
            s_follow.append(i.company_id.id)
        
        context={
            'uid':uid,
            'sid':sid,
            's_follow':s_follow,
            'cname':cname,
        }

        return render(request,"Seeker/s-search.html",{'context':context})

    else:
        return redirect('sign-in')

def change_pass(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)

        cpass = request.POST['cpassword']

        if uid.password==cpass:
            npass = request.POST['npassword']
            uid.password = npass
            uid.save()
        else:
            pass

        return redirect('s-profile')

    else:
        return redirect('sign-in')

def change_img(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id = uid)

        cprofle = request.FILES['cprofle']
        sid.s_pic = cprofle
        sid.save()

        return redirect('s-profile')

    else:
        return redirect('sign-in')

def notification(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        sid = Seeker.objects.get(user_id=uid)

        n_all = Notification.objects.filter(seeker_id=sid).order_by('created_at').reverse()

        context={
            'uid':uid,
            'sid':sid,
            'n_all':n_all
        }
        return render(request,"Seeker/notification.html",{'context':context})
    else:
        return redirect('sign-in')


def social_media(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        sid = Seeker.objects.get(user_id=uid)

        context={
            'ud':uid,
            'sid':sid,
        }
        return render(request,"Seeker/social-link.html",{'context':context})
    
    else:
        return redirect('sign-in')

def add_link(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        sid = Seeker.objects.get(user_id=uid)

        
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

        return redirect('social-media')

    else:
        return redirect('sign-in')

def del_account(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        sid = Seeker.objects.get(user_id=uid)

        if request.POST:
            try:

                uid = User.objects.get(email=request.POST['email'])
                password = request.POST['password']
                if uid:
                    if uid.password == password:
                        uid.delete()
                    else:
                        msg="password is wrong"
                        context={
                            'msg':msg,
                            'uid':uid,
                            'sid':sid,
                            }
                        return render(request,"Seeker/del-account.html",{'context':context})
                else:
                    msg="Email is wrong"

                    context={
                        'msg':msg,
                        'uid':uid,
                        'sid':sid,
                        }
                    return render(request,"Seeker/del-account.html",{'context':context})
            except:
                msg='Something is wrong'                
                context={
                        'msg':msg,
                        'uid':uid,
                        'sid':sid,
                        }
                return render(request,"Seeker/del-account.html",{'context':context})

        context={
            'uid':uid,
            'sid':sid,
        }
        return render(request,"Seeker/del-account.html",{'context':context})

    else:
        return redirect('sign-in')