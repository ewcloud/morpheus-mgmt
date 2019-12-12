#!/usr/bin/env python3
# Example application to test your connection to a Morpheus appliance using the pymorpheus Morpheus API client.
# see https://docs.morpheusdata.com/en/3.6.4/api/includes/_provisioning.html
#
# requires python3
# requires pymorpheus (https://pypi.org/project/pymorpheus/):  pip install pymorpheus==0.1.5
#
# You can set the following environment variables before running this script:
#    MORPHEUS_API_ACCESS_TOKEN=<your morpheus api access token>
#    MORPHEUS_URL=<morpheus service url, e.g. https://morpheus.example.com>
#    MORPHEUS_SSLVERIFY=<'true' to verify ssl cert, or 'false'>

import os
import json
import pprint
import sys
import getpass
import argparse

import pymorpheus

parser = argparse.ArgumentParser(
    description='Example application to test your connection to a Morpheus appliance using the pymorpheus Morpheus API client.',
    add_help=True)

parser.add_argument('-m', '--morpheus-url',
                    metavar="https://morpheus.example.com",
                    dest='url',
                    type=str,
                    required=False,
                    help="the url of your morpheus instance. Can be provided by the environment variable 'MORPHEUS_URL'.")

parser.add_argument('-s', '--ssl-verify',
                    choices=["true", "false"],
                    dest='sslverify',
                    default="true",
                    type=str,
                    required=False,
                    help="verify SSL certificate (default: true). Can be provided by the environment variable 'MORPHEUS_SSLVERIFY'.")

parser.add_argument('-u', '--user',
                    metavar="<username>",
                    dest='username',
                    type=str,
                    required=False,
                    help="your morpheus username. For subtenant accounts please use '<subtenancy>\\<username>' as username, e.g. -u 'mysubt\\janedoe'. Make sure to escape the backslash by using quotes around the username or double backslash when passing as a command line argument in shell!")

parser.add_argument('-t', '--access-token',
                    metavar="<api access token>",
                    dest='token',
                    type=str,
                    required=False,
                    help="your morpheus api access token. When an api access token is provided, username (and password) are ignored. To generate an acess token, log on to your morpheus appliance using the web interface, go to 'User Settings' and click on 'API ACCESS'.")

def main(username, password, morpheusUrl, token, sslverify=True):
    c = None #client
    if not token is None:
        # use the provided token
        c = pymorpheus.MorpheusClient(morpheusUrl, token=token, sslverify=sslverify)
    else:
        # use username password
        c = pymorpheus.MorpheusClient(morpheusUrl, username=username, password=password, sslverify=sslverify)

    req = {
        "name" : "*"
    }

    res = c.call(
        'get',
        'instances',
        jsonpayload=json.dumps(req)
    )
    pprint.pprint(res)

    #try read json to dict
    print ("# --- Instances ---")
    if 'instances' in res and len(res['instances']) > 0:
        for instance in res['instances']:
            print("-\n  Name: {}\n  IP: \"{}\"\n  Status: {}\n  CreatedBy: {}\n".format(
                instance['name'],
                instance["connectionInfo"][0]['ip'],
                instance["status"],
                instance['createdBy']['username']) )
    else:
        print("No instances found.")

if __name__ == '__main__':

    # try read from env
    username=None
    password = None
    token = os.environ.get('MORPHEUS_API_ACCESS_TOKEN', None)
    url = os.environ.get('MORPHEUS_URL', None)
    sslverify = False if os.environ.get('MORPHEUS_SSLVERIFY', "true").lower() == "false" else True

    # override env from explicit command line options
    args = parser.parse_args()
    if args.sslverify is not None:
        sslverify = False if args.sslverify == "false" else True

    if args.url is not None:
        url = args.url

    if args.username is not None:
        username = args.username

    if args.token is not None:
        token = args.token
    
    # read unset/empty vars from stdin
    if url in (None, ""):
        url=input("Morpheus URL (e.g. 'https://morpheus.example.com'): ")
    if token is None:
        # only ask for username and password if no access token was provided
        if username in (None, ""):
            username=input("Username (for subtenant accounts please login with '<subtenancy>\\<username>'): ")
        
        if password in (None, ""):
            password=getpass.getpass("Password for user '{}': ".format(username))

    if token is None:
        print("Connecting to '{0}' with user '{1}' ...".format(url, username))
    else:
        print("Connecting to '{0}' with token '{1}' ...".format(url, token))
    sys.exit(main(username=username, password=password, morpheusUrl=url, token=token, sslverify=sslverify))