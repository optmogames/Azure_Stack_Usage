import requests
import json
import urllib3
import re

# disable warnings
urllib3.disable_warnings()

# read private credentials from text file
client_id, client_secret, username, password, app_id_uri, directory_id, admin_arm_url, *_ = open('_PRIVATEwithPass.txt').read().split('\n')
if (client_id.startswith('*') and client_id.endswith('*')) or \
    (client_secret.startswith('*') and client_secret.endswith('*')):
    print('MISSING CONFIGURATION: the _PRIVATEwithPass.txt file needs to be edited ' + \
        'to add client ID and secret.')
    sys.exit(1)

# acquire access_token
microsoft_url = "https://login.microsoftonline.com/" + directory_id + "/oauth2/token?api-version=1.0"
post_headers = {"Content-Type": "application/x-www-form-urlencoded"}
post_data = {
    "grant_type" : "password",
    "scope" : "openid",
    "resource" : app_id_uri,
    "client_id" : client_id,
    "client_secret" : client_secret,
    "username" : username,
    "password" : password
}

response = requests.post(microsoft_url, data = post_data, headers = post_headers)
result_json = json.loads(response.text)
my_token = result_json['access_token']

# get tenantId
admin_sub_url = admin_arm_url + "/subscriptions/?api-version=2015-06-01-preview"
get_headers = { "Content-Type": "application/json", "Authorization": "Bearer " + my_token }
get_response = requests.get(admin_sub_url, headers=get_headers, verify=False)
get_response_json = json.loads(get_response.text)
output_subscription_id = get_response_json['value'][0]['subscriptionId']
output_tenantId = get_response_json['value'][0]['tenantId']
#print(get_response_json)
print("subscription id: " + output_subscription_id)
print("tenant id: " + output_tenantId)
# tenantId is User subscription id
output_tenantId = "0bbebd9d-457d-40e2-a0ee-536276e2bff5"

# get usage for tenantId
#storage_url = "https://adminmanagement.asdk2.umbrellar.io/subscriptions/" + output_subscription_id + "/providers/Microsoft.Compute.Admin/locations/local/quotas/Cloud%20PAYG%20Base%20Compute%20Quota%2001?api-version=2015-12-01-preview"
#usage_url = "https://adminmanagement.asdk2.umbrellar.io/subscriptions/" + output_subscription_id + "/providers/Microsoft.Commerce/subscriberUsageAggregates?reportedStartTime=2017-11-01&reportedEndTime=2017-11-20&aggregationGranularity=Daily&subscriberId=" + output_tenantId + "&api-version=2015-06-01-preview"
usage_url = admin_arm_url + "/subscriptions/" + output_subscription_id + "/providers/Microsoft.Commerce/UsageAggregates?reportedStartTime=2017-11-21&reportedEndTime=2017-11-22&aggregationGranularity=Hourly&subscriberId=" + output_tenantId+ "&api-version=2015-06-01-preview"
#print(storage_url)
usage = requests.get(usage_url, headers=get_headers, verify=False)
usage_json = json.loads(usage.text)
#usage_json_dump = json.dumps(usage_json, sort_keys=True, indent=4)
print(len(usage_json['value']))
# print(usage_json['nextLink'])
# if result is more than one page, use the nextLink.

# while (usage_json['nextLink']):
#      usage_next = requests.get(usage_json['nextLink'], headers=get_headers, verify=False)
#      usage_next_json = json.loads(usage_next.text)
#      usage_next_json_dump = json.dumps(usage_next_json, sort_keys=True, indent=4)
#      usage_json['nextLink'] = usage_next_json['nextLink']
#      print(usage_next_json['nextLink'])
#with open('report.txt', 'w+') as report:
#    report.write(usage_json_dump)
#print(usage_json_dump)