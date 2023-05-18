#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/0-hbnb', strict_slashes=False)
def hbnb():
    """Display template with states, cities & amentities"""
    states = storage.all('State').values()
    state_c = dict([state.name, state] for state in states)
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    cache_id = (str(uuid.uuid4()))
    return render_template('0-hbnb.html',
                           states=state_c,
                           amenities=amenities,
                           places=places,
                           owner=users,
                           cache_id=cache_id)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
