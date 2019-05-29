# -*- coding: utf-8 -*

import requests

import base64


class AnimalRecognizer(object):

  def __init__(self, api_key, secret_key):
      self.access_token = self._get_access_token(api_key=api_key, secret_key=secret_key)
      self.API_URL = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/animal' + '?access_token=' \
                      + self.access_token

  @staticmethod
  def _get_access_token(api_key, secret_key):
      api = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
            '&client_id={}&client_secret={}'.format(api_key, secret_key)
      rp = requests.post(api)
      if rp.ok:
          rp_json = rp.json()
          #print(rp_json['access_token'])
          return rp_json['access_token']
      else:
          print('=> Error in get access token!')

  def get_result(self, params):
      rp = requests.post(self.API_URL, data=params)
      if rp.ok:
          #print('=> Success! got result: ')
          rp_json = rp.json()
          #print(rp_json)
          return rp_json
      else:
          print('=> Error! token invalid or network error!')
          print(rp.content)
          return None

  def detect(self, img_path):
      f = open(img_path, 'rb')
      img_str = base64.b64encode(f.read())
      params = {'image': img_str, 'top_num': 6,'baike_num':6}
      rp_json = self.get_result(params)

      return rp_json['result']

