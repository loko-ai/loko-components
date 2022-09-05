FROM python:3.6-slim
ARG user
ARG password
ADD requirements.lock /
RUN pip install --upgrade --extra-index-url https://$user:$password@distribution.livetech.site -r /requirements.lock
ADD . /loko-components
ENV PYTHONPATH=$PYTHONPATH:/loko-components
WORKDIR /loko-components/loko_components/services
CMD python services.py
