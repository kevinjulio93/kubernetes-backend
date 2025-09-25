# Use an image from the OpenShift / Red Hat registry by default.
# You can override the image at build time by passing --build-arg PYTHON_IMAGE=...
ARG PYTHON_IMAGE=registry.redhat.io/ubi8/python-38:latest
FROM ${PYTHON_IMAGE}
LABEL org.opencontainers.image.source="local"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install minimal build deps needed for some wheels (UBI uses microdnf)
RUN microdnf -y update \
    && microdnf install -y gcc make libffi-devel openssl-devel \
    && microdnf clean all

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY ./app ./app

# create non-root user and set ownership (use useradd/groupadd on UBI)
RUN groupadd -r app && useradd -r -g app app \
    && chown -R app:app /app
USER app

EXPOSE 8000

# default command (override at runtime if needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
