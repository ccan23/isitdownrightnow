#!/usr/bin/env python3

import requests
from urllib.parse import urlparse
import validators
from lxml import html


class IsItDownRightNow:
    
    def __init__(self, domain: str):

        self.__domain = domain
        self.__response = self.__get_response()

    def __repr__(self) -> str:
        
        domain = self.__valid_domain
        return f"IsItDownRightNow('{domain}')" if domain else 'IsItDownRightNow()'
    
    @property
    def __valid_domain(self) -> str:
        
        if validators.domain(self.__domain):
            return self.__domain
        
        elif validators.url(self.__domain):
            return urlparse(self.__domain).netloc
        
        else:
            return ''
        
    def __get_response(self) -> dict:

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
    def info(self) -> dict:

        if self.__response['status']:
            return self.__scrape(self.__response['html_text'])
        
        else:
            return self.__response