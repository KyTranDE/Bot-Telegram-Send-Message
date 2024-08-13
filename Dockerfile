FROM python:3.9
RUN gpg --keyserver pgp.mit.edu --recv-keys 54404762BBB6E853 BDE6D2B9216EC7A8 648ACFD622F3D138 0E98404D386FA1D9 F8D2585B8783D481 0E98404D386FA1D9 6ED0E7B82643E131
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C && apt-get update  && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
