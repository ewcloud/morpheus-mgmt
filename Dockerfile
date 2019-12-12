# Slim Docker multi-stage build
# for morpheus appliance management
# using morpheus cli and pymorpheus

# Build image
FROM python:3.8-slim-buster as build

# Install tools
RUN set -ex \
    && apt-get update \
    && apt-get install --yes --no-install-suggests --no-install-recommends \
        build-essential \
        ruby-dev \
        rubygems
 
# Install Morpheus CLI (see https://github.com/gomorpheus/morpheus-cli)
ARG MORPHEUS_CLI_VERSION=4.1.7   
RUN set -ex \
    && gem install rake \
        morpheus-cli:${MORPHEUS_CLI_VERSION}

#
# Run-time image.
#
FROM python:3.8-slim-buster

# Copy Python run-time and ECMWF softwate.
COPY --from=build /usr/local/bin/morpheus /usr/local/bin/morpheus
COPY --from=build /var/lib/gems/ /var/lib/gems/

# Install run time dependencies
# and tools for easy access to code repos.
# Delete resources after installation.
RUN set -ex \
    && apt-get update \
    && apt-get install --yes --no-install-suggests --no-install-recommends \
        ruby \
        rubygems \
        git \
        wget \
        curl \
        make \
    && rm -rf /var/lib/apt/lists/*

# Install Python run-time dependencies.
COPY requirements.txt /root/
RUN set -ex \
    && pip install -r /root/requirements.txt

# Python example application
COPY ./example.py ./

# Patch certifi certificates for certificates 
# issued by 'QuoVadis Global SSL ICA G3'
# https://www.quovadisglobal.com/QVRepository/DownloadRootsAndCRL/QuoVadisGlobalSSLICAG3-PEM.aspx
# (Not sure why this is necessary, since issuer cert can be found in cacert.pem)
COPY certs/QuoVadisGlobalSSLICAG3.pem /root/QuoVadisGlobalSSLICAG3.pem
RUN set -ex \
    && cat /root/QuoVadisGlobalSSLICAG3.pem >> /usr/local/lib/python3.8/site-packages/certifi/cacert.pem

# Display version
CMD morpheus --version

# METADATA
# Build-time metadata as defined at http://label-schema.org
# --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"`
ARG BUILD_DATE
# --build-arg VCS_REF=`git rev-parse --short HEAD`, e.g. 'c30d602'
ARG VCS_REF
# --build-arg VCS_URL=`git config --get remote.origin.url`, e.g. 'https://github.com/eduardrosert/docker-magics'
ARG VCS_URL
# --build-arg VERSION=`git tag`, e.g. '0.2.1'
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
        org.label-schema.name="Morpheus" \
        org.label-schema.description="Morpheus CLI utility and pymorpheus python3 api to interact with Morpheus appliances." \
        org.label-schema.url="https://www.morpheusdata.com" \
        org.label-schema.vcs-ref=$VCS_REF \
        org.label-schema.vcs-url=$VCS_URL \
        org.label-schema.vendor="Morpheus Data" \
        org.label-schema.version=$VERSION \
        org.label-schema.schema-version="1.0"