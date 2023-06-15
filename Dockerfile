# Use the Alpine Linux base image
FROM python:3

RUN pip3 install requests && pip3 install pyyaml

COPY . .

ENTRYPOINT [ "python3", "main.py" ]