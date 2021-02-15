import datetime
import logging
import os
import flask
from flask import Flask, jsonify
from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_pyoidc.user_session import UserSession
import requests

app = Flask(__name__)

APP_BASE_URI = 'https://example2.USERNAME.repl.co'
APP_CLIENT_ID = '4fa2099f-ae7d-4f92-8d4b-2a30b6043d84'
APP_SECRET = os.getenv('APP_SECRET')

AUTH_PROVIDER_BASE_URI = 'https://auth.dataporten.no'
AUTH_PROVIDER_NAME = 'Feide'
GROUPS_BASE_URI = 'https://groups-api.dataporten.no'
MY_GROUPS_PATH = 'groups/me/groups'

# OpenID Connect configuration
app.config.update({'OIDC_REDIRECT_URI': APP_BASE_URI + '/' + 'redirect_uri'})

# Flask web framework configuration
# See http://flask.pocoo.org/docs/0.12/config/
app.config.update({
    'SECRET_KEY': 'flask_session_key',  # make sure to change this!!
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'PERMANENT_SESSION_LIFETIME': datetime.timedelta(minutes=1).total_seconds(),
})

auth_provider_config = ProviderConfiguration(
    issuer=AUTH_PROVIDER_BASE_URI,
    client_metadata=ClientMetadata(APP_CLIENT_ID, APP_SECRET))
auth = OIDCAuthentication({AUTH_PROVIDER_NAME: auth_provider_config})


def get_my_groups(user_session):
    headers={"Authorization": f"Bearer {user_session.access_token}"}
    response = requests.get(GROUPS_BASE_URI + '/' + MY_GROUPS_PATH, headers=headers)
    response.raise_for_status()
    return response.json()


@app.route('/')
@auth.oidc_auth(AUTH_PROVIDER_NAME)
def login1():
    user_session = UserSession(flask.session)
    mygroups = get_my_groups(user_session)
    return jsonify([
        {'access_token': user_session.access_token},
        {'id_token': user_session.id_token},
        {'userinfo': user_session.userinfo},
        {'mygroups': mygroups}
    ])


@app.route('/logout')
@auth.oidc_logout
def logout():
    return "You've logged out"


@auth.error_view
def error(error=None, error_description=None):
    return jsonify({'error': error, 'message': error_description})


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    auth.init_app(app)
    app.run(host='0.0.0.0', port=8080)
