from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    
    departments=[('Cardiologist','Cardiologist'),
    ('Dermatologists','Dermatologists'),
    ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
    ('Allergists/Immunologists','Allergists/Immunologists'),
    ('Anesthesiologists','Anesthesiologists'),
    ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20,unique=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['phone','first_name','last_name']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='patients', default='default.png')
    address = models.CharField(max_length=40)
    

    def __str__(self):
        return self.user.username


class PatientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.ImageField()
    symptoms = models.TextField(null=False)
    status=models.BooleanField(default=False)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    converted_date = models.DateTimeField(null=True, blank=True)

    objects = PatientManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def handle_upload_follow_ups(instance, filename):
    return f"patient_followups {instance.lead.pk}/{filename}"


class FollowUp(models.Model):
    patient = models.ForeignKey(Patient, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name}"


class Agent(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30)  # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)

























# from django.db import models
# from django.db.models.signals import post_save
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.utils.translation import ugettext_lazy as _

# class UserManager(BaseUserManager):
#     """Define a model manager for User model with no username field."""

#     use_in_migrations = True

#     def _create_user(self, email, phone, password, **extra_fields):
#         """Create and save a User with the given email and password."""
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         """Create and save a regular User with the given email and password."""
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         """Create and save a SuperUser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(email, password, **extra_fields)
 
    
# class User(AbstractUser):
#     """User model."""
#     username = None
#     phone = models.CharField(max_length = 256, unique=True, null=True)
#     email = models.EmailField(_('email address'), unique=True)
#     first_name= models.CharField(max_length=50,null=True,blank=True)
#     last_name= models.CharField(max_length=50,null=True,blank=True)
#     # is_organisor = models.BooleanField(default=True)
#     # is_agent = models.BooleanField(default=False)



    
    
    

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(default="no bio...")
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return f" {self.user.first_name} {self.user.last_name} "


# class PatientManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset()


# class Patient(models.Model):   
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     address = models.CharField(max_length=40)
#     symptoms = models.TextField(null=False)
#     assignedDoctorId = models.PositiveIntegerField(null=True)
#     date_added=models.DateTimeField(auto_now_add=True)
#     status=models.BooleanField(default=False)
#     # category = models.ForeignKey("Category", related_name="patients", null=True, blank=True, on_delete=models.SET_NULL)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
#     def __str__(self):
#         return self.user.first_name+" ("+self.symptoms+")"
#     objects = PatientManager()
#     # first_name = models.CharField(max_length=20)
#     # last_name = models.CharField(max_length=20)
#     # address = models.TextField(null=True, blank=True)
#     # age = models.IntegerField(default=0)
#     # blood_group = models.CharField(max_length=10,blank=True)
#     # geno_type = models.CharField(max_length=10, blank=True)
#     # organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     # agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
#     # category = models.ForeignKey("Category", related_name="patients", null=True, blank=True, on_delete=models.SET_NULL)
#     # description = models.TextField(null=True, blank=True)
#     # date_added = models.DateTimeField(auto_now_add=True)
#     # email = models.EmailField()
#     # profile_picture = models.ImageField(upload_to='patients', default='default.png')
#     # converted_date = models.DateTimeField(null=True, blank=True)

#     # objects = PatientManager()

#     # def __str__(self):
#     #     return f"{self.first_name} {self.last_name}"


# # def handle_upload_follow_ups(instance, filename):
# #     return f"patient_followups/patient_{instance.patient.pk}/{filename}"


# # class FollowUp(models.Model):
# #     patient = models.ForeignKey(Patient, related_name="followups", on_delete=models.CASCADE)
# #     date_added = models.DateTimeField(auto_now_add=True)
# #     notes = models.TextField(blank=True, null=True)
# #     file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

# #     def __str__(self):
# #         return f"{self.patient.first_name} {self.patient.last_name}"


# departments=[('Cardiologist','Cardiologist'),
# ('Dermatologists','Dermatologists'),
# ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
# ('Allergists/Immunologists','Allergists/Immunologists'),
# ('Anesthesiologists','Anesthesiologists'),
# ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
# ]

# class Agent(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=40)
#     department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
#     status=models.BooleanField(default=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
#     def __str__(self):
#         return "{} ({})".format(self.user.first_name,self.department)
    
#     # organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

#     # def __str__(self):
#     #     return self.user.email


# class Appointment(models.Model):
#     patientId=models.PositiveIntegerField(null=True)
#     doctorId=models.PositiveIntegerField(null=True)
#     patientName=models.CharField(max_length=40,null=True)
#     doctorName=models.CharField(max_length=40,null=True)
#     appointment_date=models.DateField(auto_now=True)
#     description=models.TextField(max_length=500)
#     status=models.BooleanField(default=False)


# class PatientDischargeDetails(models.Model):
#     patientId=models.PositiveIntegerField(null=True)
#     patientName=models.CharField(max_length=40)
#     assignedDoctorName=models.CharField(max_length=40)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=True)
#     symptoms = models.CharField(max_length=100,null=True)

#     admitDate=models.DateField(null=False)
#     releaseDate=models.DateField(null=False)
#     daySpent=models.PositiveIntegerField(null=False)

#     roomCharge=models.PositiveIntegerField(null=False)
#     medicineCost=models.PositiveIntegerField(null=False)
#     doctorFee=models.PositiveIntegerField(null=False)
#     OtherCharge=models.PositiveIntegerField(null=False)
#     total=models.PositiveIntegerField(null=False)

# # class Category(models.Model):
# #     name = models.CharField(max_length=30)  # New, Contacted, Converted, Unconverted
# #     organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

# #     def __str__(self):
# #         return self.name


# def post_user_created_signal(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


# post_save.connect(post_user_created_signal, sender=User)
















# # class Patients(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     age = models.IntegerField(default=0)
# #     blood_group = models.CharField(max_length=10,blank=True)
# #     geno_type = models.CharField(max_length=10, blank=True)
# #     address = models.TextField()
# #     phone_number = models.CharField(max_length=20)
# #     img = models.ImageField(upload_to='patients', default='default.png')
# #     date_added = models.DateTimeField(auto_now_add=True)
# #     updated = models.DateTimeField(auto_now=True)
     
# #     def __str__(self):
# #         return f"{self.user.username}"

# # # Create your models here.
