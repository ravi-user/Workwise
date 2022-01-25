from django.db import models
from Company.models import *
import math
from django.utils import timezone


# Create your models here.

class Seeker(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    sname = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    s_pic = models.FileField(upload_to="media/images")

    def __str__(self):
        return self.sname


class Project(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    p_post = models.CharField(max_length=50)
    pduration = models.CharField(max_length=50)
    pdesc = models.TextField(max_length=1000)
    salary_start = models.CharField(max_length=50)
    salary_end = models.CharField(max_length=50)
    ptags = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.company_id.cname + " "+ self.p_post

    def ViewTags(self):
        return self.ptags.split(',')
     
    def LikeProjectCount(self):
        pcount = ProjectLike.objects.filter(project_id = self.id).count()

        if pcount>1:
            return str(pcount)+" Likes"
        else:
            return str(pcount)+" Like"

    def whenpublished(self):

        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Job(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    jpost = models.CharField(max_length=50)
    jduration = models.CharField(max_length=50)
    jdesc = models.TextField(max_length=1000)
    jsalary = models.CharField(max_length=50)
    jtags = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.company_id.cname + " "+ self.jpost
    
    def ViewTags(self):
        return self.jtags.split(',')

    def LikeJobCount(self):
        jcount = JobLike.objects.filter(job_id=self.id).count()

        if jcount>1:
            return str(jcount)
        else:
            return str(jcount)
 

    def whenpublished(self):

        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

class JobLike(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.job_id.jpost+" "+self.seeker_id.sname

class SavedJob(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Saved')
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def LikeJobCount(self):
        jcount = JobLike.objects.filter(job_id = self.job_id).count()

        if jcount>1:
            return str(jcount)+" Likes"
        else:
            return str(jcount)+" Like"

    def _str__(self):
        return self.job_id.jpost+" "+ self.seeker_id.sname

    def whenpublished(self):

        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

class SavedProject(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Saved')
    created_at = models.DateTimeField(auto_now_add=True, blank=False)


    def __str__(self):
        return self.project_id.p_post+" "+ self.seeker_id.sname

    def LikeProjectCount(self):
        pcount = ProjectLike.objects.filter(project_id = self.project_id).count()

        if pcount>1:
            return str(pcount)+" Likes"
        else:
            return str(pcount)+" Like"

    def whenpublished(self):

        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

class ProjectLike(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
 
    def __str__(self):
        return self.project_id.p_post+" "+self.seeker_id.sname

class ProjectBid(models.Model):
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.project_id.p_post+" "+self.seeker_id.sname

class ApplyJob(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.job_id.jpost+" "+ self.seeker_id.sname

class Following(models.Model):
    seeker_id = models.ForeignKey(Seeker,on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.seeker_id.sname+" "+self.company_id.cname

class Comment(models.Model):
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker,on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.seeker_id.sname+" "+self.project_id.p_post

class Jcomment(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker_id = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.seeker_id.sname+" "+self.job_id.jpost

class Link(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    facebook = models.CharField(max_length=100, null=True,blank=True)
    twitter = models.CharField(max_length=100, null=True,blank=True)
    pinterest = models.CharField(max_length=100, null=True,blank=True)
    instagram = models.CharField(max_length=100, null=True,blank=True)
    youtube = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return self.user_id.email

class Notification(models.Model):
    seeker_id = models.ForeignKey(Seeker,models.CASCADE)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)

    def __str__(self):
        return self.seeker_id.sname

    def whenpublished(self):
        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"