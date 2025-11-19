FROM python:3.12-slim

# create app directory
WORKDIR /app

# copy requirements file
COPY requirements.txt /app/requirements.txt

# install Flask + dependencies
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# copy app source code
COPY . /app

# expose port
EXPOSE 5000

# run the flask server
CMD ["python3", "app.py"]
