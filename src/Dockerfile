FROM 3.10.14-bookworm

WORKDIR /usr/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $PYTHONPATH:$PWD

RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/
RUN pip install -r requirements.txt

COPY . /usr/src/app
RUN chmod +x ./entrypoints/*