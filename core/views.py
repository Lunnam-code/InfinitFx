from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from . models import Inbox


from decimal import Decimal, getcontext
from django.utils import timezone
from .models import Investment, Deposit

def index(request):
  return render(request, 'index.html')


def support(request):
  if request.method == 'POST':
    name = request.POST['full_name']
    email = request.POST['full_email']
    subject = request.POST['full_subject']
    message = request.POST['full_message']
    
    inbox = Inbox(name=name,email=email,subject=subject,message=message)
    
    try:
      subject = 'New Inquery From InfiniteFx'
      message = 'You have new inquery from ' + name + '. Please login to to your admin dashboard to see more info.'
      from_email = settings.DEFAULT_FROM_EMAIL
      to_email = ['lukendblog@gmail.com']

      send_mail(subject,message,from_email,to_email, fail_silently=False)


      inbox.save()
      return JsonResponse({'success': True, 'message': 'Message Sent. We will get back to you soon!'})
    except Exception as e:
      # Handle other errors (if any)
      return JsonResponse({'success': False, 'error_code': 'unknown_error', 'message': 'An error occurred: ' + str(e)})
  else:
    return render(request, 'support.html')

def contact(request):
  if request.method == 'POST':
    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']
    print(name)
    print(subject)
    print(email)
    inbox = Inbox(name=name,email=email,subject=subject,message=message)
    

    subject = 'New Inquery From InfiniteFxForexSolution'
    message = 'You have new inquery from ' + name + '. Please login to to your admin dashboard to see more info.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [settings.DEFAULT_FROM_EMAIL]

    send_mail(subject,message,from_email,to_email, fail_silently=False)


    inbox.save()
    return HttpResponse('Message Sent. We will get back to you soon!')
  
def about(request):
  return render(request, 'about.html')

def faq(request):
  return render(request, 'faq.html')

def policy(request):
  return render(request, 'policy.html')



def calculate_profit(deposit_id):
    try:
        deposit = Deposit.objects.get(pk=deposit_id)
        investments = Investment.objects.filter(deposit=deposit, status=Investment.STATUS_ACTIVE)

        if not investments.exists():
            return  # No active investments for this deposit

        getcontext().prec = 6

        for investment in investments:
            current_time = timezone.now()
            interest_rate = Decimal(investment.plan.profit_percentage) / 100
            duration = investment.plan.maturity_duration_hours
            every_three_minutes_increment = (duration * 60) / 3

            mature_hour = current_time - timezone.timedelta(hours=duration)

            if investment.created_at < mature_hour:
                investment.status = Investment.STATUS_COMPLETED
                investment.save()
            else:
                earnings_increment = Decimal(investment.deposit.amount) * interest_rate / Decimal(every_three_minutes_increment)
                investment.earnings += earnings_increment
                investment.save()

    except (Deposit.DoesNotExist, Investment.DoesNotExist) as e:
        print(f"Error in calculate_profit task: {e}")





  
