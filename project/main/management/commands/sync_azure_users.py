from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
import msal
import requests
from main.models import AzureCredentials

class Command(BaseCommand):
    help = 'Sync users and groups from Azure AD'

    def handle(self, *args, **kwargs):
        credentials = AzureCredentials.objects.first()
        if not credentials:
            self.stdout.write(self.style.ERROR("No Azure credentials found."))
            return

        # Securely decrypt and log values for verification
        tenant_id = credentials.tenant_id
        client_id = credentials.client_id
        client_secret = credentials.client_secret

        # Log the credentials to make sure they're correct and visible for debugging
        self.stdout.write(f'Tenant ID: {tenant_id}')
        self.stdout.write(f'Client ID: {client_id}')
        self.stdout.write(f'Client Secret: {client_secret[:4]}********{client_secret[-4:]}')  # Partially masked for security

        token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        resource = 'https://graph.microsoft.com'
        scope = f"{resource}/.default"
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope,
        }
        token_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        token_r = requests.post(token_endpoint, data=token_data, headers=token_headers)
        token_response = token_r.json()
        token = token_response.get('access_token')
        if not token:
            self.stdout.write(self.style.ERROR("Failed to obtain token."))
            self.stdout.write(self.style.ERROR(token_response))
            return

        headers = {'Authorization': 'Bearer ' + token}

        # Mapping for Azure AD groups to Django groups
        group_mapping = {
            'OOL_Admin': 'Admin',
            'OOL_IT': 'IT',
            'OOL_User': 'User',
            'OOL_Approver': 'Approver',
        }

        graph_url = f"{resource}/v1.0/groups"
        groups_response = requests.get(graph_url, headers=headers).json()

        group_id_map = {}
        for group in groups_response.get('value', []):
            if group.get('displayName') in group_mapping:
                django_group, created = Group.objects.get_or_create(name=group_mapping[group.get('displayName')])
                group_id_map[group.get('id')] = django_group

        # Sync Users
        user_url = f"{resource}/v1.0/users"
        users_response = requests.get(user_url, headers=headers).json()
        for user in users_response.get('value', []):
            if 'userPrincipalName' in user:
                user_email = user['userPrincipalName']
                django_user, created = User.objects.get_or_create(email=user_email)

                # Ensure user details are updated, with defaults if needed
                first_name = user.get('givenName') or 'Unknown'
                last_name = user.get('surname') or 'User'

                django_user.username = user_email 
                django_user.first_name = first_name
                django_user.last_name = last_name

                if created:
                    django_user.set_unusable_password()  # Ensure password is managed through Azure AD

                django_user.save()
                
                member_of_url = f"{resource}/v1.0/users/{user['id']}/memberOf"
                member_of_response = requests.get(member_of_url, headers=headers).json()
                for group in member_of_response.get('value', []):
                    if group['id'] in group_id_map:
                        group_id_map[group['id']].user_set.add(django_user)

                self.stdout.write(self.style.SUCCESS(f"Synced {user_email} to {', '.join(group_mapping.values())} groups."))

        self.stdout.write(self.style.SUCCESS("Users and groups synced successfully."))