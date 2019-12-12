# Morpheus Management
[Morpheus CLI](https://github.com/gomorpheus/morpheus-cli) and [pymorpheus](https://pypi.org/project/pymorpheus) python client packaged in a docker container for simplified management of your [Morpheus](https://www.morpheusdata.com/) appliance.

This docker image ``eduardrosert/morpheus-mgmt`` provides an environment to work with shell scripts using the [Morpheus command line interface](https://github.com/gomorpheus/morpheus-cli) and python scripts using the [pymorpheus python client](https://pypi.org/project/pymorpheus) to set up and manage your [Morpheus](https://www.morpheusdata.com/) appliance.

## Run using docker
The pre-built image ``eduardrosert/morpheus-mgmt`` is available on [Dockerhub](https://hub.docker.com/r/eduardrosert/morpheus-mgmt). If you already have Docker running on your machine, just do the following to run the image:
```bash
docker run --rm eduardrosert/morpheus-mgmt
```
This will output version of the morpheus cli installed, e.g.:
```
4.1.7
```

## Run interactive shell
To run this image interactively, run
```bash
docker run --rm -it eduardrosert/morpheus-mgmt bash
```
Now you can use the cli, e.g:
```bash
morpheus --version
```

## Run python api example
The docker image provides a python example application that allows you to connect to your appliance and list existing instances.

### Display example.py help
```bash
docker run --rm -it eduardrosert/morpheus-mgmt ./example.py --help
```
Example output:
```
usage: example.py [-h] [-m https://morpheus.example.com] [-s {true,false}] [-u <username>] [-t <api access token>]

Example application to test your connection to a Morpheus appliance using the pymorpheus Morpheus API client.

optional arguments:
  -h, --help            show this help message and exit
  -m https://morpheus.example.com, --morpheus-url https://morpheus.example.com
                        the url of your morpheus instance. Can be provided by the environment variable 'MORPHEUS_URL'.
  -s {true,false}, --ssl-verify {true,false}
                        verify SSL certificate (default: true). Can be provided by the environment variable
                        'MORPHEUS_SSLVERIFY'.
  -u <username>, --user <username>
                        your morpheus username. For subtenant accounts please use '<subtenancy>\<username>' as username,
                        e.g. -u 'mysubt\janedoe'. Make sure to escape the backslash by using quotes around the username
                        or double backslash when passing as a command line argument in shell!
  -t <api access token>, --access-token <api access token>
                        your morpheus api access token. When an api access token is provided, username (and password)
                        are ignored. To generate an acess token, log on to your morpheus appliance using the web
                        interface, go to 'User Settings' and click on 'API ACCESS'.
```
### Run the example
To run the python example included in the docker image, run:
```bash
docker run --rm -it eduardrosert/morpheus-mgmt ./example.py
```
You will be prompted to provide the morpheus appliance url, your username and your password. The example will return a json of your instances, with a yaml overview in the end:
```
{'instances': [{'accountId': 1,
                'autoScale': False,
                'cloud': {'id': 42, 'name': 'planet-sized-supercomputer'},

               ...

               }],
 'meta': {'max': 25, 'offset': 0, 'size': 4, 'total': 4}}
# --- Instances ---
-
  Name: bistromath
  IP: "10.10.0.10"
  Status: running
  CreatedBy: fperfect

-
  Name: heart-of-gold
  IP: "10.10.0.11"
  Status: stopped
  CreatedBy: zbeeblebrox

...
```


## Connect using an access token
You can use the ``--access-token`` command line option to connect to your appliance:
```bash
 docker run --rm -it eduardrosert/morpheus-mgmt ./example.py --morpheus-url https://morpheus.example.com --access-token <your morpheus api access token>
```
Alternatively you can set the ``MORPHEUS_API_ACCESS_TOKEN`` environment variable, e.g.:
```bash
docker run --rm -it --env MORPHEUS_API_ACCESS_TOKEN=<your morpheus api access token> eduardrosert/morpheus-mgmt ./example.py --morpheus-url https://morpheus.example.com
```

## Fixing Problems with SSL certificates
If you run into ssl errors when connecting to your appliance, or you use self-signed certificates, you might need to add ``--ssl-verify false`` (this is not generally recommended!):
```bash
docker run --rm -it eduardrosert/morpheus-mgmt ./example.py --ssl-verify false
```
A better solution is to add your certificate to the list of accepted certificates of the ``certifi`` python module. To do that, run python interactive shell:
```bash
python3 -c "import certifi; print (certifi.where())"
```
This will output the path of the accepted certificate authorities, e.g.:
```
/usr/local/lib/python3.8/site-packages/certifi/cacert.pem
```
You can now add you own certificate to that list, e.g.:
```bash
cat MyCustomCertificate.pem >> /usr/local/lib/python3.8/site-packages/certifi/cacert.pem
```
To permanently patch the docker image you need to create your own custom docker image based on ``eduardrosert/morpheus-mgmt``, e.g.:
```Dockerfile
FROM eduardrosert/morpheus-mgmt
COPY ./patched_cacert.pem /usr/local/lib/python3.8/site-packages/certifi/cacert.pem
CMD python ./example.py --help
```