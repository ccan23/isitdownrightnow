# IsItDownRightNow

This is a simple Python wrapper for the IsItDownRightNow API, allowing users to check in real-time whether a specific website is currently accessible worldwide.

## Installation
```bash
pip install isitdownrightnow
```

## Usage
```py
from isitdownrightnow import IsItDownRightNow

# Create an instance for a website
checker = IsItDownRightNow('google.com')

# Get the status of the website
status = checker.status
print(status)
```

```py
{
    'up': True, 
    'website_name': 'Google', 
    'url_checked': 'www.google.com',
    'response_time_ms': 16.73,
    'last_down': 'More than a week ago', 
    'down_for': None, 
    'status': 'UP', 
    'message': 'Google.com is UP and reachable by us.'
}
```

## Simple Overview

The main class in the wrapper is IsItDownRightNow. Here's a brief overview of its methods and properties:

**Public Methods and Properties:**
* **status:** Returns a dictionary containing the status of the website.

**Attributes:**
* **domain:** The domain name of the site to be checked.

___

**Returns**

For the status method, you can expect a dictionary with the following structure:

* **up** (bool): True if the domain is up, False otherwise.

* **website_name** (str): The name of the website.

* **url_checked** (str): The URL that was checked.

* **response_time** (str): The response time of the website.

* **last_down** (str): The last time the website was down (None if the website is down).

* **down_for** (str): The duration of time the website has been down (None if the website is up).

* **status** (str): The status of the website, either "UP" or "DOWN".

* **message** (str): A message about the result of the check.
