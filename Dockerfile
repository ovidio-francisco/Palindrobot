FROM python:3.7-alpine

COPY bots/config.py /bots/

COPY bots/retweet.py /bots/
COPY bots/palindrome.py /bots/
COPY bots/palindromer.py /bots/
COPY bots/peers.py /bots/

copy bots/seen.txt /bots/	
copy bots/white_list.txt /bots/	


COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt


WORKDIR /bots
CMD ["python3","retweet.py"]



