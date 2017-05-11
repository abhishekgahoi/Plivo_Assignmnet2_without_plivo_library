import requests
import json
import time


class ResponseError(Exception):
    pass


class SendHTTPSRequest(object):
    def __init__(self, auth_id, auth_token, url='https://api.plivo.com', version="v1"):
        self.auth_token = auth_token
        self.auth_id = auth_id
        self.version = version
        self.url = url.rstrip('/') + '/' + self.version
        self._api = self.url + '/Account/%s' % self.auth_id
        self.headers = {'Abhishek-API-Caller':'TestCaller'}

    def _request(self, method, path, data={}):
        #path = path.rstrip('/') + '/'
        path = path + '/'
        if method == 'POST':
            headers = {'content-type': 'application/json'}
            headers.update(self.headers)
            r = requests.post(self._api + path, headers=headers,
                              auth=(self.auth_id, self.auth_token),
                              data=json.dumps(data))
        elif method == 'GET':
            r = requests.get(self._api + path, headers=self.headers,
                             auth=(self.auth_id, self.auth_token),
                             params=data)
        elif method == 'DELETE':
            r = requests.delete(self._api + path, headers=self.headers,
                                auth=(self.auth_id, self.auth_token),
                                params=data)
        content = r.content
        if content:
            try:
                response = json.loads(content.decode("utf-8"))
            except ValueError:
                response = content
        else:
            response = content
        return (r.status_code, response)

    @staticmethod
    def get_param(params, key):
        try:
            return params[key]
        except KeyError:
            print ("missing mandatory parameter %s", key)
    def extract_cdr_func(self, params=None):
        if not params: params = {}
        call_uuid = params.pop('call_uuid')
        return self._request('GET', '/Call/%s' % call_uuid, data=params)

    def start_call_func(self, params=None):
        if not params: params = {}
        return self._request('POST', '/Call', data=params)

    def disconnect_call_func(self, params=None):
        if not params: params = {}
        call_uuid = params.pop('call_uuid')
        return self._request('DELETE', '/Call/%s' % call_uuid, data=params)


if __name__ == "__main__":
        
	auth_id = "MAZDMXNDM0MTMWYTJKNJ"
	auth_token = "ZDVhYTQ5YTViZmQ4ZTBmYWIyYTMzZDJiNWY2NTQ1"

	p = SendHTTPSRequest(auth_id, auth_token)

	input_vars = {
		'to': 'sip:abhishekgahoi170422055353@phone.plivo.com',    # The phone numer to which the call will be placed
		'from' : '1234567890', # The phone number to be used as the caller id
		'answer_url' : "https://s3.amazonaws.com/plivosamplexml/play_url.xml",
		'answer_method' : "GET", # The method used to call the answer_url
	}

	# Make an outbound call and print the response
	code,response = p.start_call_func(input_vars)

	#print "about to print uuid"
	print(str(response))


	data = response

	print data['message']
	print data['request_uuid']
	str2= data['request_uuid']

	
	### call hang up #
	time.sleep(5)
	input_vars = {'call_uuid': str2}

	code,response = p.disconnect_call_func(input_vars)
	print(str(response)) 

	###generating CDR####
	input_vars = {'call_uuid': str2}

	code,response = p.extract_cdr_func(input_vars)
	print str(response)

	
