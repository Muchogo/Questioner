
import unittest
from flask import json
from ... import create_app
from .basetest import BaseTestCase
app = create_app()


class MeetupsTest(BaseTestCase):
 
    def test_create_new_meetups(self):
        result = self.app.post('/api/v1/meetups', data=self.new_incident)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "New meetup created")

    def test_create_new_meetups_with_wrong_format(self):
        result = self.app.post('/api/v1/meetups',
                               data=self.new_incident_data_with_wrong_format)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_get_all_meetups(self):
        result = self.app.get('/api/v1/meetups')
        self.assertEqual(result.status_code, 200)

    def test_create_new_meetups_user_doesnt_exist(self):
        result = self.app.post('/api/v1/meetups',
                               data=self.new_meetups_data_nonexisting_user)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Not Authorized")

    def test_get_specific_meetups(self):
        result = self.app.get("/api/v1/meetups/1")
        self.assertEqual(result.status_code, 200)
        data  = json.loads(result.data)
        self.assertEqual(data['data']["meetupsId"], 1)

    def test_get_non_existing_record(self):
        result = self.app.get("/api/v1/meetups/500")
        self.assertEqual(result.status_code, 404)

    def test_update_an_meetups_location(self):
        data = json.dumps({"location": "-1.28333, 36.81667",
                           "userid": 1})
        result = self.app.put('/api/v1/meetups/1/location', data=data)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Meetups Updated")

    def test_update_an_meetups_comment(self):
        data = json.dumps({"comment": "Postponed",
                           "userid": 1})
        result = self.app.put('/api/v1/incident/1/comment', data=data)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Meetups Updated")

    def test_update_on_nonexisting_meetups(self):
        data = json.dumps({"comment": "Postponed",
                           "userid": 1})
        result = self.app.put('/api/v1/meetups/500/comment', data=data)
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Update on non-existing record denied")
    
    def test_update_on_with_wrong_format(self):
        data = json.dumps({"comment": "Postponed",
                          })
        result = self.app.put('/api/v1/meetups/1/comment', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Comment/userid is not present")

    def test_update_with_empty_values(self):
        data = json.dumps({})
        result = self.app.put('/api/v1/meetups/1/location', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "location/userid is not present")

    def test_update_on_incident_not_in_draft(self):
        data = json.dumps({"comment": "Postponed",
                           "userid": 2})
        result = self.app.put('/api/v1/meetups/2/comment', data=data)
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Cannot update a record not in draft state")

    def test_update_user_didnt_create_comment(self):
        data = json.dumps({"comment": "Postponed",
                           "userid": 2})
        result = self.app.put('/api/v1/meetups/1/comment', data=data)
        self.assertEqual(result.status_code, 403)

    def test_delete_meetups(self):
        result = self.app.delete('/api/v1/meetups/3',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(data["status"], 204)
        self.assertEqual(data['message'], "Incident record has been deleted")

    def test_delete_meetups_with_wrong_user(self):
        result = self.app.delete('/api/v1/meetups/2',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['message'], "Forbidden: Record not owned")

    def test_delete_meetups_with_missing_field(self):
        result = self.app.delete('/api/v1/incident/2',
                            data=json.dumps({}))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'],"Missing userid field")
    def test_delete_nonexisting_meetups(self):
        result = self.app.delete('/api/v1/meetups/500',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['message'], "Meetups does not exist")
if __name__ == '__main__':
    unittest.main()
