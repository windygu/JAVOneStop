from math import ceil
from blitzdb import Document, FileBackend
from blitzdb.document import DoesNotExist


class JavObj(Document):
    pass

class JavManagerDB:
    def __init__(self):
        self.jav_db = FileBackend('jav_manager.db')

    def create_indexes(self):
        self.jav_db.create_index(JavObj, 'stat')

    def bulk_list(self):
        return self.jav_db.filter(JavObj, {})

    def partial_search(self, search_string: str):
        rt = self.jav_db.filter(JavObj, {'pk': {'$regex': search_string}})[:20]
        return rt

    def query_on_filter(self, filter_on: dict, page=1, limit=8):
        rt = self.jav_db.filter(JavObj, filter_on)
        rt_max_page = ceil(len(rt)/limit)
        rt_list = rt[(page-1)*limit : (page)*limit]

        return [dict(x) for x in rt_list], rt_max_page

    def upcreate_jav(self, jav_obj: dict):
        # uniform car to upper case
        jav_obj['car'] = str(jav_obj['car']).upper()
        # set pk to car
        jav_obj['pk'] = jav_obj['car']
        # set default to no opinion
        #0-want, 1-viewed, 2-no opinion 3-local 4-downloading
        jav_obj.setdefault('stat', 2)

        _jav_doc = JavObj(jav_obj)
        _jav_doc.save(self.jav_db)
        self.jav_db.commit()
        print('writed ', jav_obj)

    def get_by_pk(self, pk: str):
        return self.jav_db.get(JavObj, {'pk': pk.upper()})

    def pk_exist(self, pk: str):
        try:
            self.jav_db.get(JavObj, {'pk': pk})
            return True
        except DoesNotExist:
            return False