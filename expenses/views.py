from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Expense, Balance
from django.db.models import Sum
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User

@login_required(login_url='/expenses/login/')
def add_expense(request):
   
    if request.method == 'POST':
        description = request.POST['description']
        amount = request.POST['amount']
        paid_by_id = request.POST['paid_by']
        participants = request.POST.getlist('participants[]')
        expense_type = request.POST['expense_type']
        exact_shares = request.POST['exact_shares']
        percent_shares = request.POST['percent_shares']
        
        expense = Expense.objects.create(
            description=description,
            amount=amount,
            paid_by_id=paid_by_id,           
            expense_type=expense_type,
            exact_shares= exact_shares,
            percent_shares=percent_shares,   
        )

        
        expense.participants.set(participants)
        expense.split_expense()
        
        return redirect('view_expenses')
    
    users = User.objects.all()
    return render(request, 'add_expense.html', {'users': users,'active':'add_expense'})

@login_required(login_url='/expenses/login/')
def view_expenses(request):
    try:
        expenses = Expense.objects.all()
    except Exception:
        expenses = []    
    # Add logic to display expenses
    return render(request, 'view_expenses.html', {'expenses': expenses,'active':'view_expenses'})


@login_required(login_url='/expenses/login/')
def view_balances(request):
    balances = Balance.objects.values('from_user__username', 'to_user__username').annotate(total_amount=Sum('amount'))
    return render(request, 'view_balances.html', {'balances': balances,'active':'view_balances'})


@login_required(login_url='/expenses/login/')
def home(request):    
    return render(request, 'homepage.html',{'active':'home'})


@login_required(login_url='/expenses/login/')
def passbook(request):
    user = request.user

    # Retrieve balances where the current user is the sender
    balances_sent = Balance.objects.filter(from_user=user)

    # Retrieve balances where the current user is the recipient
    balances_received = Balance.objects.filter(to_user=user)

    # Calculate net balance
    net_balance = 0
    for balance in balances_sent:
        net_balance -= balance.amount
    for balance in balances_received:
        net_balance += balance.amount

    # Retrieve transaction history
    transaction_history = Expense.objects.filter(paid_by=user)

    # Sort the transaction history by date (you may need to adjust the field name)
    transaction_history = transaction_history.order_by('-created_at')

    return render(request, 'passbook.html', {
        'user': user,
        'balances_sent': balances_sent,
        'balances_received': balances_received,
        'net_balance': net_balance,
        'transaction_history': transaction_history,
        'active':'passbook',
    })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('user_login')