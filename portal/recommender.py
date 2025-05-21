import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
import os
from pathlib import Path
from .models import UserHealth, Treatment, MedicalCondition, Recommendation

class HealthRecommender:
    """AI-based health treatment recommender system"""
    
    def __init__(self):
        self.model_path = Path(__file__).resolve().parent / 'models'
        self.model_path.mkdir(exist_ok=True)
        self.scaler_file = self.model_path / 'scaler.joblib'
        self.similarity_matrix_file = self.model_path / 'similarity_matrix.joblib'
        
        # Initialize or load models
        if os.path.exists(self.scaler_file) and os.path.exists(self.similarity_matrix_file):
            self.scaler = joblib.load(self.scaler_file)
            self.similarity_matrix = joblib.load(self.similarity_matrix_file)
        else:
            self.scaler = StandardScaler()
            self.similarity_matrix = None
    
    def _prepare_data(self):
        """Prepare data for the recommender system"""
        # Get all user health profiles
        health_profiles = UserHealth.objects.all().prefetch_related('conditions')
        
        # Get all treatments
        treatments = Treatment.objects.all().prefetch_related('conditions')
        
        # Create user features
        user_features = []
        for profile in health_profiles:
            # Basic health metrics
            features = {
                'user_id': profile.user.id,
                'age': profile.age or 0,
                'height': profile.height or 0,
                'weight': profile.weight or 0,
            }
            
            # Add conditions as one-hot encoding
            for condition in MedicalCondition.objects.all():
                features[f'condition_{condition.id}'] = 1 if condition in profile.conditions.all() else 0
            
            user_features.append(features)
        
        # Create treatment features
        treatment_features = []
        for treatment in treatments:
            features = {
                'treatment_id': treatment.id,
                'effectiveness': treatment.effectiveness_score,
            }
            
            # Add conditions as one-hot encoding
            for condition in MedicalCondition.objects.all():
                features[f'condition_{condition.id}'] = 1 if condition in treatment.conditions.all() else 0
            
            treatment_features.append(features)
        
        # Convert to DataFrames
        user_df = pd.DataFrame(user_features)
        treatment_df = pd.DataFrame(treatment_features)
        
        return user_df, treatment_df
    
    def train(self):
        """Train the recommender system"""
        user_df, treatment_df = self._prepare_data()
        
        if user_df.empty or treatment_df.empty:
            return False
        
        # Extract features (excluding IDs)
        user_features = user_df.drop('user_id', axis=1).values
        treatment_features = treatment_df.drop('treatment_id', axis=1).values
        
        # Scale features
        user_features_scaled = self.scaler.fit_transform(user_features)
        treatment_features_scaled = self.scaler.transform(treatment_features)
        
        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(user_features_scaled, treatment_features_scaled)
        
        # Save models
        joblib.dump(self.scaler, self.scaler_file)
        joblib.dump(self.similarity_matrix, self.similarity_matrix_file)
        
        return True
    
    def get_recommendations(self, user_id, top_n=5):
        """Get treatment recommendations for a user"""
        if self.similarity_matrix is None:
            self.train()
            
        if self.similarity_matrix is None:
            return []
        
        user_df, treatment_df = self._prepare_data()
        
        # Find user index
        try:
            user_idx = user_df[user_df['user_id'] == user_id].index[0]
        except (IndexError, KeyError):
            return []
        
        # Get similarity scores for this user
        user_scores = self.similarity_matrix[user_idx]
        
        # Create recommendations
        recommendations = []
        for i, score in enumerate(user_scores):
            treatment_id = treatment_df.iloc[i]['treatment_id']
            treatment = Treatment.objects.get(id=treatment_id)
            
            # Get conditions that match between user and treatment
            user_health = UserHealth.objects.get(user_id=user_id)
            user_conditions = user_health.conditions.all()
            treatment_conditions = treatment.conditions.all()
            
            # Find matching conditions
            matching_conditions = set(user_conditions).intersection(set(treatment_conditions))
            
            # Create a recommendation for each matching condition
            for condition in matching_conditions:
                # Check if recommendation already exists
                rec, created = Recommendation.objects.update_or_create(
                    user_id=user_id,
                    treatment=treatment,
                    condition=condition,
                    defaults={'score': float(score)}
                )
                recommendations.append(rec)
        
        # Return top N recommendations
        return sorted(recommendations, key=lambda x: x.score, reverse=True)[:top_n]

# Create a singleton instance
recommender = HealthRecommender()
