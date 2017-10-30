import api_helper
import requests
import json
import unittest
import linecache
import ConfigParser

from ConfigParser import SafeConfigParser

#Reading values from config file.
parser = SafeConfigParser()
parser.read('conf.ini')
auth_id = parser.get('SECURITY', 'auth_id')
auth_token = parser.get('SECURITY', 'auth_token')

#Creating api helper instance with valid auth_id and token.
api = api_helper.API(auth_id, auth_token)

class TestLiveCallFinalResponse(unittest.TestCase):

    def test_live_call_response(self):
        expected_keys = ["direction", "from", "call_status", "request_uuid", "api_id", "to", "caller_name", "call_uuid", "session_start"]
        final_response = call_flow()
        self.assertEqual(final_response[0], 200)
        live_call_body = final_response[1]
        for key in expected_keys:
            self.assertTrue(key in live_call_body)
        self.assertEqual(final_response[2], live_call_body["request_uuid"])
        self.assertEqual(live_call_body["request_uuid"], live_call_body["call_uuid"])


def call_flow():
	# Making api call for searching numbers in US, and getting 2 numbers for buying.
    params = {
    'limit' : parser.get('PARAMS', 'limit'),
    'offset' : parser.get('PARAMS', 'offset'),
    'country_iso' : parser.get('PARAMS', 'country_iso')
    }
    searchNumberResponse = api.search_phone_numbers(params)
    print str(searchNumberResponse[1])
    json_response = searchNumberResponse[1]
    number_1 = json_response["objects"][0]["number"]
    number_2 = json_response["objects"][1]["number"]

    buy_params = {
        'number' : number_1
    }
#Buying 2 numbers.
    buy_response = api.buy_phone_number(buy_params)
    print str(buy_response)

    buy_params = {
        'number' : number_2
    }
    buy_response2 = api.buy_phone_number(buy_params)
    print str(buy_response2)

#Calling 1 bought number from other. and storing the request_uuid for further validation.
    call_params = {
        'to' : number_2,
        'from' : number_1,
        'answer_url' : parser.get('PARAMS', 'answer_url'),
        'answer_method' : "GET"
        
    }
    call_response = api.make_call(call_params)
    print str(call_response)
    request_uuid = call_response[1]["request_uuid"]

#Getting all the current live calls and fetching the call_uuid for the live call.
    live_calls_params = {
        'status' : parser.get('PARAMS', 'call_status')
    }

    live_calls = api.get_live_calls(live_calls_params)
    print str(live_calls)
    call_uuid = live_calls[1]["calls"][0]
    print str(call_uuid)
    
# Making call to get the details of the call spawned by us above. and passing the response for the test case validator. 
    current_live_call_params = {
        'status' : parser.get('PARAMS', 'call_status'),
        'call_uuid' : call_uuid
    }
    my_call = api.get_live_call(current_live_call_params)
    print str(my_call)
    print str(my_call[0])
#my_call_2 = api.get_cdr(current_live_call_params)
#print str(my_call_2)
    return(my_call[0], my_call[1], request_uuid)


if __name__ == '__main__':
    unittest.main()

