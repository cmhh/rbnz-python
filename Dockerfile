FROM ubuntu:23.04

ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && \
  apt-get -y dist-upgrade && \
  apt-get --no-install-recommends -y install \
    wget curl unzip gdebi ca-certificates python3 python3-pip python3-venv && \ 
  wget --quiet \
    https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_112.0.5615.165-1_amd64.deb \
    -O chrome.deb && \
  wget --quiet \
    https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip && \
  gdebi --non-interactive chrome.deb && \
  unzip chromedriver_linux64.zip && \
  mv chromedriver /usr/local/bin/ && \
  rm /chrome* && \
  python3 -m venv $VIRTUAL_ENV && \
  python3 -m pip install --upgrade pip && \
  pip install selenium requests pandas openpyxl 

COPY scrape.py /
COPY browser.py /

RUN chmod ugo+x /scrape.py

ENTRYPOINT ["python", "scrape.py"]