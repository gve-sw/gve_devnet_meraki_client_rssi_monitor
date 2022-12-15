# gve_devnet_meraki_client_rssi_monitor
This prototype provides the user with a report of historical signal qualities seen by both AP and Client, with a focus on the RSSI metric. This use case is ideal for troubleshooting in scenarios such as sticky clients. 

## Contacts
* Jordan Coaten

## Solution Components
* Python 3.9 
* Meraki SDK
* Pandas
* Meraki MR with wireless clients

## Workflow

![/IMAGES/workflow.jpg](/IMAGES/Meraki_RSSI_Workflow.png)

## Installation/Configuration
The following commands are executed in the terminal.

1. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). 


2.	(Optional) Create and activate a virtual environment - once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).  
    ```
    python3 -m venv [add name of virtual environment here] 
    source [add name of virtual environment here]/bin/activate
    ```
  * Access the created virtual environment folder
    ```
    cd [add name of virtual environment here] 
    ```

3. Clone this Github repository:  
        ```
         git clone [add github link here]
        ```
  * For Github link: 
      In Github, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  
      ![/IMAGES/giturl.png](/IMAGES/giturl.png)
  * Or simply download the repository as zip file using 'Download ZIP' button and extract it


4. Access the downloaded folder:  
        ```cd gve_devnet_meraki_client_rssi_monitor```
    

5. Install all dependencies:  
        ```pip install -r requirements.txt```
  

6. Follow the instructions under https://developer.cisco.com/meraki/api/#!authorization/obtaining-your-meraki-api-key to obtain the Meraki API Token. Save the token for a later step.


    > The Meraki API key can be found in the Meraki dashboard, under `My Profile > API access`.


7. Open the `.env` file and fill out the following environment variables: 
   ```
   API_KEY=<your-meraki-api-key>
   ORG_NAME=<your-organisation-name>
   NET_NAME=<your-network-name>
   SSID=<your-SSID>
   ```
   

## Usage

1. To launch the app, type the following command in your terminal:

        $ python3 app.py

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
