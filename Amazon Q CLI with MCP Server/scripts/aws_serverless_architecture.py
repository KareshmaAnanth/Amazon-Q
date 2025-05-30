#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import APIGateway, CloudFront, Route53
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM

# Set the output file name and format
output_file = "/root/Amazon-Q-CLI/MCP-Server/aws-architecture-diagram-generator/diagrams/serverless_architecture"
output_format = "png"

# Create the diagram
with Diagram("AWS Serverless Architecture", 
             filename=output_file, 
             outformat=output_format, 
             show=False):
    
    # Define DNS and CDN components
    route53 = Route53("Route 53\nCustom Domain")
    cdn = CloudFront("CloudFront CDN")
    
    # Define IAM user for access management
    iam_user = IAM("IAM User")
    
    # Define API and compute components
    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        
    with Cluster("Compute Layer"):
        lambda_function = Lambda("Lambda Functions")
    
    # Define storage components
    with Cluster("Storage Layer"):
        dynamodb = Dynamodb("DynamoDB")
        website_bucket = S3("S3\nStatic Website")
    
    # Define the relationships
    route53 >> Edge(label="DNS Resolution") >> cdn
    cdn >> Edge(label="Static Content") >> website_bucket
    cdn >> Edge(label="API Requests") >> api
    api >> lambda_function
    lambda_function >> dynamodb
    lambda_function >> website_bucket
    
    # IAM user permissions and access
    iam_user >> Edge(label="Manages") >> lambda_function
    iam_user >> Edge(label="Configures") >> api
    iam_user >> Edge(label="Administers", style="dashed") >> dynamodb
    iam_user >> Edge(label="Manages Content", style="dashed") >> website_bucket
