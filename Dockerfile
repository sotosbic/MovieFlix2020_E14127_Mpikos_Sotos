FROM python 
ADD . /data
WORKDIR /data
RUN pip install -r requirements.txt