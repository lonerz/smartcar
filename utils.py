def get_value(data, attr):
  raw_value = data.get(attr)

  if not raw_value:
    return None

  type = raw_value.get('type')
  value = raw_value.get('value')

  if not type:
    return value
  
  if type == 'String':
    return value
  elif type == 'Boolean':
    return value == 'True'
  elif type == 'Number':
    return float(value)
  elif type == 'Array':
    return value
  elif type == 'Null':
    return None
