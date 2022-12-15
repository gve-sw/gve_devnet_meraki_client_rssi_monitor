""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import meraki, os
import pandas as pd
from dotenv import load_dotenv

#get environmental variables
load_dotenv()

#time in seconds to retrieve data from meraki
RESOLUTION = 300
#timespan for which the information will be fetched, in seconds 
TIMESPAN = 86400
RSSI_THRESHOLD = -75
API_KEY = os.environ['API_KEY']
ORG_NAME = os.environ['ORG_NAME']
NET_NAME = os.environ['NET_NAME']
SSID = os.environ['SSID']

dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

def main():
    #get org id
    org_id = get_org_id()
    if org_id is None:
        #given organization name did match an organization associated with Meraki API key
        print('''There was an issue getting the org id. 
        Check that the organization name is correct.''')
    else:
        #Org ID is retrieved 
        print("Retrieved organization ID")
        #get network ID based on defined network and associated org
        network_id = get_net_id(org_id)
        print("Retrieved networks from the organization")
        #get information about the existing APs on the defined network
        aps = get_meraki_aps(org_id, network_id)
        print("Retrieved APs from the network")
        #get the clients that have connected to each AP
        clients = get_network_clients(network_id)
        print("Retrieved wireless clients from the network")
        #filter the clients of the network by a provided ssid
        clients = filter_clients_by_ssid(clients)
        #join clients under a specific AP of the network, useful for relevant RSSI info
        clients = match_clients_to_aps(clients, aps)
        #structuring the obtained client data into a more manageable format 
        client_info = parse_client_info(clients)
        #get rssi information for each of the clients we've received
        client_info = get_rssi_from_clients(network_id, client_info)   
        #structuring the rssi info with the clients and APs
        rssi_list = parse_rssi_from_clients(client_info)
        #exports the obtained data to a CSV file using pandas
        export_data(rssi_list)

'''This function returns the organization id that is associated
with the organization name given in the environmental variables
in the .env file'''
def get_org_id():
    response = dashboard.organizations.getOrganizations()
    for org in response:
        if org['name'] == ORG_NAME:
            org_id = org['id']
            return org_id

    #if no organization is found with the name then None is returned
    return print("Hello")

'''This function returns the network id that is associated
with the network name given in the environmental variables
in the .env file'''
def get_net_id(org_id):
    response = dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')
    for network in response:
        if network['name'] == NET_NAME:
            network_id = network['id']
            return network_id
    #if no organization is found with the name then None is returned
    return print("Hello")

'''This function retrieves all the APs in the network, filtered via the 
productTypes parameter. The function then returns the response containing
the APs as a list'''
def get_meraki_aps(org_id, network_id): 
    aps = dashboard.organizations.getOrganizationDevices(org_id, 
    networkIds=network_id, productTypes='wireless', total_pages='all')
    print(aps)
    return aps

'''This function retrieves all the wireless clients in the network from the
 past day. The function returns a dictionary of clients.'''
def get_network_clients(network_id):   
    resp = dashboard.networks.getNetworkClients(network_id, recentDeviceConnections='Wireless', 
    timespan=TIMESPAN, total_pages='all')
    return resp

'''The function below filters the clients of the network by a given SSID. A 
list of these clients will be returned.'''
def filter_clients_by_ssid(clients):
    ssid_clients = []
    for client in clients:
        if client["ssid"] == SSID:
            ssid_clients.append(client)
    return ssid_clients

'''This function takes the filtered clients belonging to a specific SSID
and matches them to an AP of the network. This is done by taking the APs
found from a previous function and comparing the serials to the 'recentDeviceSerial' 
parameter. If there is a match then store the clients under the serial of the AP'''
def match_clients_to_aps(clients, aps):
    clients_per_device = {}
    for ap in aps:
        serial = ap['serial']
        clients_per_device[serial] = ap
        clients_per_device[serial]['clients'] = []
        for client in clients: 
            if client['recentDeviceSerial'] == serial:
                clients_per_device[serial]['clients'].append(client)
    return clients_per_device

'''This function filters and restructures the already attained information
into a more manageable way via a new dictionary'''
def parse_client_info(clients_per_device):
    client_info = {}
    try:
        for ap in clients_per_device.values():
            apSerial = ap['serial']
            apName = ap['name']
            apMac = ap['mac']
            apTagList = ap['tags']
            apTags = ", ".join(apTagList)

            for client in ap['clients']:
                clientId = client['id']
                clientMac = client['mac']
                clientDescription = client['description']
                clientSSID = client['ssid']

                client_info[clientId] = {
                    'clientId': clientId,
                    'clientMac': clientMac,
                    'clientDescription': clientDescription,
                    'clientSSID': clientSSID,
                    'apSerial': apSerial,
                    'apName': apName,
                    'apMac': apMac,
                    'apTags': apTags
                }   
        return client_info
    except Exception as e:
            print("Error - ", e )

'''This function calls an API endpoint which will respond back with the
signal quality history of a specific client and their associated AP. 
The timespan and resolution global variables are used to define the data
we desire. If the client has no RSSI history we remove that client.'''
def get_rssi_from_clients(network_id, client_info):
    client_info_with_rssi = client_info.copy()
    for client in client_info.values(): 
        clientId = client['clientId']
        apSerial = client['apSerial']
        resp = dashboard.wireless.getNetworkWirelessSignalQualityHistory(
            network_id, clientId=clientId, apSerial=apSerial, timespan=TIMESPAN,
             resolution=RESOLUTION)
        if resp:
            client_info[clientId]['client_rssi_data'] = resp
            print(resp)
        else: del client_info_with_rssi[clientId]
    client_info = client_info_with_rssi.copy() 

    if not client_info:
        print('''No RSSI data was found. This will be due to clients not being
         actively used within the specified timespan. If this continues please
         consider editing the timespan whilst being conscious of the resolution
         as well.''')
    print("RSSI Data Gathered")
    return client_info

'''This function filters and restructures the already attained client, 
ap, and RSSI information into a more manageable way via a new dictionary.'''
def parse_rssi_from_clients(client_info):
    rssi_list = []
    try: 
        for client in client_info.values():
            for client_rssi in client['client_rssi_data']:
                rssi_info = {
                    'client': client['clientId'],
                    'clientMac': client['clientMac'],
                    'clientDescription': client['clientDescription'],
                    'clientSSID': client['clientSSID'],
                    'apSerial': client['apSerial'],
                    'apName': client['apName'],
                    'apMac': client['apMac'],
                    'apTags': client['apTags'],
                    'rssi': client_rssi['rssi'],
                    'snr': client_rssi['snr'],
                    'startTs': client_rssi['startTs'],
                    'endTs': client_rssi['endTs']   
                }      
                if rssi_info['rssi'] is None: 
                    continue
                elif rssi_info['rssi'] <= RSSI_THRESHOLD:
                    rssi_list.append(rssi_info)  

            del client['client_rssi_data']
        return rssi_list
    except Exception as e:
            print("Error - ", e )

'''Finally, this function will be used to export our restructured and filtered
data to both a CSV file named rssi_data.csv, and an excel file named 
rssi_data.xlsx. The library used to export this data is called Pandas.'''
def export_data(rssi_list):
    df = pd.DataFrame.from_dict(rssi_list)
    df = df.sort_values('rssi')
    df.to_csv('rssi_data.csv', encoding='utf-8', index=False)
    print("RSSI Data Exported")

if __name__ == "__main__":
    main()