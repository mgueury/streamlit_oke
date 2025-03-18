FROM python:3.10-bullseye

RUN pip install --upgrade pip

WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"
COPY src/* /app/
RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit","run", "streamlit.py", "--server.port", "8080"]

