# Introduction
This repository contains some useful scripts to use while supporting the Help Desk during the daily customer care job, mainly focused on the "Bonus Vacanze" initiative.

So far there 2 scripts:
- **get_prifile.py** => returns the user profiles givend his/her email or fiscal code
- **get_bonus.py** => returns the bonus activation json given the user's fiscal code.

## Setup

- Clone the repository:
```
>> git clone git@github.com:pagopa/bonus_vacanze_support.git
```
- Create python virtual environment:

```
>> cd bonus_vacanze_support
>> python3 -m venv .venv
```
- Activate the virtual environment:

```
>> source .venv/bin/activate
```
- Install the required dependencies

```
>> pip install -r requirements.txt
```

- Create a hidden file called .env
```
>> touch .env
```
- edit the .env file and fill the values of the following keys:

```
# io-p-cosmos-api
COSMOS_API_ENDPOINT='<cosmos db url>'
COSMOS_API_KEY='<cosmos db key>'

# io-p-cosmos-bonus
COSMOS_BONUS_ENDPOINT='<cosmos db url>'
COSMOS_BONUS_KEY='<cosmos db key>'
```

## Run the scripts

- Get user profile by email or fiscal code.

```
>> python get_profile.py -e <user email > # case sensitive
```

```
>> python get_profile.py -f <user fiscal code> # no case sensitive
```

- Get bonus by fiscal code:

```
>> python get_bonus.py -f <user fiscal code>
```
