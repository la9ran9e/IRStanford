from flask import Blueprint, request, jsonify

from .service import Service

endpoint = Blueprint('index', __name__, url_prefix='/idx')


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


@endpoint.route('get/<string:word>', methods=['GET'])
def get(word):
    print(service._sources)
    try:
        hits = service.get(word)
    except Exception as err:
        raise
    else:
        return jsonify(hits), 200


@endpoint.route('search', methods=['GET'])
def search():
    q = request.args.get('q', None)
    if not q:
        return '', 400
    query_sequence = q.split()
    hits = service.search(query_sequence)
    return jsonify(hits), 200


@endpoint.route('source/<string:src>/feed', methods=['POST'])
def feed_src(src):
    if not request.files:
        return '', 400

    format = request.args.get('f', None)

    files = request.files.values()
    for file in files:
        path = file.name
        file.save(path)
        file.close()
        try:
            service.feed_src(src, path, format=format)
        except Exception as err:
            print('err', err)
            return '', 400

    return '', 201
