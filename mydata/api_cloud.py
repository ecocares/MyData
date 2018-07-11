import requests

class ApiCloud:
  """ Flower Power API Cloud """

  url = 'https://api-flower-power-pot.parrot.com'
  
  def __setitem__(self, key, item): 
    self.__token[key] = item
  
  def __getitem__(self, key): 
    return self.__token[key]   
        
  def __init__(self, apiKey, apiSecret):
    self._credentials = {'client_id': apiKey, 'client_secret': apiSecret}
    self.__logged = False
    self.__token = {}
  
  def credentials(self, username):
    """ Sets user's credentials"""

    self._credentials['username'] = username
    self.__logged = True
        
  def login(self, username, password):
    self._credentials['username'] = username
    self._credentials['password'] = password
    options = self._credentials
    options['grant_type'] = 'password'

    req = requests.post(ApiCloud.url + '/user/v1/authenticate', data=options)

    if (req.status_code == 200):
      self.__logged = True
      self.__token = req.json()
      token=req.json()
      print ("Loggin successful!")
      return True
    else:
      self.__logged = False
      print ("Loggin Failure: " + req.json()['error'])
      return False

  def getSensorStatus(self):
    if (not self.__logged):
      return False

    path = '/garden/v1/status'
    req = requests.get(ApiCloud.url + path,
      headers={'Authorization': 'Bearer ' + self.__token['access_token']},
      params={'include_s3_urls': 1})
    return self.__returnResult(path, req)
        
        
  def getSensorDataSync(self):
    if (not self.__logged):
      return False

    path = '/garden/v2/configuration'
    req = requests.get(ApiCloud.url + path,
      headers={'Authorization': 'Bearer ' + self.__token['access_token']},
      params={'include_s3_urls': 1})
    return self.__returnResult(path, req)

  def getSamplesLocation(self, identifier, formDateTime, toDateTime):
    if (not self.__logged):
      return False

    path = '/sensor_data/v6/sample/location/' + identifier
    req = requests.get(ApiCloud.url + path,
      headers={'Authorization': 'Bearer ' + self.__token['access_token']},
      params={'from_datetime_utc': formDateTime, 'to_datetime_utc': toDateTime})
    return self.__returnResult(path, req)


  def __returnResult(self, path, req):
    if (req.status_code == 200):
      return req.json()
    else:
      return req.status_code, "Error: " + path


  def __str__(self):
    dest = "User: " + self._credentials['username'] + "\n"
    dest += "Logged: " + str(self.__logged)
    return dest
