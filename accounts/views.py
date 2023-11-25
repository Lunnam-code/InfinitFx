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
from core.models import Deposit, Withdraw, Investment
from referral_system.models import ReferralLink, Referral
from decimal import Decimal
from django.db.models import Q

import requests

@login_required(login_url = 'login')
def dashboard(request):
  user = request.user
  # user_details = User.objects.get(id=user.id)
  deposit = Deposit.objects.filter(user=user)
  withdrawal = Withdraw.objects.filter(user=user).order_by('-created_at')
  active_investment =  Investment.objects.filter(user=user, status='active')
  context = {
    # 'user_details':user_details,
    'deposit':deposit,
    'withdrawal':withdrawal,
    'active_investment':active_investment,
  }
  return render(request, 'accounts/dashboardpages/dashboard.html',context)

@login_required(login_url = 'login')
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

@login_required(login_url = 'login')
def invest(request):
  if request.method == 'POST':
    amount = int(request.POST['amount'])
    
    deposit_amount = Deposit.objects.create(amount=amount, user=request.user)
    deposit_amount.save()
    messages.success(request, 'Deposit pending for approval')
    return redirect('dashboard')
  else:
    return render(request, 'accounts/dashboardpages/invest.html')

@login_required(login_url = 'login')
def withdraw(request):
  user_id = request.user.id
  pending_withdraw = 0
  if request.method == 'POST':
    amount = Decimal(request.POST['w-amount'])
    
    user = User.objects.get(id=user_id)
    if user.account_balance >= amount :
      user.account_balance -= amount
      user.save()
      
      make_withdraw = Withdraw.objects.create(
        user = request.user,
        amount = amount,
      ) 
      make_withdraw.save()
      
      messages.success(request, 'Pending Approval')
      return redirect('withdraw')
    else:
      messages.error(request, 'Insufficient Fund')
      return redirect('withdraw')
      
  else:
    withdraw_details = Withdraw.objects.filter(user=request.user,status= 'pending')
    for item in withdraw_details:
      pending_withdraw += item.amount
      
    data = {
      'pending_withdraw':pending_withdraw,
    }
    return render(request, 'accounts/dashboardpages/withdraw.html', data)

@login_required(login_url = 'login')
def referralfun(request):
  # ref_code = User.objects.get(id=request.user.id)
  return render(request, 'accounts/dashboardpages/referrals.html')

@login_required(login_url = 'login')
def deposit_list(request):
  Standard = 0
  Business = 0
  Professional = 0
  Enterprise = 0
  total = 0
  deposit_item = Deposit.objects.filter(user=request.user, status='approved')
  
  for item in deposit_item:
    if 50 <= item.amount <=299:
      Standard += item.amount
    elif 300 <= item.amount <= 999:
      Business += item.amount
    elif 1000 <= item.amount <= 4999:
      Professional += item.amount
    else:
      Enterprise += item.amount
    
    total = Standard + Business + Professional + Enterprise
  data = {
    'Standard':Standard,
    'Business':Business,
    'Professional':Professional,
    'Enterprise':Enterprise,
    'total':total
  }
  return render(request, 'accounts/dashboardpages/deposit-list.html',data)

@login_required(login_url = 'login')
def account_history(request):
  user = request.user
  if request.method == 'GET':
    category = request.GET.get('category', 'all_transactions')
    search_type = request.GET.get('search-type', '-1')
    month_from = request.GET.get('month_from')
    day_from = request.GET.get('day_from')
    year_from = request.GET.get('year_from')
    month_to = request.GET.get('month_to')
    day_to = request.GET.get('day_to')
    year_to = request.GET.get('year_to')

    # Check if date parameters are provided and not None
    if all([month_from, day_from, year_from, month_to, day_to, year_to]):
        # Assuming 'all_transactions' means all categories
        if category == 'all_transactions':
            deposit_transactions = Deposit.objects.filter(
              user=user,
              created_at__gte=f'{year_from}-{month_from}-{day_from}',
              created_at__lte=f'{year_to}-{month_to}-{day_to}'
            )
            withdraw_transactions = Withdraw.objects.filter(
              user=user,
              created_at__gte=f'{year_from}-{month_from}-{day_from}',
              created_at__lte=f'{year_to}-{month_to}-{day_to}'
            )
        elif category == 'deposit':
            deposit_transactions = Deposit.objects.filter(
              user=user,
              created_at__gte=f'{year_from}-{month_from}-{day_from}',
              created_at__lte=f'{year_to}-{month_to}-{day_to}'
            )
            withdraw_transactions = Withdraw.objects.none()
        elif category == 'withdrawal':
            deposit_transactions = Deposit.objects.none()
            withdraw_transactions = Withdraw.objects.filter(
              user=user,
              created_at__gte=f'{year_from}-{month_from}-{day_from}',
              created_at__lte=f'{year_to}-{month_to}-{day_to}'
            )
        # Add similar logic for other categories if needed
        print(deposit_transactions)
        # Render the template with the filtered transactions
        return render(request, 'accounts/dashboardpages/account_history.html.html', {
            'deposit_transactions': deposit_transactions,
            'withdraw_transactions': withdraw_transactions,
            # Add other context variables as needed
        })
    print('Nothing')
    # Handle other HTTP methods or invalid parameters
    return render(request, 'accounts/dashboardpages/account_history.html.html', {
        'error_message': 'Invalid parameters provided.',
        # Add other context variables as needed
    })
 
@login_required(login_url = 'login')   
def investment(request):
  user = request.user
  investment_list = Investment.objects.filter(user=user)
  data = {
    'investment_list':investment_list
  }
  return render(request, 'accounts/dashboardpages/investment.html',data)




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
    # referral_link = request.POST['referral_link']
    
    
    # check if email eist 
    useremail = User.objects.filter(email=email).exists()
    user_username = User.objects.filter(username=username).exists()
    if useremail:
      return JsonResponse({'success': False, 'error_code': 'Email_exist', 'message': 'Email Already exists'})
    elif user_username:
      return JsonResponse({'success': False, 'error_code': 'Username_taken', 'message': 'Username has been taken'})
    else:
      user = User.objects.create( first_name=fname,last_name=lname,username=username,email=email,password=hashed_password,country=country,btc_wallet=pay_account,agree_to_terms_and_condition=True)
      
      referral_link = ReferralLink.objects.create(user=user)
      user.referral_link = referral_link
      user.save()
      
      referral_link_param = request.POST['referral_link']
      if referral_link_param:
        try:
          # Extract the referral user from the referral link
          referral_user = ReferralLink.objects.get(link=referral_link_param).user
          
          refer = Referral.objects.create(
            referrer = referral_user,
            referred_user = user
          )
          refer.save()
        except ReferralLink.DoesNotExist:
          pass
      
      
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


@login_required(login_url = 'login')
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

@login_required(login_url='login') 
def profile(request):

  return render(request, 'accounts/profile.html')

@login_required(login_url='login') 
def setting(request):
  user_id = request.user.id
  
  if request.method == 'POST':
    btc = request.POST['btc']
    
    user = User.objects.get(id=user_id)
    user.btc_wallet = btc
    user.save()
    messages.success(request, 'Successfully Updated!')
    return redirect('setting')
  
  return render(request, 'accounts/setting.html')


@login_required(login_url='login') 
def profileImage(request):
  user_id = request.user.id

  if request.method == 'POST':
    image = request.FILES['imagefile']
    user = User.objects.get(pk=user_id)  
    user.profile_image = image 
    user.save()
    return redirect('setting')
  else:
    user = User.objects.get(pk=user_id)
    user.profile_image = None
    user.save()
    return redirect('setting')