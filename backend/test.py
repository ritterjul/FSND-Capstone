import os
import unittest
import http
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import Swimmer, Meet, Result

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'fsnd-ritterjul.eu.auth0.com')
API_AUDIENCE = os.environ.get('API_AUDIENCE', 'swimresults')
# configuration of test application with all permissions
CLIENT_ID = os.environ['TEST_CLIENT_ID']
CLIENT_SECRET = os.environ['TEST_CLIENT_SECRET']
# configuration of test application with permissions of role Swimmer
SWIMMER_CLIENT_ID = os.environ['TEST_SWIMMER_CLIENT_ID']
SWIMMER_CLIENT_SECRET = os.environ['TEST_SWIMMER_CLIENT_SECRET']
# configuration of test application with permissions of role Swimmer
COACH_CLIENT_ID = os.environ['TEST_COACH_CLIENT_ID']
COACH_CLIENT_SECRET = os.environ['TEST_COACH_CLIENT_SECRET']
# configuration of test application with permissions of role Swimmer
OFFICIAL_CLIENT_ID = os.environ['TEST_OFFICIAL_CLIENT_ID']
OFFICIAL_CLIENT_SECRET = os.environ['TEST_OFFICIAL_CLIENT_SECRET']

def getToken(id, secret):
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

    payload = {
        'client_id': id,
        'client_secret': secret,
        'audience': API_AUDIENCE,
        'grant_type': 'client_credentials'
    }
    
    headers = {'content-type': 'application/json'}

    conn.request('POST', '/oauth/token', json.dumps(payload), headers)

    data = conn.getresponse().read()

    conn.close()

    return json.loads(data.decode('utf-8'))['access_token']


class SwimResultsTestCase(unittest.TestCase):

    def setUp(self):
        """Executed before each test"""
        self.app = app

        self.client = self.app.test_client

        self.token = getToken(CLIENT_ID, CLIENT_SECRET)
        self.swimmer_token = getToken(SWIMMER_CLIENT_ID, SWIMMER_CLIENT_SECRET)
        self.coach_token = getToken(COACH_CLIENT_ID, COACH_CLIENT_SECRET)
        self.official_token = getToken(OFFICIAL_CLIENT_ID, OFFICIAL_CLIENT_SECRET)

    def tearDown(self):
        """Executed after each test"""
        pass

    '''
    Test endpoints for success and error handling
    '''
    
    def test_get_swimmers(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/swimmers', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['swimmers']))

    def test_get_swimmers_unauthorized(self):
        res = self.client().get('/swimmers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_swimmer(self):
        payload = {
            'id': 155847,
            'gender': 'F',
            'first name': 'Melina',
            'last name': 'Mattis',
            'year of birth': 1994
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().post('/swimmers', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], 155847)

    def test_create_swimmer_empty_gender(self):
        payload = {
            'id': 155847,
            'gender': '',
            'first name': 'Melina',
            'last name': 'Mattis',
            'year of birth': 1994
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().post('/swimmers', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_get_swimmer_details(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/swimmers/155849', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['swimmer']))

    def test_get_swimmer_details_invalid_id(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/swimmers/1000000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_swimmer_results(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/swimmers/155849/results', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['results']))

    def test_get_swimmer_results_invalid_id(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/swimmers/1000000/results', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_edit_swimmer(self):
        payload = {
            'year of birth': 1995
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().patch('/swimmers/155849',
                          data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['swimmer']['year of birth'], 1995)

    def test_edit_swimmer_invalid_year(self):
        payload = {
            'year of birth': 'someyear'
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().patch('/swimmers/155849',
                          data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_delete_swimmer(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().delete('/swimmers/155848', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], 155848)

    def test_delete_swimmer_invalid_id(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().delete('/swimmers/1000000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_meets(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/meets', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['meets']))

    def test_get_meets_unauthorized(self):
        res = self.client().get('/meets')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_meet(self):
        payload = {
            'id': 3,
            'name': '8. Volvo-Lochner-Cup',
            'start date': '02.05.2004',
            'end date': '02.05.2004',
            'city': 'Berlin',
            'country': 'Germany'
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().post('/meets', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_meet_invalid_name(self):
        payload = {
            'id': 4,
            'name': None,
            'start date': '02.05.2004',
            'end date': '02.05.2004',
            'city': 'Berlin',
            'country': 'Germany'
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().post('/meets', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_get_meet_details(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/meets/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['meet']))

    def test_get_meet_details_invalid_id(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/meets/1000000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_meet_results(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/meets/1/results', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['results']))

    def test_get_meet_results_invalid_id(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/meets/1000000/results', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_edit_meet(self):
        payload = {
            'name': 'Some meet'
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().patch('/meets/1', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['meet']['name'], 'Some meet')

    def test_edit_meet_invalid_date(self):
        payload = {
            'start date': 0
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        res = self.client().patch('/meets/1', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_delete_meet(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().delete('/meets/2', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], 2)

    def test_delete_meet_invalid_id(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().delete('/meets/1000000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_results(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        res = self.client().get('/results', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['results']))

    def test_get_results_unauthorized(self):
        res = self.client().get('/results')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
    
    '''
    Test endpoints for role based access control
    '''

    def test_role_swimmer_get_swimmers(self):
        headers = {'Authorization': f'Bearer {self.swimmer_token}'}
        res = self.client().get('/swimmers', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['swimmers']))

    def test_role_swimmer_delete_swimmer(self):
        headers = {'Authorization': f'Bearer {self.swimmer_token}'}
        res = self.client().delete('/swimmers/155849', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
    
    def test_role_coach_edit_swimmer(self):
        payload = {
            'year of birth': 1994
        }
        headers = {
            'Authorization': f'Bearer {self.coach_token}',
            'Content-Type': 'application/json'
        }
        res = self.client().patch('/swimmers/155849', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['swimmer']['year of birth'], 1994)

    def test_role_coach_delete_meet(self):
        headers = {'Authorization': f'Bearer {self.coach_token}'}
        res = self.client().delete('/meets/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_role_official_edit_meet(self):
        payload = {
            'name': '7. Volvo-Lochner-Cup'
        }
        headers = {
            'Authorization': f'Bearer {self.official_token}',
            'Content-Type': 'application/json'
        }
        res = self.client().patch('/meets/1', data=json.dumps(payload), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['meet']['name'], '7. Volvo-Lochner-Cup')

    def test_role_official_delete_swimmer(self):
        headers = {'Authorization': f'Bearer {self.official_token}'}
        res = self.client().delete('/swimmers/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
