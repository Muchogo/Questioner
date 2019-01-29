

from flask import make_response, jsonify, request
from flask_restful import Resource
from .models import User, MeetupsModel

from .validators import (UserSchema, MeetupsSchema,
                         MeetupsEditSchema)


class SignUpEndpoint(Resource, User):
    

    def __init__(self):
        self.user = User()

    def post(self):
        
        data = request.get_json(force=True)
        user_data, error = UserSchema().load(data)

        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)

        if self.user.check_username(user_data['username']):
            return make_response(jsonify({"message": "Username already exists"}), 400)
        if self.user.check_email(user_data['email']):
            return make_response(jsonify({"message": "Email already exists"}), 400)

        if 'isAdmin' in user_data:
            self.user.save(
                user_data['first_name'],
                user_data['last_name'],
                user_data['other_names'],
                user_data['phonenumber'],
                user_data['email'],
                user_data['username'],
                user_data["password"],
                user_data['isAdmin']
            )
        else:
            self.user.save(
                user_data['first_name'],
                user_data['last_name'],
                user_data['other_names'],
                user_data['phonenumber'],
                user_data['email'],
                user_data['username'],
                user_data["password"]
            )

        return make_response(jsonify({"message": "Sign Up successful. Welcome!"}), 201)


class LoginEndpoint(Resource, User):
    

    def __init__(self):
        self.users = User()

    def post(self):

        data = request.get_json(force=True)
        user_data, error = UserSchema(
            only=('username', 'password')).load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)
        if self.users.confirm_login(user_data['username'], user_data['password']):
            return make_response(jsonify({"message": "Login Success!"}), 200)

        return make_response(jsonify({"message": "Login Failed!"}), 401)


class BaseMeetupsEndpoint(Resource, MeetupsModel, User):

    def __init__(self):
        self.db = MeetupsModel()
        self.user = User()


class AllMeetupsEndpoint(BaseMeetupsEndpoint):

    def get(self):
        
        return make_response(jsonify(self.db.db), 200)

    def post(self):

        data = request.get_json(force=True)
        meetups_data, error = MeetupsSchema().load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)
        if self.user.search_user(meetups_data['createdBy']):
            new_meetup = self.db.save( data["comment"], data['location'],
                                        data['createdBy'], data['images'], data['videos'])
            return make_response(jsonify({"message": "New meetup created",
                                          "data": new_meetup}), 201)

        return make_response(jsonify({"message": "Not Authorized"}), 401)


class MeetupsEndpoint(BaseMeetupsEndpoint):

    def get(self, meetups_id):

        if self.db.db:
            result = self.db.search_meetups(meetups_id)
            if result is not None:
                return make_response(jsonify({"data": result}), 200)
            return make_response(jsonify({"message": "Meetup does not exist"}), 404)

        return make_response(jsonify({"message": "No Meetups created yet!"}), 200)

    def delete(self, meetups_id):

        data = request.get_json(force=True)
        meetups_data = MeetupsEditSchema(
            only=('userid',)).load(data)
        if meetups_data.errors:
            return make_response(jsonify({
                "message": "Missing userid field",
                "required": meetups_data.errors,
                "status": 400}), 400)
        result = self.db.search_meetups(meetups_id)

        if result is not None:
            user = self.user.search_user(data['userid'])
            if user is not None and user['userid'] == result['createdBy']:
                meetups_to_pop = self.db.db.index(result)
                self.db.db.pop(meetups_to_pop)
                return make_response(jsonify({
                    "message": "Meetups record has been deleted",
                    "status": 204,
                    "id": meetups_id}), 200)

            return make_response(jsonify({"message": "Forbidden: Record not owned",
                                          "status": 403}), 403)

        return make_response(jsonify({
            "message": "Meetup does not exist",
            "status": 404
        }), 404)


class MeetupsEditCommentEndpoint(BaseMeetupsEndpoint):

    def put(self, meetups_id):

        data = request.get_json(force=True)
        meetups_data = MeetupsEditSchema(
            only=('userid', 'comment')).load(data)
        if meetups_data.errors:
            return make_response(jsonify({
                "message": "Comment/userid is not present",
                "required": meetups_data.errors}),
                400)

        result = self.db.search_meetups(meetups_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['comment'] = data['comment']
                    return make_response(jsonify({
                        'message': "Meetups Updated",
                        "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)


class MeetupsEditLocationEndpoint(BaseMeetupsEndpoint):

    def put(self, meetups_id):

        data = request.get_json(force=True)
        meetups_data = MeetupsEditSchema(
            only=('userid', 'location')).load(data)
        if meetups_data.errors:
            return make_response(jsonify({
                "message": "location/userid is not present",
                "required": meetups_data.errors}),
                400)
        result = self.db.search_meetups(meetups_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['location'] = data['location']
                    return make_response(jsonify({
                        'message': "Meetups Updated", "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)
