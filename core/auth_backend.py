from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import requests
import json

User = get_user_model()

class ProviderIDAuthBackend(BaseBackend):
    """
    Custom authentication backend for Provider ID
    """
    
    def authenticate(self, request, providerid_token=None, **kwargs):
        """
        Authenticate user using Provider ID token
        """
        if not providerid_token:
            return None
            
        # In real implementation, this would validate the JWT token with Provider ID API
        # For demo purposes, we'll handle both demo tokens and real JWT tokens
        
        # Demo mode - for testing
        if providerid_token.startswith('demo_providerid_token_'):
            # Create or get a demo user
            username = 'demo_user'
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user for demo
                user = User.objects.create_user(
                    username=username,
                    email='demo@example.com',
                    first_name='Demo',
                    last_name='User'
                )
            return user
        
        # Real JWT token validation with Provider ID API
        try:
            # Check if token looks like a JWT (basic validation)
            if len(providerid_token) > 50 and '.' in providerid_token:
                # Validate JWT token with Provider ID API
                api_url = 'https://provider.chiangmaihealth.go.th/check/token/'
                payload = {
                    'token': providerid_token
                }
                
                try:
                    response = requests.post(api_url, json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        
                        if response_data.get('status') == 200 and response_data.get('message') == 'Token is valid':
                            # Token is valid, extract user information
                            profile_data = response_data.get('data', {}).get('profile', {})
                            
                            # Extract user information from profile
                            id_card = profile_data.get('id_card', '')
                            organization = profile_data.get('organization', [])
                            
                            # Create username from ID card
                            username = f'{id_card}' if id_card else f'{hash(providerid_token) % 10000}'
                            
                            # Get position and hcode from organization
                            position = ''
                            hcode = ''
                            if organization and len(organization) > 0:
                                position = organization[0].get('position', '')
                                hcode = organization[0].get('hcode', '')
                            
                            try:
                                # Try to get existing user
                                user = User.objects.get(username=username)
                                
                                # Update user information if needed
                                if user.first_name != position or user.last_name != hcode:
                                    user.first_name = position
                                    user.last_name = hcode
                                    user.save()
                                    
                            except User.DoesNotExist:
                                # Create new user based on Provider ID data
                                user = User.objects.create_user(
                                    username=username,
                                    email=f'{username}',
                                    first_name=position,
                                    last_name=hcode
                                )
                                
                                # You might want to store additional information in a custom user profile model
                                # For now, we'll store some info in the user's first_name and last_name
                
                            return user
                        else:
                            print(f"Provider ID API returned invalid status: {response_data}")
                            return None
                    else:
                        print(f"Provider ID API error: {response.status_code} - {response.text}")
                        return None
                        
                except requests.exceptions.RequestException as e:
                    print(f"Error calling Provider ID API: {e}")
                    return None
                    
        except Exception as e:
            print(f"JWT validation error: {e}")
            return None
            
        return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 