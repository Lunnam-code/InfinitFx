from django.shortcuts import render, redirect
from . models import User
from django.http import HttpResponse

from django.contrib import messages
from django.http import JsonResponse

from django.contrib import messages, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from core.models import Deposit


import requests

def dashboard(request):
  user = request.user
  deposit = Deposit.objects.filter(user=user)
  context = {
    'deposit':deposit,
  }
  return render(request, 'accounts/dashboardpages/dashboard.html',context)

def deposite(request):
  if request.method == 'POST':
    amount = int(request.POST['amount'])
    
    if 50 <= amount <= 299:
      plan_name = 'Standard'
      plan_duration = 12
      profit_percentage = '5%'
    elif 300 <= amount <= 999:
      plan_name = 'Business'
      plan_duration = 24
      profit_percentage = '9%'
    elif 1000 <= amount <= 4999:
      plan_name = 'Professional'
      plan_duration = 48
      profit_percentage = '13%'
    elif amount >= 5000:
      plan_name = 'Enterprise'
      plan_duration = 72
      profit_percentage = '17%'
      
    
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    bitcoin_rate = float(response.json()['bpi']['USD']['rate'].replace(',', ''))
    bitcoin_equivalent = round(amount / bitcoin_rate, 8)
    
    context = {
      'amount':amount,
      'bitcoin_equivalent':bitcoin_equivalent,
      'plan_name':plan_name,
      'plan_duration':plan_duration,
      'profit_percentage':profit_percentage,
    }
    return render(request, 'accounts/dashboardpages/invest.html', context)
  else:
    return render(request, 'accounts/dashboardpages/deposite.html')

def invest(request):
  if request.method == 'POST':
    amount = int(request.POST['amount'])
    
    deposit_amount = Deposit.objects.create(amount=amount, user=request.user)
    deposit_amount.save()
    messages.success(request, 'Deposit pending for approval')
    return redirect('dashboard')
  else:
    return render(request, 'accounts/dashboardpages/invest.html')

def withdraw(request):
  return render(request, 'accounts/dashboardpages/withdraw.html')

def register(request):
  if request.user.is_authenticated:
    return redirect('index')
  elif request.method == 'POST':
    fname = request.POST['fname']
    lname = request.POST['lname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    hashed_password = make_password(password)
    country = request.POST['country']
    pay_account = request.POST['pay_account']
    agree = request.POST['agree']
    
    # check if email eist 
    useremail = User.objects.filter(email=email).exists()
    user_username = User.objects.filter(username=username).exists()
    if useremail:
      return JsonResponse({'success': False, 'error_code': 'Email_exist', 'message': 'Email Already exists'})
    elif user_username:
      return JsonResponse({'success': False, 'error_code': 'Username_taken', 'message': 'Username has been taken'})
    else:
      user = User.objects.create( first_name=fname,last_name=lname,username=username,email=email,password=hashed_password,country=country,btc_wallet=pay_account,agree_to_terms_and_condition=True)
      user.save()
      return JsonResponse({'success': True, 'message': 'Account Created successful'})
  else:
    return render(request, 'accounts/register.html')
  

def login(request):
  if request.user.is_authenticated:
    return redirect('index')
  elif request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
      user = auth.authenticate(email=email,password=password) 
      if user is not None:
        # User authentication successful
        auth.login(request, user)
        return JsonResponse({'success': True, 'message': 'Login successful'})
      else:
        # User authentication failed
        return JsonResponse({'success': False, 'error_code': 'invalid_credentials', 'message': 'Invalid username or password'})
    except Exception as e:
        # Handle other errors (if any)
        return JsonResponse({'success': False, 'error_code': 'unknown_error', 'message': 'An error occurred: ' + str(e)})
  else:
    return render(request, 'accounts/login.html')


@login_required(login_url = 'signin')
def signout(request):
  auth.logout(request)
  messages.success(request, 'You have logged out!')
  return redirect('index')

def forgotPassword(request):
  if request.method == 'POST':
    email = request.POST['email']
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email__exact=email)
      
      current_site = get_current_site(request)
      mail_subject = 'Reset Password'
      message = render_to_string('accounts/reset_password_email.html',{
          'user':user,
          'domain':current_site,
          'uid':urlsafe_base64_encode(force_bytes(user.pk)),
          'token':default_token_generator.make_token(user)
      })
      to_email = email
      send_email = EmailMessage(
        mail_subject,
        message, 
        from_email = settings.DEFAULT_FROM_EMAIL,
        to=[to_email])
      send_email.content_subtype = 'html'
      send_email.send()
      # once the email is send 
      messages.success(request,'Password reset email has been sent to your email address!')
      return redirect('login')
    else:
      messages.error(request,'Email those not exist')
      return redirect('forgotPassword')
  else:
    return render(request, 'accounts/forgot-password.html')

def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError, User.DoestNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid #save uid inside session, so that i can access this session when reseting the password
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('login')

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            
            uid = request.session.get('uid')#get uid from session we save above
            user = User.objects.get(pk=uid)#get user
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successful')
            return redirect('login')
        else:
            messages.error(request,'Password does not match')
            return redirect('restpassword')
    else:
        return render(request, 'accounts/reset_passward.html')

