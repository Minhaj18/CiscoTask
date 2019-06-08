FROM python:2.7
ADD macaddress_rest_api.py /
RUN pip install requests
RUN pip install boto3
RUN pip install botocore
RUN pip install awscli
WORKDIR /
RUN chmod 777 macaddress_rest_api.py
ENTRYPOINT ["python","macaddress_rest_api.py"]

