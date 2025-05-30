#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.devtools import Codebuild, Codepipeline
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.vcs import Github

# Set the output file name and format
output_file = "aws_cicd_architecture"
output_format = "png"

# Create the diagram
with Diagram("AWS CI/CD Pipeline Architecture", 
             filename=output_file, 
             outformat=output_format, 
             show=False):
    
    # Define the components
    github = Github("Source Code")
    
    with Cluster("CI/CD Pipeline"):
        pipeline = Codepipeline("CodePipeline")
        build = Codebuild("CodeBuild")
        
    lambda_function = Lambda("Lambda Function")
    
    s3 = S3("Assets Storage")
    
    cloudwatch = Cloudwatch("Monitoring")
    
    # Define the relationships
    github >> pipeline >> build >> lambda_function
    lambda_function >> s3
    cloudwatch >> Edge(style="dotted") >> lambda_function
    cloudwatch >> Edge(style="dotted") >> pipeline
    cloudwatch >> Edge(style="dotted") >> build
