import time

import requests
import json
import pprint
import sys
from concurrent import futures
from multiprocessing import cpu_count
import datetime

token = "34462a5e-4a5a-4218-8595-7b091ca4a18d::b763d614-54e3-44ec-9966-a53db54c5dd4"

# BASE_URL = 'https://cpe-vrops-beta.oc.vmware.com/suite-api/api/resources'
BASE_URL = 'https://vcsa-01a.tanzu.local:4000/suite-api/api/resources'

keys = [
    "sys|poweredOn", 'net|transmitted_average', 'virtualDisk|write_average', 'virtualDisk|read_average',
    'virtualDisk:Aggregate of all instances|numberReadAveraged_average', 'net|received_average',
    'virtualDisk:Aggregate of all instances|numberWriteAveraged_average', 'cpu|usagemhz_average', 'mem|guest_demand',
    'cpu|demandmhz', 'sys|osUptime_latest', 'cpu|vm_capacity_provisioned', 'net|maxObserved_Rx_KBps',
    'net|maxObserved_Tx_KBps ']


def send_requests():
    executor = futures.ThreadPoolExecutor(max_workers=cpu_count())

    query = {
        'resourceKind': 'virtualmachine'
    }

    headers = {
        'Authorization': 'vRealizeOpsToken %s' % token,
        'accept': 'application/json'
    }
    results = requests.get(BASE_URL, headers=headers, params=query, verify=False).json()

    vms = [x for x in results['resourceList']]

    identifierList = [i['identifier'] for i in vms]
    stats_post_future = executor.submit(get_stats_post, identifierList)
    #print(stats_post_future.result())
    #properties_future = executor.submit(get_properties, identifierList)
    #print(properties_future.result())

    '''
    for i in vms:

        identifier = i['identifier']

        properties_future = executor.submit(get_properties, identifier)
        print(properties_future.result(10))

        
        stats_future = executor.submit(get_stats, identifier)

        symptoms = get_symptoms(identifier)
        alerts = get_alerts(identifier)
        super_metrics = executor.submit(get_super_metrics, identifier)

        stats_key_future = executor.submit(get_stat_keys, identifier)
        print(stats_key_future.result())
        
        stats_post_future = executor.submit(get_stats_post, identifier)

        stats = stats_post_future.result(timeout=10)
        print(stats)
    '''


#  print(stats)


# stats.update(properties)

#  pprint.pprint(stats)

# Available values for rollupType : SUM, AVG, MIN, MAX, NONE, LATEST, COUNT
# Available values for intervalTypes HOURS, MINUTES, SECONDS, DAYS, WEEKS, MONTHS, YEARS
def get_stats_post(vmid):
    tim = int(time.time()*1000) - 5*60*1000
    print(tim)

    stats_for_resource = requests.post(BASE_URL + '/stats/query',
                                       json={
                                           "rollUpType": "AVG",
                                           "begin": tim,
                                           "intervalType": "MINUTES",
                                           "intervalQuantifier": 5,
                                           'resourceId': vmid,
                                           "statKey": keys
                                       }, headers={'Authorization': f'vRealizeOpsToken {token}',
                                                   'accept': 'application/json'}, verify=False)

    print(stats_for_resource.json())


def get_alerts(vmid):
    headers = {
        'Authorization': 'vRealizeOpsToken %s' % token,
        'accept': 'application/json'
    }
    url = "https://cpe-vrops-beta.oc.vmware.com/suite-api/api/alerts?resourceId=%s" % (vmid)
    results = requests.get(url, headers=headers).json()
    return results


def get_symptoms(vmid):
    headers = {
        'Authorization': 'vRealizeOpsToken %s' % token,
        'accept': 'application/json'
    }
    url = "https://cpe-vrops-beta.oc.vmware.com/suite-api/api/symptoms?resourceId=%s" % (vmid)
    results = requests.get(url, headers=headers, verify=False).json()
    return results


def get_properties(vmid):
    headers = {
        'Authorization': 'vRealizeOpsToken %s' % token,
        'accept': 'application/json'
    }
    url = "%s/%s/properties?" % (BASE_URL, 'resources')

    for i in vmid:
        url += 'resourceId=%s&' % i

    print("Url is : " + url)
    results = requests.get(url, headers=headers, verify=False).json()
    print(results)
    CONFIG_PROPERTIES = {
        'datastore|maxObservedRead': 'readcap',
        'datastore|maxObservedWrite': 'writecap',
        'runtime|memoryCap': 'memhzcap',
        'summary|config|isTemplate': 'isTemplate',
        'config | createDate': 'createDate'
    }

    d = {}
    for i in results['property']:

        if i['name'] in CONFIG_PROPERTIES:
            name = i['name']
            value = i['value']
            d[name] = value

    return d


def get_stats(vmid):
    headers = {
        'Authorization': 'vRealizeOpsToken %s' % token,
        'accept': 'application/json'
    }
    url = "%s/%s/stats/latest" % (BASE_URL, vmid)
    results = requests.get(url, headers=headers, verify=False).json()
    d = {}
    results = results['values'][0]['stat-list']['stat']

    for i in results:
        key = i['statKey']['key']
        data = i['data']
        d[key] = data
    return d


def get_stat_keys(vmid):
    headers = {
        'Authorization': 'vRealizeOpsToken %s' % token,
        'accept': 'application/json'
    }
    print("Getting stat keys : ")
    url = "%s/%s/statkeys" % (BASE_URL, vmid)
    results = requests.get(url, headers=headers, verify=False).json()
    print(results)


def get_super_metrics(vmid):
    headers = {
        'Authorization': 'vRealizeOpsToken %s' % token,
        'accept': 'application/json'
    }
    url = 'https://cpe-vrops-beta.oc.vmware.com/suite-api/api/supermetrics'
    results = requests.get(url, headers=headers).json()
    # print(results)


def login():
    response = requests.post('https://vcsa-01a.tanzu.local:4000/suite-api/api/auth/token/acquire',
                             json={
                                 "username": "admin",
                                 "password": "VMware1!"
                             }
                             , headers={'accept': 'application/json'}, verify=False).json()
    return response['token']


if __name__ == '__main__':
    # sys.stdout = open('output.txt', 'wt')

    token = login()
    print(token)

    send_requests()
