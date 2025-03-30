from django.shortcuts import render, redirect
from .forms import HealthDataForm
from .models import HealthData
from django.contrib.auth.decorators import login_required
from tracker.wellness.analyzer import WellnessAnalyzer
from tracker.aws_sns import send_sns_email_notification
from tracker.aws_dynamodb import log_to_dynamodb

@login_required
def add_data(request):
    if request.method == 'POST':
        form = HealthDataForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()

            # ✅ Log to DynamoDB
            log_to_dynamodb(
                username=request.user.username,
                steps=data.steps,
                sleep_hours=data.sleep_hours,
                calories=data.calories
            )

            # ✅ Trigger SNS email
            try:
                send_sns_email_notification(
                    subject='New Health Data Submitted',
                    message=f"{request.user.username} added health data on {data.date}."
                )
            except Exception:
                pass  # Optionally handle/log this elsewhere

            return redirect('dashboard')
    else:
        form = HealthDataForm()

    return render(request, 'tracker/add_data.html', {'form': form})

@login_required
def dashboard(request):
    data = HealthData.objects.filter(user=request.user).order_by('-date')

    # Analyze the most recent entry if it exists
    analysis = None
    if data.exists():
        latest = data.first()
        analyzer = WellnessAnalyzer(
            steps=latest.steps,
            sleep_hours=latest.sleep_hours,
            calories=latest.calories
        )
        category = analyzer.category()
        score = analyzer.activity_score()

        analysis = {
            'category': category,
            'score': score
        }

    return render(request, 'tracker/dashboard.html', {
        'data': data,
        'analysis': analysis
    })

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

import csv, os
from django.http import HttpResponse
from tracker.aws_helpers import upload_file_to_s3

@login_required
def export_csv(request):
    from .models import HealthData
    data = HealthData.objects.filter(user=request.user)

    filename = f"{request.user.username}_health_data.csv"
    local_path = os.path.join("tmp", filename)

    os.makedirs("tmp", exist_ok=True)

    with open(local_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Steps', 'Sleep Hours', 'Calories'])
        for item in data:
            writer.writerow([item.date, item.steps, item.sleep_hours, item.calories])

    # Upload to S3
    s3_key = f"exports/{filename}"
    upload_file_to_s3(local_path, s3_key)

    # Serve CSV download
    with open(local_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    

