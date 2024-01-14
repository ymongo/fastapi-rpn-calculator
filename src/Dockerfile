# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./../requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./src/app /code/src/app

# 
CMD ["uvicorn", "src.app.api.main:app", "--host", "0.0.0.0", "--port", "5005", "--reload"]