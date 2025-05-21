from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserHealth, MedicalCondition, Treatment, Recommendation
from .recommender import recommender
from .forms import UserHealthForm
from django.views.decorators.http import require_POST
import json

def home_view(request):
    """Home page view"""
    return render(request, 'portal/home.html')

@login_required
def dashboard_view(request):
    """User dashboard view"""
    # Get or create user health profile
    health_profile, created = UserHealth.objects.get_or_create(user=request.user)

    # Get recommendations
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-score')[:5]

    # Get all medical conditions
    conditions = MedicalCondition.objects.all()

    context = {
        'health_profile': health_profile,
        'recommendations': recommendations,
        'conditions': conditions,
    }

    return render(request, 'portal/dashboard.html', context)

@login_required
def health_profile_view(request):
    """View and update health profile"""
    health_profile, created = UserHealth.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserHealthForm(request.POST, instance=health_profile)
        if form.is_valid():
            form.save()
            # Retrain the recommender system
            recommender.train()
            return redirect('dashboard')
    else:
        form = UserHealthForm(instance=health_profile)

    return render(request, 'portal/health_profile.html', {'form': form})

@login_required
def recommendations_view(request):
    """View all recommendations"""
    # Get recommendations
    recommendations = recommender.get_recommendations(request.user.id, top_n=10)

    return render(request, 'portal/recommendations.html', {
        'recommendations': recommendations
    })

@login_required
@require_POST
def update_conditions(request):
    """Update user conditions via AJAX"""
    try:
        data = json.loads(request.body)
        condition_ids = data.get('conditions', [])

        # Get user health profile
        health_profile, created = UserHealth.objects.get_or_create(user=request.user)

        # Clear existing conditions
        health_profile.conditions.clear()

        # Add new conditions
        for condition_id in condition_ids:
            condition = get_object_or_404(MedicalCondition, id=condition_id)
            health_profile.conditions.add(condition)

        # Retrain the recommender system
        recommender.train()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def api_recommendations(request):
    """API endpoint for recommendations"""
    recommendations = recommender.get_recommendations(request.user.id, top_n=5)

    # Convert to JSON-serializable format
    data = [{
        'id': rec.id,
        'treatment_name': rec.treatment.name,
        'treatment_description': rec.treatment.description,
        'condition_name': rec.condition.name,
        'score': rec.score,
        'created_at': rec.created_at.isoformat()
    } for rec in recommendations]

    return JsonResponse({'recommendations': data})
