
import json
import datetime
from lbgenerator.lib import utils

def validate_reg_data(cls, request):

    params, method = utils.split_request(request)
    if method == 'GET': return None

    valid_fields = (
        'id_reg',
        'json_reg',
        'grupos_acesso',
        'dt_reg',
        'dt_reg_del',
        'dt_index_rel',
        'dt_index_tex',
        'dt_index_sem'
        )

    data = utils.filter_params(params, valid_fields)

    if method == 'POST':
        return validate_post_data(cls, data)

    elif method == 'PUT':
        id = int(request.matchdict['id'])
        return validate_put_data(cls, data, id)

def validate_post_data(cls, data):

    if 'json_reg' in data:
        id = cls.context.entity.next_id()
        json_reg = utils.to_json(data.get('json_reg'))

        base = cls.get_base()

        data['id_reg'] = id
        data['json_reg'] = base.validate(json_reg, id)
        data['dt_reg'] = datetime.datetime.now()

        data.update(cls.get_relational_data(json_reg))

    return data

def validate_put_data(cls, data, id):

    if 'json_reg' in data:
        json_reg = utils.to_json(data['json_reg'])

        base = cls.get_base()

        data['json_reg'] = base.validate(json_reg, id)

        data.update(cls.get_relational_data(json_reg))
        if not 'dt_index_tex' in data:
            data['dt_index_tex'] = None

    return data

