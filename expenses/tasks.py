from celery import shared_task
from django.core.mail import send_mail
from expenses.models import Balance
from django.contrib.auth.models import User
from django.db.models import Sum

@shared_task
def send_weekly_balance_email():
    # Get a list of all users
    users = User.objects.all()

    # Loop through users to send them individual balance emails
    for user in users:
        # Calculate the total amount of money they owe to others
        
        total_owe = Balance.objects.filter(from_user=user).aggregate(total_owe=Sum('amount'))
        total_owe = total_owe['total_owe'] or 0

        # Prepare the email content
        subject = 'Weekly Balance Summary'
        message = f'Hello, {user.username}!\n'
        message += f'Total amount you owe to others: INR {total_owe}\n'
        from_email = 'your-email@example.com'
        recipient_list = [user.email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)