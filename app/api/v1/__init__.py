from flask import Blueprint
from flask_restful import Api
from .views import (SignUpEndpoint, LoginEndpoint,
                    AllMeetupsEndpoint, MeetupsEndpoint,
                    MeetupsEditCommentEndpoint, MeetupsEditLocationEndpoint)

v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(v1)
api.add_resource(SignUpEndpoint, '/signup')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(AllMeetupssEndpoint, '/meetups')
api.add_resource(MeetsupsEndpoint, '/meetups/<int:meetups_id>')
api.add_resource(MeetsupsEditCommentEndpoint, '/meetups/<int:meetups_id>/comment')
api.add_resource(MeetsupsEditLocationEndpoint, '/meetups/<int:meetups_id>/location')

