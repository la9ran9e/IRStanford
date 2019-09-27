from flask import Blueprint, request, jsonify

from .service import Service


class HitsResponse:
    def __init__(self, hits, exclude, **kwargs):
        self._data = {
            "hits": hits,
            "total": len(hits),
            **kwargs
        }
        self._exclusions = set(exclude)

    @property
    def data(self):
        return {k: v for k, v in self._data.items() if k not in self._exclusions}

    @property
    def json(self):
        return jsonify(self.data)


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
    exclude = request.args.get("exc", [])
    exclude = exclude.replace(" ", "").split(",")
    try:
        hits = service.get(word)
    except Exception as err:
        raise
    else:
        return HitsResponse(hits, exclude).json, 200


@endpoint.route('search', methods=['GET'])
def search():
    q = request.args.get('q', None)
    if not q:
        return '', 400

    merge_type = request.args.get('mt', "skip_merge")
    if merge_type not in {"merge", "skip_merge"}:
        return '', 400

    exclude = request.args.get("exc", [])
    exclude = exclude.replace(" ", "").split(",")

    query_sequence = q.split()
    hits, stat = service.search(query_sequence, merge_type)
    return HitsResponse(hits, exclude, stat=stat, merge_type=merge_type).json, 200


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
