from flask import Blueprint, request, jsonify
from .service import Service


endpoint = Blueprint('index',
                     __name__,
                     url_prefix='/idx')


service = Service()


@endpoint.route('feed/<string:field>', methods=['POST'])
def feed(field):
    if 'file' not in request.files:
        return '', 400

    file = request.files['file']
    try:
        service.feed(field, file)
    except Exception as err:
        print('err', err)
        return '', 400
    else:
        return '', 201
    finally:
        file.close()


@endpoint.route('search/<string:word>', methods=['GET'])
def search(word):
    try:
        hits = service.search(word)
    except Exception as err:
        raise
    else:
        return jsonify(hits), 200


@endpoint.route('source/<string:src>/feed', methods=['POST'])
def feed_src(src):
    if not request.files:
        return '', 400

    files = request.files.values()
    for file in files:
        path = file.name
        file.save(path)
        file.close()
        try:
            service.feed_src(src, path)
        except Exception as err:
            print('err', err)
            return '', 400

    return '', 201
