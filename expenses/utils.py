from django.core.mail import send_mail

def send_expense_notification_email(expense):
    subject = 'New Expense Notification'
    message = f'You have been added to an expense: {expense.description}\n'
    message += f'Total amount you owe: INR {expense.amount}\n'
    from_email = 'your-email@example.com'
    recipient_list = [user.email for user in expense.participants.all()]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)