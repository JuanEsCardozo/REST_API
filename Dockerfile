FROM python:3.12

WORKDIR /code

COPY ./single-odyssey-404518-d3e05ea7c215.json /code/

# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/code/single-odyssey-404518-d3e05ea7c215.json

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
   curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && \
   apt-get update -y && \
   apt-get install google-cloud-sdk -y && \
   gcloud auth activate-service-account --key-file=/code/single-odyssey-404518-d3e05ea7c215.json && \
   gcloud config set project single-odyssey-404518

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app.py /code

COPY ./config.py /code

EXPOSE 5000

CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "5000"]
