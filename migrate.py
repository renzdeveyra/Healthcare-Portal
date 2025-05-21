#!/usr/bin/env python
import os
import sys

# Set up Django environment first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcareportal.settings')

# Then import Django and other modules
import django
django.setup()

from django.contrib.sites.models import Site
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import call_command

def run_migrations():
    """Run database migrations"""
    call_command('migrate')
    print("Migrations completed successfully")

def setup_site():
    """Set up the default site"""
    try:
        # Get or create the default site
        site, created = Site.objects.get_or_create(id=1)
        
        # Get the hostname from environment or use default
        hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'healthcare-portal.onrender.com')
        
        # Make sure we're using the full domain without 'https://'
        if hostname.startswith('https://'):
            hostname = hostname[8:]
        
        # Update site details
        site.domain = hostname
        site.name = 'Healthcare Portal'
        site.save()
        
        print(f"Site configured with domain: {hostname}")
    except Exception as e:
        print(f"Error setting up site: {e}")

if __name__ == '__main__':
    # Check if database is available
    try:
        conn = connections['default']
        conn.cursor()
        print("Database connection successful")
        
        # Run migrations
        run_migrations()
        
        # Set up site
        setup_site()
        
    except OperationalError:
        print("Database unavailable, skipping migrations")


