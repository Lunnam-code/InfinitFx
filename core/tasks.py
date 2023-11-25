from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django_apscheduler.models import DjangoJob
from decimal import Decimal,  getcontext
from accounts.models import User



scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
register_events(scheduler)

def update_earnings(investment_id, start_time):
    from .models import Investment
    investment = Investment.objects.get(id=investment_id)
    user = User.objects.get(pk=investment.user.pk) 
    
    interest_rate = investment.plan.profit_percentage / 100
    
    duration = investment.plan.maturity_duration_hours
    every_three_minutes_increment = (duration * 60) / 3
    job_id = investment.job_id
    elapsed_time = datetime.now() - start_time
    
    getcontext().prec = 6
    # Check if one hour has elapsed
    if elapsed_time >= timedelta(hours=investment.maturity_duration_hour):
      percentage =  investment.deposit.amount * Decimal(interest_rate)
      user.earning -= investment.profit
      # user.earning += percentage
      user.save()
      investment.profit = percentage
      investment.status = Investment.STATUS_COMPLETED
      investment.save()
      
      user.account_balance += percentage 
      user.save()
      scheduler.remove_job(job_id)
      # scheduler.pause(job_id)
    else:
      earning_increment = investment.deposit.amount * Decimal(interest_rate) / Decimal(every_three_minutes_increment)

      investment.profit += earning_increment
      investment.save()
      user.earning += earning_increment
      user.save()
      pass

scheduler.start()
    





