import os
from crontab import CronTab


def create_cron_job():
    user_cron = CronTab(user=True)
    python_executable = os.path.abspath("aa_metrics.py")
    
    # Construct the command to call this script with --run-task argument
    command = f'python3 {python_executable} --run-task'
    
    # Remove existing job with the same comment to avoid duplicates
    for job in user_cron.find_comment('daily_task'):
        user_cron.remove(job)
    
    # Create a new cron job
    job = user_cron.new(command=command, comment='daily_task')
    
    # Set the job to run every day at 12:00 PM
    job.setall('0 12 * * *')
    
    # Write the job to the cron tab
    user_cron.write()
    
    print("Cron job created!")