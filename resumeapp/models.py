from django.db import models
from PIL import Image

# Create your models here.

from django.db import models
from PIL import Image


class tbl_register(models.Model):
    email = models.EmailField(max_length=100)
    phn = models.CharField(max_length=15, default="")
    name = models.CharField(max_length=100, default="")
    uname = models.CharField(max_length=100, default="")
    pswd = models.CharField(max_length=255, default="")
    
    adrs = models.CharField(max_length=255, default="")
    gender = models.CharField(max_length=20, default="")
    dob = models.DateField(null=True, blank=True)
    
    qualification = models.CharField(max_length=100, default="")
    plc = models.CharField(max_length=100, default="")
    
    utype = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=20, default="")
    
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_pic:
            img = Image.open(self.profile_pic.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)           

    
class tbl_jobdetails(models.Model):
    company = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    jobtitle = models.CharField('jobtitle', max_length=100)
    jobtype = models.CharField('jobtype', max_length=100)
    jobvacancy = models.CharField('jobvacancy', max_length=100)
    jobdate1 = models.DateField()
    jobdate2 = models.DateField()
    jobexp1 = models.CharField('jobexp1', max_length=100)
    jobexp2 = models.CharField('jobexp2', max_length=100)
    joblocation = models.CharField('joblocation', max_length=100)
    jobskills = models.CharField(default="", max_length=1000)
    jobdescription = models.CharField('jobdescription', max_length=1000)
    
    # jobdescription = models.FileField(upload_to='desc/')

    
class tbl_userresume(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    experience = models.CharField('experience', max_length=100)
    resume = models.FileField(upload_to='resume')
    
class tbl_userresume2(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    experience = models.CharField('experience', max_length=100)
    resume1 = models.FileField(upload_to='file/file1/')



class tb_skill(models.Model):
    skill = models.TextField()
    user_id=models.ForeignKey(tbl_register,on_delete=models.CASCADE,blank=True,null=True)
    
    
class tbl_user_apply_job(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    resume= models.ForeignKey(tbl_userresume2, on_delete=models.CASCADE, blank=True, null=True)
    job= models.ForeignKey(tbl_jobdetails, on_delete=models.CASCADE, blank=True, null=True)
    status=models.CharField(max_length=100,default="applied")
    notification_sent = models.BooleanField(default=False)
    
class tbl_notification(models.Model):
    application = models.ForeignKey(tbl_user_apply_job, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50)
    message = models.TextField()



class AIResumeScreening(models.Model):
    application = models.OneToOneField(
        tbl_user_apply_job,
        on_delete=models.CASCADE,
        related_name='ai_screening'
    )

    match_score = models.FloatField(default=0)
    semantic_score = models.FloatField(default=0)
    skill_score = models.FloatField(default=0)

    matched_skills = models.TextField(blank=True, null=True)
    missing_skills = models.TextField(blank=True, null=True)

    recommendation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application} - {self.match_score}%"

    