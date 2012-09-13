from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet

class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        return JSONEncoder.default(self,obj)
