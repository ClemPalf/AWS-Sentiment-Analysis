# AWS-Sentiment-Analysis

The goal is to build a simple web page which a user can use to enter a movie review. The web page will then send the review off to a RNN deployed model which will predict the sentiment of the entered review.   
  
<p align="center">
  <img src="https://github.com/ClemPalf/SageMaker-case-studies/blob/560ae3e7ff253478ee2cb92e6be8fc9cf21cce73/Sentiment-analysis/images/Test_1.png"/>
</p>  
  
## Setup Instructions

The notebooks provided in this repository are intended to be executed using Amazon's SageMaker platform. The following is a brief set of instructions on setting up a managed notebook instance using SageMaker, from which the notebooks can be completed and run.

### Log in to the AWS console and create a notebook instance

Log in to the AWS console and go to the SageMaker dashboard. Click on 'Create notebook instance'. The notebook name can be anything and using ml.t2.medium is a good idea as it is covered under the free tier. For the role, creating a new role works fine. Using the default options is also okay. Important to note that you need the notebook instance to have access to S3 resources, which it does by default. In particular, any S3 bucket or objectt with sagemaker in the name is available to the notebook.

### Use git to clone the repository into the notebook instance

Once the instance has been started and is accessible, click on 'open' to get the Jupyter notebook main page. We will begin by cloning the SageMaker Deployment github repository into the notebook instance. Note that we want to make sure to clone this into the appropriate directory so that the data will be preserved between sessions.
