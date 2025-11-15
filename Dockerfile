FROM python:3.12
WORKDIR /home/chen/LaptopParser/project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY back_front/ ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
