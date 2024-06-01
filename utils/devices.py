"""
Common Device Management Tasks
"""

def get_devices(obj):
    try:
        response = obj.load('/api/v1/spaces/default/instances')
        instances = response.get('_embedded').get('devices')
        return instances
    except Exception as e:
        return e


# TODO needs to be tested
def factory_reset_device(obj, id):
    try:
        return obj.update(f'/api/device/v1/proxy/${id}?path=/actions/factory-reset', data={'verify': True})
    except Exception as e:
        return e


# TODO needs to be tested
def delete_device(obj, id):
    try:
        return obj.delete(f'api/v1/spaces/default/instances/${id}', data={'save_backup': False})
    except Exception as e:
        return e

