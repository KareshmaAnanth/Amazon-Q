#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import Eventbridge
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Lex
from diagrams.aws.integration import SNS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.general import Users
from diagrams.onprem.client import Client

# Create a custom node for Amazon Bedrock (since it might not be in the library yet)
from diagrams.aws.ml import _ML
class Bedrock(_ML):
    _icon = "sagemaker.png"  # Using SageMaker icon as a placeholder

# Set the output file name and diagram attributes
output_file = "devops_chatops_architecture"
with Diagram("DevOps ChatOps Bot Architecture", show=False, filename=output_file, outformat="png"):
    
    # Define users and chat platforms
    with Cluster("Users & Platforms"):
        users = Users("DevOps Team")
        slack = Client("Slack")
        teams = Client("MS Teams")
    
    # Define the API Gateway for external communication
    api = APIGateway("API Gateway")
    
    # Define the core ChatOps components
    with Cluster("ChatOps Core"):
        lex = Lex("Amazon Lex\nIntent Recognition")
        
        with Cluster("Event Processing"):
            events = Eventbridge("EventBridge\nEvent Router")
            
        with Cluster("Processing & Logic"):
            command_lambda = Lambda("Command\nProcessor")
            response_lambda = Lambda("Response\nFormatter")
            
        with Cluster("AI Engine"):
            bedrock = Bedrock("Amazon Bedrock\nAI/ML Models")
    
    # Define monitoring and notification components
    with Cluster("Monitoring & Alerts"):
        cloudwatch = Cloudwatch("CloudWatch\nMetrics & Logs")
        alerts = SNS("SNS\nAlerts & Notifications")
    
    # Define data storage
    with Cluster("Data Storage"):
        logs = S3("Conversation\nLogs")
        
    # Connect the components with arrows to show the flow
    users >> slack >> api
    users >> teams >> api
    
    api >> lex
    lex >> events
    
    events >> command_lambda
    command_lambda >> bedrock
    bedrock >> response_lambda
    response_lambda >> api
    
    # Monitoring flows
    command_lambda >> cloudwatch
    response_lambda >> cloudwatch
    cloudwatch >> alerts >> slack
    
    # Logging flows
    command_lambda >> logs
    response_lambda >> logs
    
    # Feedback loop
    api >> Edge(color="firebrick", style="dashed") >> cloudwatch

print(f"Diagram created: {output_file}.png")
