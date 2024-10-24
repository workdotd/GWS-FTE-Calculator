# Copyright (C) 2022 CBRE, Inc. All rights reserved.
FROM python:3.8-slim-buster

RUN groupadd -g 1001 mygroup && \
    useradd -u 1001 -g mygroup -d /usr/src/app -m myuser

RUN mkdir -p /usr/src/app && chown myuser:mygroup /usr/src/app

 
WORKDIR /usr/src/app

ARG MODEL_FILE
ENV MODEL_FILE ${MODEL_FILE}


ADD requirements.txt /usr/src/app

RUN apt-get update
RUN apt-get install -y libgomp1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD main.py /usr/src/app
COPY FTE_Calc_wc.pkl /usr/src/app/FTE_Calc_wc.pkl
COPY dbconn.py /usr/src/app/dbconn.py
COPY FTE_TargetEncoderwc.py /usr/src/app/FTE_TargetEncoderwc.py
COPY Inputs.xlsx /usr/src/app/Inputs.xlsx

RUN chown -R myuser:mygroup /usr/src/app

USER myuser

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]
