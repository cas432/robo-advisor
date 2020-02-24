# "Robo Advisor" Project

[Project Description](https://github.com/prof-rossetti/intro-to-python/tree/master/projects/robo-advisor)


## Instalatiion

Fork this  [repository](https://github.com/cas432/robo-advisor) from Github and then clone your fork to download it locally onto your computer. Then navigate there from the command line:

```sh
cd robo-advisor
```

## Setup

### Environment Setup
Setup the virtual environment "stocks-env":

```sh
conda create -n stocks-env python=3.7 #(first time only)
conda activate stocks-env
```
### Package Installation
Please install all packages from the requirements.txt file:

```sh
pip install -r requirements.txt
```

### Setup Environment Variable

Before using or developing this application, take a moment to [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key).

After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

```sh
ALPHAVANTAGE_API_KEY = "xxx"
```

Additionally, in order to receive SMS updates, you must [sign up for a Twilio account](https://www.twilio.com/try-twilio). Click the link in the confiration email to verify your account and confirm the code sent to your phone. 

Then, create a new project with "Programmable SMS" capabilities. From the console you can view the project's Account SID and Auth Token. Make sure to update the contents of the ".env" file to specify these values as environment variable.

```sh
TWILIO_ACCOUNT_SID = "xxx"
TWILIO_AUTH_TOKEN = "xxx"
```

To receive a Twilio phone number to send the messages from click [here](https://www.twilio.com/console/sms/getting-started/build). Then update the contents of the ".env" variable.

```sh
SENDER_SMS= "xxx"
```

Lastly, set an environent variable to specify the intended recipient's phone number (including the plus sign at the beginning)

```sh
RECIPIENT_SMS= "xxx"
```


## Usage
Run the python script from the command line:

```py
python app/robo_advisor.py
```