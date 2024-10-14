# AI-Powered Photo Album Web Application

This project implements a smart photo album web application that leverages AWS services to enable natural language search capabilities. The application allows users to upload photos, automatically detect labels, and search for images using natural language queries.

## Features

- Upload photos to an S3 bucket
- Automatic label detection using AWS Rekognition
- Natural language search powered by Amazon Lex
- Elasticsearch integration for efficient photo indexing and retrieval
- Serverless architecture using AWS Lambda functions
- API Gateway for RESTful API endpoints
- Frontend hosted on S3 with static website hosting

## Architecture

The application is built using the following AWS services:

- S3: Photo storage and frontend hosting
- Lambda: Serverless compute for indexing and search functions
- Elasticsearch: Photo metadata indexing
- Rekognition: Image label detection
- Lex: Natural language processing for search queries
- API Gateway: RESTful API management
- CloudFormation: Infrastructure as Code (IaC) for resource provisioning
- CodePipeline: Continuous integration and deployment

<img width="500" alt="image" src="https://github.com/user-attachments/assets/cbff50df-2753-4430-bca0-5f6275c9d6a6">


## Implementation Details

### 1. Elasticsearch Setup

I created an Elasticsearch domain named "photos" using the AWS Elasticsearch service to store and index photo metadata.

### 2. Photo Upload and Indexing

- Created an S3 bucket (B2) for photo storage
- Implemented a Lambda function (LF1) called "index-photos"
- Set up a PUT event trigger on the S3 bucket to invoke LF1 when photos are uploaded
- LF1 uses Rekognition to detect labels and indexes the photo metadata in Elasticsearch

### 3. Search Functionality

- Created a Lambda function (LF2) called "search-photos"
- Implemented an Amazon Lex bot with a "SearchIntent" to handle natural language queries
- LF2 uses Lex for query disambiguation and searches the Elasticsearch index for matching photos

### 4. API Layer

- Built an API using API Gateway with two methods:
  - PUT /photos: S3 proxy for photo uploads
  - GET /search?q={query}: Connected to LF2 for photo searches
- Implemented API key authentication
- Generated an SDK for the API

### 5. Frontend Development

- Developed a simple web application for searching photos and uploading new ones
- Integrated the API Gateway SDK for backend communication
- Implemented custom label support during photo uploads
- Hosted the frontend on an S3 bucket configured for static website hosting

### 6. CI/CD Pipeline

- Created two AWS CodePipeline pipelines:
  - P1: Builds and deploys Lambda function code
  - P2: Builds and deploys frontend code to S3

### 7. Infrastructure as Code

- Developed a CloudFormation template (T1) to represent all infrastructure resources and permissions

## Getting Started

1. Clone this repository
2. Deploy the CloudFormation template to create the necessary AWS resources
3. Set up the CodePipeline pipelines for automated deployments
4. Access the frontend using the S3 static website URL

## Usage

- Upload photos using the web interface
- Search for photos using natural language queries (e.g., "Show me photos with dogs and cats")
- View search results and manage your photo collection

## Future Improvements

- Implement user authentication and personal photo collections
- Add support for video indexing and searching
- Enhance the frontend with additional features like photo editing and sharing

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/34013391/4d62a865-0274-4d59-9b40-6f8d538b5a73/Homework-Assignment-3.pdf
