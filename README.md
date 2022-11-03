# gve_devnet_meraki_client_rssi_monitor
This prototype provides the user with a report of historical signal qualities seen by both AP and Client, with a focus on the RSSI metric. This use case is ideal for troubleshooting in scenarios such as sticky clients. 

## Contacts
* Jordan Coaten

## Solution Components
* Meraki SDK
* Python 3.9 

## Installation/Configuration
The following commands are executed in the terminal.

1. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). 
Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html). 

2. Access the created virtual environment folder

        $ cd your_venv

3. Clone this repository

        $ git clone https://wwwin-github.cisco.com/gve/gve_devnet_meraki_client_rssi_monitor.git

4. Access the folder `gve_devnet_meraki_client_rssi_monitor`

        $ cd gve_devnet_meraki_client_rssi_monitor

5. Install the dependencies:

        $ pip install -r requirements.txt

6. Open the `.env` file and fill out the following environment variables: 
```
API_KEY=<your-meraki-api-key>
ORG_NAME=<your-organisation-name>
NET_NAME=<your-network-name>
```

> The Meraki API key can be found in the Meraki dashboard, under `My Profile > API access`.
   

## Usage

1. To launch the app, type the following command in your terminal:

        $ python3 app.py

## Workflow

![/IMAGES/workflow.jpg](/IMAGES/workflow.jpg)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
