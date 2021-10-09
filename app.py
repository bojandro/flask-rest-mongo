from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_mongoengine import MongoEngine
import datetime
import json


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'db',
    'host': 'mongo',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)
name_space = api.namespace('api', description='API')


class User(db.Document):
    email = db.StringField()
    name = db.StringField()
    creating_date = db.DateTimeField(default=datetime.datetime.utcnow)
    company_id = db.IntField()

    def to_dict(self):
        return {"name": self.name,
                "email": self.email,
                "creating_date": str(self.creating_date),
                "company_id": self.company_id}

@name_space.route("/user")
class UserClass(Resource):
    @name_space.doc(params={'name': 'name of a user'})
    def get(self):
        props = request.args
        name = props['name']
        user = User.objects(**props).first()
        if not user:
            return {'error': 'entry not found'}, 404
        else:
            return user.to_dict(), 200

    @name_space.doc(params={'name': 'name of a user',
                            'email': 'email of a user',
                            'company_id': 'company id'})
    def post(self):
        props = request.args
        user = User(**props).save()
        return {'message': 'created successfully'}, 201

    @name_space.doc(params={'name': 'name of a user',
                            'email': 'email of a user',
                            'company_id': 'company id'})
    def put(self):
        props = request.args
        user = User.objects(name=props['name']).first()
        if not user:
            return {'error': 'entry not found'}, 404
        else:
            user.update(**props)
        return {'message': 'updated successfully'}, 200

    @name_space.doc(params={'name': 'name of a user'})
    def delete(self):
        props = request.args
        user = User.objects(**props).first()
        if not user:
            return {'error': 'entry not found'}, 404
        else:
            user.delete()
        return {'message': 'deleted successfully'}, 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
