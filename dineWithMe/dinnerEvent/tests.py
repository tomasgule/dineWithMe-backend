from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import DinnerEvent
from .models import UserProfile
from .models import DinnerPreferences
from userProfile.tests import create_users
from userProfile.tests import get_token
from .models import DinnerComment


# Create your tests here.
class DinnerEventTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        data = {
            "first_name": "Tomas",
            "last_name": "Gule",
            "username": "tom",
            "email": "tomas@gule.no",
            "password": "1234",
            "birthday": "1997-02-27",
            "phoneNumber": 12345678,
            "allergy": "Egg",
            "gender": "M",
            "bio": "Dette er en test",
        }
        response = (self.client.post('/api/auth/register', data, format='json'))
        assert response.status_code == 200
        self.token = response.data['token']

    def test_post_dinner(self):
        client = APIClient()
        data = {
            "username": "tom",
            "password": "1234"
        }
        response = client.post('/api/auth/login', data)
        assert response.status_code == 200
        self.token = response.data['token']
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        data = {
            "header": "he",
            "dateTime": "1901-05-14 06:12",
            "address": "hehe",
            "description": "hehe",
            "maxGuests": "3",
            "preferences": [{"preference": "vegan"}]
        }

        response = client.post('/api/dinnerEvent/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.item1_id = response.data["id"]

        data = {
            "header": "TestTittel",
            "dateTime": "2021-02-27T08:00",
            "address": "Klæbuveien",
            "description": "Test",
            "price": 50.50,
            "maxGuests": 10,
            "preferences": [{"preference": "vegan"}]
        }
        response = client.post('/api/dinnerEvent/', data, format='json')
        self.item2_id = response.data["id"]
        test_object = DinnerEvent.objects.get(id=self.item2_id)
        preference = DinnerPreferences.objects.filter(dinner_id=self.item2_id)
        self.assertEqual(test_object.header, "TestTittel")
        self.assertEqual(test_object.dateTime.strftime("%Y-%m-%d %H:%M"), "2021-02-27 08:00")
        self.assertEqual(test_object.address, "Klæbuveien")
        self.assertEqual(test_object.description, "Test")
        self.assertEqual(test_object.price, 50.50)
        self.assertEqual(preference[0].preference, "vegan" )

        response = client.get('/api/dinnerEvent/1/')
        self.assertEqual(response.data["header"], "he")
        self.assertEqual(response.data["dateTime"], "1901-05-14T06:12:00Z")
        self.assertEqual(response.data["address"], "hehe")
        self.assertEqual(response.data["description"], "hehe")
        self.assertEqual(response.data["price"], None)
        self.assertEqual(response.data["maxGuests"], 3)

    def test_delete_own_dinnerEvent(self):
        """Tester om DELETE funker på /api/dinnerEvent/{id}/"""
        client = APIClient()
        users = create_users(2)
        user_host = users.get(username=0)
        user_not_host = users.get(username=1)
        token_host = get_token(user_host)
        token_not_host = get_token(user_not_host)
        id = create_dinner(user_host).pk
        
        # Tester å slette uten token
        response = client.delete(f"/api/dinnerEvent/{id}/")
        self.assertEqual(response.status_code, 401)

        # Tester å slette med token til feil bruker
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_not_host)
        response = client.delete(f"/api/dinnerEvent/{id}/")
        self.assertEqual(response.status_code, 403)

        # Tester å slette med token til host
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_host)
        response = client.delete(f"/api/dinnerEvent/{id}/")
        self.assertEqual(response.status_code, 403)


    def test_put_dinnerEvent(self):
        """Tester om PUT funker på /api/dinnerEvent/{id}/"""
        client = APIClient()
        user = create_users(1).get(username=0)
        token = get_token(user)
        id = create_dinner(user).id

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            "header": "Test1",
            "dateTime": "2021-02-27T08:00",
            "address": "Klæbuveien",
            "description": "Test1",
            "price": 50.50,
            "maxGuests": 10,
            "preferences": []
        }
        response = client.put(f"/api/dinnerEvent/{id}/", data, format='json')
        self.assertEqual(response.data["header"], "Test1")
        self.assertEqual(response.data["dateTime"], "2021-02-27T08:00:00Z")
        self.assertEqual(response.data["address"], "Klæbuveien")
        self.assertEqual(response.data["description"], "Test1")
        self.assertEqual(response.data["price"], '50.50')
        self.assertEqual(response.data["maxGuests"], 10)

    def test_patch_dinnerEvent(self):
        """Tester om PATCH funker på /api/dinnerEvent/{id}/"""
        client = APIClient()
        user = create_users(1).get(username=0)
        token = get_token(user)
        id = create_dinner(user).id

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            "header": "Test1",
        }
        response = client.patch(f"/api/dinnerEvent/{id}/", data, format='json')
        self.assertEqual(response.data["header"], "Test1")


    def test_attendDinnerEvent(self):
        """Tester om man kan melde seg på et middagsarrangement"""
        client = APIClient()
        users = create_users(3)
        user_host = users.get(username=0)
        user_not_host = users.get(username=1)
        user_not_host_2 = users.get(username=2)
        
        token_host = get_token(user_host)
        token_not_host = get_token(user_not_host)
        token_not_host_2 = get_token(user_not_host_2)
        id = create_dinner(user_host, maxGuests=1).pk

        # Melde seg på andres middag
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_not_host)
        data = {
            "dinner_id": id
        }
        response = client.post('/api/attend', data, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(DinnerEvent.objects.get(id=id).guests.all()[0].username, '1')

        # Melde på flere enn max_guests
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_not_host_2)
        data = {
            "dinner_id": id
        }
        response = client.post('/api/attend', data, format='json')
        self.assertEqual(response.status_code, 400)

        # Melde seg av andres middag
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_not_host)
        data = {
            "dinner_id": id
        }
        response = client.delete('/api/attend', data, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(len(DinnerEvent.objects.get(id=id).guests.filter(username=1)), 0)

        # Melde seg på egen middag
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_host)
        data = {
            "dinner_id": id
        }
        response = client.post('/api/attend', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_cancel_dinner(self):
        """Tester om man kan avlyse et middagsarrangement"""
        client = APIClient()
        user = create_users(1).get(username=0)
        token = get_token(user)
        id = create_dinner(user).id

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            "is_cancelled": True,
        }
        response = client.patch(f"/api/dinnerEvent/{id}/", data, format='json')
        self.assertEqual(response.data["is_cancelled"], True)  

    def test_comment_dinner(self):
        """Tester om chatfunksjon"""
        client = APIClient()
        user = create_users(1).get(username=0)
        token = get_token(user)
        id = create_dinner(user).id
        print(id)

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            "dinner_id": id,
            "text": "Jeg er sulten"
        }
        response = client.post("/api/comment", data, format='json')
        self.assertEqual(DinnerComment.objects.filter(dinner_id__id=id)[0].text, "Jeg er sulten")
    



 
    
# Funksjoner som er hjelpsomme under testing
    
def create_dinner(user: UserProfile, header="Middag", dateTime="1901-05-14T06:12", address="NTNU",
 description="TEST", maxGuests=5):    

    return DinnerEvent.objects.create(header=header, dateTime=dateTime,address=address,
     description="Test", maxGuests=maxGuests, host=user)
    
