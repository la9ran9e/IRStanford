from flask import Flask

from api.idx.resource import endpoint as index


app = Flask(__name__)

app.register_blueprint(index)
app.config['JSON_AS_ASCII'] = False
