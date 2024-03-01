# Base image -> https://github.com/runpod/containers/blob/main/official-templates/base/Dockerfile
FROM runpod/base:0.4.0-cuda11.8.0

# Python dependencies
RUN mkdir /model
COPY ./model/mistral-7b-it-emails ./model/mistral-7b-it-emails
COPY builder/requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade --default-timeout=3000 -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files (Worker Template)
ADD src .

CMD python3.11 -u /handler.py
