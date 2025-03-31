FROM python:3.10-bullseye

RUN pip install --upgrade pip

WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"
COPY src/ /app/
RUN pip3 install -r requirements.txt
RUN mkdir $HOME/.oci
RUN touch $HOME/.oci/config

ENTRYPOINT ["streamlit", "run", "MyGPT.py", "--server.port", "8080"]


