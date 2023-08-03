FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV DB_URI=sqlite:///app.db
ENV ADMIN_USERNAME=dispenser
ENV ADMIN_PASSWORD=admin
ENV JWT_SECRET=supersecretjwtsecretissecret


CMD ["python3", "run_dev.py"]