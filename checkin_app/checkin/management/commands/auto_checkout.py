from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timezone as dt_timezone, timedelta
from checkin.models import AttendanceLog, User

class Command(BaseCommand):
    help = 'Automatically check out all users at 5 PM or 11:59:59 PM if they checked in after 5 PM'

    def handle(self, *args, **kwargs):
        # Get the current time in the local timezone
        current_time = timezone.localtime()
        
        # Find all users who are still checked in
        users = User.objects.filter(is_checked_in=True)
        for user in users:
            # Find the active attendance log for the user
            log = AttendanceLog.objects.filter(employee=user, check_out_time__isnull=True).first()
            if log:
                # Set the checkout time to 5 PM on the day of the check-in in the local timezone
                check_in_time_local = timezone.localtime(log.check_in_time)
                if check_in_time_local.hour < 17:
                    checkout_time_local = check_in_time_local.replace(hour=17, minute=0, second=0, microsecond=0)
                else:
                    # If the check-in time is after 5 PM, set the checkout time to 11:59:59 PM the same day
                    checkout_time_local = check_in_time_local.replace(hour=23, minute=59, second=59, microsecond=0)
                
                # Convert the local checkout time to UTC
                checkout_time_utc = checkout_time_local.astimezone(dt_timezone.utc)
                
                # Ensure the checkout time is after the check-in time
                if checkout_time_utc > log.check_in_time:
                    log.check_out_time = checkout_time_utc
                    log.save()
                    user.is_checked_in = False
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Checked out user {user.username} at {checkout_time_utc} UTC'))
                else:
                    self.stdout.write(self.style.WARNING(f'Checkout time {checkout_time_utc} is not after check-in time {log.check_in_time} for user {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'No active check-in found for user {user.username}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully checked out all users at 5 PM or 11:59:59 PM local time'))