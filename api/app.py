import os

from flask import Flask

from api.idx.resource import endpoint as index
from api.idx.resource import service
from api.idx.service import prepare_idx

app = Flask(__name__)

app.register_blueprint(index)
app.config['JSON_AS_ASCII'] = False

src = {
    'raw_data': {'vals': ['filials.raw_data.0', 'filials.raw_data.1',
                          'filials.raw_data.2', 'filials.raw_data.3',
                          'filials.raw_data.4'],
                 'format': 'json'
                 },
    'url': {'vals': ['filials.slice', 'filials.slice.1']}
}
docs = ['filials.raw_data.0', 'filials.raw_data.1', 'filials.raw_data.2', 'filials.raw_data.3',
        'filials.raw_data.4']

prepare_idx(
    service,
    docs=docs,
    src=src,
    prefix=os.path.join(os.getcwd(), 'dataset')
)

application = app
