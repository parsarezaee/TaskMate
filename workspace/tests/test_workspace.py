from django.test import TestCase
from django.contrib.auth import get_user_model
from workspace.models import Workspace, Membership
from rest_framework.test import APIClient, APITestCase

User = get_user_model()

class WorkspaceTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name='testuser',
            last_name='test',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_workspace(self):
        response = self.client.post('/workspace/create/', {'name': 'Test Workspace', 'description': 'A sample description'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Workspace.objects.count(), 1)
        workspace = Workspace.objects.first()
        self.assertEqual(workspace.name, 'Test Workspace')


class WorkspaceUpdateTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name='testuser',
            last_name='test',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.workspace = Workspace.objects.create(name='Test Workspace', description='Sample description', admin=self.user)
        Membership.objects.create(user=self.user, workspace=self.workspace, role='admin')

    def test_update_workspace(self):
        updated_data = {
            'name': 'Updated Workspace Name',
            'description': 'Updated description'
        }
        response = self.client.put(f'/workspace/workspace/{self.workspace.id}/', updated_data)
        self.assertEqual(response.status_code, 200)

        self.workspace.refresh_from_db()
        self.assertEqual(self.workspace.name, 'Updated Workspace Name')
        self.assertEqual(self.workspace.description, 'Updated description')
