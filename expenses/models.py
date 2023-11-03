from django.db import models
from django.contrib.auth.models import User

# import uuid

# class CustomUser(AbstractUser):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     userId = models.CharField(max_length=10, unique=True, default=uuid.uuid4)    
#     name = models.CharField(max_length=100, blank=True)    
#     mobile_number = models.CharField(max_length=15)
#     simplify_expenses = models.BooleanField(default=True)

#     def __str__(self) -> str:
#         return self.name
    
class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'

    EXPENSE_TYPES = (
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percent'),
    )

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPES ,default=None)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paid_by")
    participants = models.ManyToManyField(User, related_name="participants")
    created_at = models.DateTimeField(auto_now_add=True)    
    exact_shares = models.TextField(default=None)
    percent_shares = models.TextField(default=None)   

    def split_expense(self):
        total_participants = len(self.participants.all())
        share = 0
        if self.expense_type == self.EQUAL:
            share = float(self.amount) / total_participants
        elif self.expense_type == self.EXACT:
            # Parse the exact_shares string and calculate the total shares
            exact_shares_list = self.exact_shares.split(',')
            total_shares = sum(float(share.split(':')[1]) for share in exact_shares_list)
            if total_shares != float(self.amount):
                raise ValueError("Total shares do not match the total amount.")
        elif self.expense_type == self.PERCENT:
            # Parse the percent_shares string and calculate the total sum of percentage shares
            percent_shares_list = self.percent_shares.split(',')
            total_percent_shares = sum(float(share.split(':')[1]) for share in percent_shares_list)
            if total_percent_shares != 100:
                raise ValueError("Total percentage shares do not equal 100.")

        for participant in self.participants.all():
            if participant != self.paid_by:
                if self.expense_type == self.PERCENT:
                    # Extract the percent share for the current participant
                    percent_share = next(share.split(':')[1] for share in percent_shares_list if share.split(':')[0] == participant.username)
                    share = (float(self.amount) * float(percent_share)) / 100
                elif self.expense_type == self.EXACT:
                    share= next(share.split(':')[1] for share in exact_shares_list if share.split(':')[0] == participant.username)
                    
                Balance.objects.create(
                    from_user=self.paid_by,
                    to_user=participant,
                    amount=share
                )

class ExpenseShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='expense_shares')
    percent = models.DecimalField(max_digits=5, decimal_places=2)

    
class Balance(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="balances_sent")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="balances_received")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
