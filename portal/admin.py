from django.contrib import admin
from .models import MedicalCondition, Treatment, UserHealth, Recommendation

@admin.register(MedicalCondition)
class MedicalConditionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'effectiveness_score')
    list_filter = ('conditions',)
    search_fields = ('name', 'description')
    filter_horizontal = ('conditions',)

@admin.register(UserHealth)
class UserHealthAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'height', 'weight')
    list_filter = ('conditions',)
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('conditions',)

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'treatment', 'condition', 'score', 'created_at')
    list_filter = ('condition', 'created_at')
    search_fields = ('user__username', 'treatment__name', 'condition__name')
    readonly_fields = ('score', 'created_at')
