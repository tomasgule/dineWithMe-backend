# Create your tests here.
from django.test import TestCase
from rest_framework.test  import APITestCase
from userProfile.models import UserProfile
from rest_framework.test  import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
# Create your tests here.


class UserProfileTests(APITestCase):
    

    def test_register_userProfile(self):
        client = APIClient()
        data = { 
            "first_name": "Tomas",
            "last_name": "Gule",
            "username": "tomasgule",
            "email": "tomas@gule.no",
            "password": "1234", 
            "birthday": "1997-02-27",
            "phoneNumber": 12345678,
            "allergy": "Egg",
            "gender": "M",
            "bio": "Dette er en test"  
        }
        response = client.post('/api/auth/register', data=data, format="json")
        token = response.data['token']

        client.credentials(HTTP_AUTHORIZATION='Token '+token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Funksjoner som er hjelpsomme under testing

def get_token(user: UserProfile):
    client = APIClient()
    data = {
        "username": user.username,
        "password": user.username
    }
    response = client.post('/api/auth/login', data, format='json')
    token = response.data['token']
    return token

def create_users(number_of_users):
    for i in range(number_of_users):
        userProfile = UserProfile.objects.create_user(username=f"{i}", email=f"{i}@test.com", password=f"{i}")
        userProfile.first_name = str(i)
        userProfile.last_name = str(i)
        userProfile.birthday = "1901-05-14"
        userProfile.phoneNumber = i
        userProfile.allergy = str(i)
        userProfile.gender = 'm'
        userProfile.bio = str(i)
        userProfile.save()
    return UserProfile.objects.all()
