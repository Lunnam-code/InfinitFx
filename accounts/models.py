from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from referral_system.models import Referral, ReferralLink



class MyAccountManager(BaseUserManager):
  def create_user(self, first_name, last_name, username, email, password=None):
    if not email:
      raise ValueError('User must have an email address')
    
    if not username:
      raise ValueError('User must have username')
    
    user = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name
    )
    
    user.set_password(password)
    user.save(using = self._db)
    return user
  
  def create_superuser(self, first_name, last_name, email, username, password):
    user = self.create_user(
      email = self.normalize_email(email),
      username = username,
      password = password,
      first_name = first_name,
      last_name = last_name,
    )
    user.is_admin = True
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    # user.is_superadmin = True
    user.save(using=self._db)
    return user



class User(AbstractBaseUser, PermissionsMixin):
  CLIENT = 'client'
  AGENT = 'agent' 
  MANAGER = 'manager'
  
  ROLES_CHOICES = (
    (CLIENT, 'client'),
    (AGENT, 'agent'),
    (MANAGER, 'manager'),
  ) 
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
  first_name    = models.CharField(max_length=50)
  last_name     = models.CharField(max_length=50)
  username      = models.CharField(max_length=50, unique=True)
  email         = models.EmailField(unique=True)
  account_balance =models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  phone_number  = models.CharField(max_length=50)
  profile_image         = models.ImageField(blank=True, null=True, upload_to='images/users/')
  role          = models.CharField(max_length=30, choices=ROLES_CHOICES, default=CLIENT)
  country       = models.CharField(max_length=50)
  btc_wallet   = models.CharField(max_length=300, blank=True)
  
  referral = models.ForeignKey(Referral, on_delete=models.SET_NULL, null=True, blank=True)
  referral_link = models.OneToOneField(ReferralLink, on_delete=models.SET_NULL, null=True, blank=True,  related_name='user_referral_link')
  agree_to_terms_and_condition = models.BooleanField(default=False)
  total_earned_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  earning = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  pending_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  
  # required 
  date_joined   = models.DateTimeField(auto_now_add=True)
  last_login    = models.DateTimeField(auto_now_add=True)
  is_admin      = models.BooleanField(default=False)
  is_staff      = models.BooleanField(default=False)
  is_active     = models.BooleanField(default=True)
  # is_superadmin = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  
  objects = MyAccountManager()
  
  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None):
    # return self.is_admin
    return True
  
  def has_module_perm(self, add_label):
    return True
  
  class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'
    app_label = 'accounts'











