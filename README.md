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
ALPHAVANTAGE_API_KEY = "demo"
```

## Usage
Run the python script from the command line:

```py
python app/robo_advisor.py
```