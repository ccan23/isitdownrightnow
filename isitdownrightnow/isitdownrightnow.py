#!/usr/bin/env python3

import requests
from urllib.parse import urlparse
import validators
from lxml import html


class IsItDownRightNow:
    """
    A class for checking whether a website is down or not.

    Usage:

        isdown = IsItDownRightNow('google.com')
        isdown.status

    Public Methods:

        status -> dict
            Returns a dictionary containing the status of the website.

    Private Methods:

        __validate_domain() -> bool:
            Returns the valid domain to check on isitdownrightnow.com

        __get_response() -> dict:
            Retrieves the HTML response from isitdownrightnow.com

        __scrape(html_text: str) -> dict:
            Scrapes the response from the html text and returns a dictionary.
    """

    __version__ = '0.0.1'

    def __init__(self, domain: str):
        """
        Creates a new instance of IsItDownRightNow

        Args:

            domain : str
                The domain name of the site to be checked

        Private Attributes:

            __response : dict
                Return __get_response()
        """

        self.__domain = domain
        self.__response = self.__get_response()

    def __repr__(self) -> str:
        """
        Return a string representation of the IsItDownRightNow object.

        Returns:
            str: 
                A string that contains the constructor call for the IsItDownRightNow object.
        """

        domain = self.__valid_domain
        return f"IsItDownRightNow('{domain}')" if domain else 'IsItDownRightNow()'
    
    @property
    def __valid_domain(self) -> str:
        """
        Returns the valid domain to check on isitdownrightnow.com

        Returns:
            str:
                The domain name extracted from the URL, if valid.
        """

        if validators.domain(self.__domain):
            return self.__domain
        
        elif validators.url(self.__domain):
            return urlparse(self.__domain).netloc
        
        else:
            return ''
        
    def __get_response(self) -> dict:
        """
        Sends a request to isitdownrightnow.com and returns the response.

        Returns:
            dict:
                A dictionary with information about the website's status.
        """

        # Valid domain to send isitdownrightnow.com
        domain = self.__valid_domain
        
        # URL to send request to isitdownrightnow.com
        url = f'https://www.isitdownrightnow.com/check.php?domain={domain}'
        
        # Check if the domain is valid or empty string
        if domain:

            # Get the response from istidownrightnow.com
            response = requests.get(url)

            # Check if isitdownrightnow.com is reachable
            if response.ok:

                # Wrap response text with <html> and <body> tags
                html_text = f'<html><body>{response.text}</body></html>'

                # Return response and wrapped html text
                return {
                    'status': response.ok,
                    'status_code': response.status_code,
                    'html_text': html_text
                }

            else:
                # Return an error message if isitdownrightnow.com is not reachable
                return {
                    'status': response.ok,
                    'status_code': response.status_code,
                    'message': 'isitdownrightnow.com is not reachable'
                }
        
        else:
            # Return an error message if the domain is invalid
            return {
                'status': False,
                'message': f'{self.__domain} is not a valid domain. Usage examples: google.com, speedtest.net, etc..'
            }
    
    def __scrape(self, html_text: str) -> dict:
        """
        Parses the HTML text returned by isitdownrightnow.com and returns the website's status.

        Args:
            html_text : str
                The HTML text returned by isitdownrightnow.com

        Returns:
            dict:
                A dictionary containing the following keys:
                'up' (bool), 'website_name' (str), 'url_checked' (str),
                'response_time' (str), 'last_down' (str or None), 'down_for' (str or None),
                'status' (str), 'message' (str)
        """

        # Use element tree to find elements from string
        tree = html.fromstring(html_text)

        # Lambda function to parse text from HTML element using xpath locations
        text_element = lambda index, tag: tree.xpath(f'/html/body/div[{index}]/{tag}')[0].text

        website_name  = text_element(1, 'span')
        url_checked   = text_element(2, 'span')
        response_time = text_element(3, 'span')
        down_status   = text_element(4, 'b')
        down_response = text_element(4, 'span')
        status        = text_element(5, 'span')
        message       = text_element(5, 'div') 

        return {
            'up'              : True if status == 'UP' else False,
            'website_name'    : website_name,
            'url_checked'     : url_checked,
            'response_time_ms': float(response_time[:-4]) if response_time != 'no response' else response_time,
            'last_down'       : down_response if down_status == 'Last Down:' else None,
            'down_for'        : down_response if down_status == 'Down For:' else None,
            'status'          : status,
            'message'         : message
        }
    
    @property
    def status(self) -> dict:
        """
        Check if the given domain is up or down and return relevant information.

        Returns:
            dict:
                - 'up' (bool)          : True if the domain is up, False otherwise.
                - 'website_name' (str) : The name of the website.
                - 'url_checked' (str)  : The URL that was checked.
                - 'response_time' (str): The response time of the website.
                - 'last_down' (str)    : The last time the website was down, it is None if website is down
                - 'down_for' (str)     : The duration of time the website has been down, it is None if website is up
                - 'status' (str)       : The status of the website, either "UP" or "DOWN"
                - 'message' (str)      : A message about the result of the check.
        """

        if self.__response['status']:
            return self.__scrape(self.__response['html_text'])
        
        else:
            return self.__response