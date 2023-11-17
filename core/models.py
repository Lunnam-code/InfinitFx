from django.db import models
from django.utils import timezone

from decimal import Decimal
from django.urls import reverse
from accounts.models import User
from . tasks import scheduler, update_earnings
from datetime import datetime


class Inbox(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  subject = models.CharField(max_length=100)
  message = models.TextField(max_length=3000)
  sent_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    verbose_name = 'Inbox'
    verbose_name_plural = 'Inbox'
        
  def __str__(self):
    return self.name
  
  
class Plan(models.Model):
  name = models.CharField(max_length=50)
  maturity_duration_hours = models.IntegerField() 
  profit_percentage = models.DecimalField(max_digits=5, decimal_places=2)

  def __str__(self):
    return self.name

class Deposit(models.Model):
  PENDING = 'pending'
  APPROVED = 'approved'
  CANCELED = 'canceled'

  STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (CANCELED, 'Canceled'),
  )

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  amount = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

  def __str__(self):
    return f"Deposit of {self.amount} by {self.user.email}, Status: {self.get_status_display()}"

  def create_investment(self):
    if self.status == Deposit.APPROVED:
      if 20 <= self.amount <= 49:
        plan_name = 'Testing'
      elif 50 <= self.amount <= 299:
          plan_name = 'Standard'
      elif 300 <= self.amount <= 999:
          plan_name = 'Business'
      elif 1000 <= self.amount <= 4999:
          plan_name = 'Professional'
      else:
          plan_name = 'Enterprise'

      # Get the Plan object based on the plan name
      plan = Plan.objects.get(name=plan_name)

      maturity_duration = plan.maturity_duration_hours

      maturity_date = self.created_at + timezone.timedelta(hours=maturity_duration)
      investment = Investment.objects.create(
          user=self.user,
          deposit=self,
          profit=0,  
          created_at=timezone.now(),
          maturity_duration_hour=maturity_duration,
          plan=plan,  # 
          status=Investment.STATUS_ACTIVE 
      )
      investment.save()
      
      job_id = f"update_earnings_{investment.id}"
      scheduler.add_job(
        update_earnings,
        trigger="interval",
        minutes=3,
        args=[investment.id, datetime.now()],
        jobstore='default',
        replace_existing=True,
        id=job_id,
      )
      investment.job_id = job_id
      investment.save()
      
      user = User.objects.get(pk=self.user.pk)  
      user.account_balance += self.amount  
      user.save()
      

class Investment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  deposit = models.OneToOneField(Deposit, on_delete=models.CASCADE)
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
  profit = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  maturity_duration_hour = models.IntegerField()
  job_id = models.CharField(max_length=255, blank=True, null=True)

  STATUS_ACTIVE = 'active'
  STATUS_COMPLETED = 'completed'
  STATUS_CHOICES = [
    (STATUS_ACTIVE, 'Active'),
    (STATUS_COMPLETED, 'Completed'),
  ]
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
            
  def get_absolute_url(self):
      return reverse('investment_detail', args=[str(self.id)])

  def __str__(self):
        return f"Investment for {self.user.email} - {self.deposit.amount} Plan"



