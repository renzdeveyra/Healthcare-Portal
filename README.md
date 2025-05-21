# Healthcare Portal

A comprehensive healthcare portal with AI-powered treatment recommendations, secure authentication, and OAuth integration.

## Features

- **User Authentication**
  - Email/password registration and login
  - OAuth integration with GitHub and Google
  - Multi-factor authentication (MFA) support

- **AI-Powered Recommendations**
  - Machine learning-based treatment recommendations
  - Personalized health insights based on user profiles
  - Recommendation scoring and ranking

- **Health Profile Management**
  - Track medical conditions
  - Record basic health metrics (age, height, weight)
  - Secure storage of health information

- **Responsive Design**
  - Mobile-friendly interface
  - Accessible UI components

## Technology Stack

- **Backend**: Django 4.2
- **Authentication**: django-allauth, django-otp
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: scikit-learn, pandas, numpy
- **Deployment**: Render (free tier)

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/healthcare-portal.git
   cd healthcare-portal
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=
   GITHUB_CLIENT_ID=your-github-client-id
   GITHUB_CLIENT_SECRET=your-github-client-secret
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser

## OAuth Setup

### GitHub OAuth

1. Go to GitHub Developer Settings: https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in the application details:
   - Application name: Healthcare Portal
   - Homepage URL: http://127.0.0.1:8000/ (for local development)
   - Authorization callback URL: http://127.0.0.1:8000/accounts/github/login/callback/
4. Register the application
5. Copy the Client ID and Client Secret to your `.env` file

### Google OAuth

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project
3. Go to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth client ID"
5. Configure the consent screen
6. Create OAuth client ID:
   - Application type: Web application
   - Name: Healthcare Portal
   - Authorized JavaScript origins: http://127.0.0.1:8000
   - Authorized redirect URIs: http://127.0.0.1:8000/accounts/google/login/callback/
7. Copy the Client ID and Client Secret to your `.env` file

## Deployment on Render

This application is configured for easy deployment on Render's free tier.

1. Create a Render account: https://render.com/
2. Fork this repository to your GitHub account
3. In the Render dashboard, click "New +" and select "Blueprint"
4. Connect your GitHub account and select your forked repository
5. Render will automatically detect the `render.yaml` configuration file
6. Click "Apply" to create the web service and database

The deployment will automatically:
- Create a PostgreSQL database
- Build and deploy your Django application
- Set up environment variables
- Configure HTTPS

### Important Notes for Render Free Tier

- The free PostgreSQL database will be deleted after 90 days. You'll need to backup your data before then.
- The free web service will spin down after 15 minutes of inactivity, causing a delay on the first request after inactivity.
- You'll need to manually set these environment variables in the Render dashboard:
  - GITHUB_CLIENT_ID
  - GITHUB_CLIENT_SECRET
  - GOOGLE_CLIENT_ID
  - GOOGLE_CLIENT_SECRET

### Update OAuth Callback URLs

After deployment, update your OAuth callback URLs in GitHub and Google developer settings to use your Render domain:
- GitHub: https://your-app-name.onrender.com/accounts/github/login/callback/
- Google: https://your-app-name.onrender.com/accounts/google/login/callback/

## AI Recommender System

The Healthcare Portal includes an AI-powered recommendation system that suggests treatments based on user health profiles and medical conditions.

### How It Works

1. **Data Collection**: The system collects user health data (age, height, weight) and medical conditions.
2. **Feature Engineering**: User and treatment data are transformed into feature vectors.
3. **Similarity Calculation**: Cosine similarity is used to match users with appropriate treatments.
4. **Recommendation Generation**: Treatments are ranked by relevance score and presented to users.

### Training the Model

The recommender system automatically trains when:
- A user updates their health profile
- A new medical condition or treatment is added
- An administrator manually triggers training

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django and the Django community
- scikit-learn for machine learning capabilities
- Render for free tier hosting
