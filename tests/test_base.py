from app import app
import unittest
import json
import datetime


class TestsStart(unittest.TestCase):

    def setUp(self):
         self.app = app.test_client()
        
    def test_if_can_get_users(self):
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
    def test_if_can_get_welcome(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


    def test_if_can_get_redflags(self):
        response = self.app.get('/api/v1/red-flags')
        self.assertEqual(response.status_code, 200)




    def test_redflag_not_json(self):
        """ Test redflag content to be posted not of form data """
        expectedreq ={
	
        "comment":"he ran away",
        "type":"Red_flag",
        "location":"Mbarara",
        "status":"draft",
        "image":"image"

        }
        result = self.app.post(
            '/api/v1/red-flags',
            content_type = 'text/html',
            data=json.dumps(expectedreq)
        )

        #data=result.data.decode()
        data=json.loads(result.data.decode())
        # self.assertEqual(result.status_code,401)
        self.assertEqual(data['msg'],'request header type should be form-data')
        #self.assertEqual(data['failed'],'content-type must be multipart/form-data')
    def test_create_user_request_not_json(self):
        """ Test redflag content to be posted not in json format """
        expectedreq = {
             'incident_type': 'government intervention/broken bridge',
            'comment_description': 'river rwizi bridge had broken down',
            'status': 'ressolved',
            'current_location': 'kashanyarazi, mbarara',
            'created': 'Nov 29 2018 : 11:04AM'
        }
        result = self.app.post(
            '/api/v1/users',
            content_type = 'text/html',
            data=json.dumps(expectedreq)
        )
        data=json.loads(result.data.decode())
        self.assertEqual(result.status_code,401)
        self.assertEqual(data['failed'],'content-type must be application/json')
       

    def test_if_user_cant_delete_innexistent_flag(self):
        res=self.app.delete('/api/v1/red-flags/1')
        data=json.loads(res.data.decode())
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['msg'],'item not found')
    def test_if_user_cant_get_an_innexistent_flag(self):
        res=self.app.get('/api/v1/red-flags/2')
        data=json.loads(res.data.decode())
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['msg'],'item not found')


if __name__ == "__main__":
    unittest.main()
    

    