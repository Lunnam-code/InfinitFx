from django.db import models
# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import uuid



class Referral(models.Model):
  referrer = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='referrals')
  referred_user = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE, related_name='referred_by')
  commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  is_paid = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.referrer.username} Referred {self.referred_user.username}"


class ReferralLink(models.Model):
  user = models.OneToOneField(to='accounts.User', on_delete=models.CASCADE, related_name='referral_link_user')
  link = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return f"Referral link for {self.user.email}"
    
  def get_absolute_url(self):
    return reverse('referral_link_detail', args=[str(self.user.email)])

  def save(self, *args, **kwargs):
    if not self.link:
        self.link = self.generate_unique_link()
    super().save(*args, **kwargs)

  # def generate_unique_link(self):
  #   from accounts.models import User
  #   return User.objects.make_random_password(length=8)
  
  def generate_unique_link(self):
    # Use user information to create a unique referral link
    unique_info = f"{self.user.username}{uuid.uuid4().hex[:6]}"
    return unique_info


# @receiver(post_save, sender=User)
# def create_referral_link(sender, instance, created, **kwargs):
#   if created:
#     ReferralLink.objects.create(user=instance, link=generate_referral_link(instance))

# def generate_referral_link(user):
#   # Logic to generate a unique referral link
#   return f"http://yourwebsite.com/register?ref={user.referral_link.link}"
