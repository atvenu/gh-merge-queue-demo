ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# Install service dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service source code and tests
COPY . .

# Directory for JUnit test results
RUN mkdir -p /app/reports

CMD ["pytest", "--junitxml=/app/reports/simple-calculator-test-results.xml"]
