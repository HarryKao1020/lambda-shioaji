FROM public.ecr.aws/lambda/python:3.11

# Install necessary system dependencies for building TA-Lib
RUN yum install -y gcc \
    && yum install -y python3-devel \
    && yum install -y wget tar

# Download and install TA-Lib from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make Install

# Clean up TA-Lib source files
RUN rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Install TA-Lib Python package
RUN pip install TA-Lib

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]


RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzvf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    !./configure --prefix=/usr \ 
    !make
    !make install
    !pip install Ta-Lib