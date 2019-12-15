from flask.views import MethodView
from component.enums import Role
from component.auth import authorization


class IndexHandler(MethodView):

    permission = Role.Other

    @authorization
    def get(self):
        return {"message": "Welcome to Sailboat Index.", "code": 200, "data": {}}