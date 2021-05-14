---
title: Deploy a Lambda@Edge function to serve based on devices 
weight: 2
---

In this step, you will find and deploy serverless applications that have been published to the AWS Serverless Application Repository, the application serves content based on device type, for example, mobile device will be forwarded to access content for mobile devices, desktop device will be forwarded to access specific content, and so on so forth


## Deploy an application in SAR

To find and configure an application in the AWS Serverless Application Repository

1. Open [the AWS Serverless Application Repository page](https://serverlessrepo.aws.amazon.com/applications)
2. Check **Show apps that create custom IAM roles or resource policies**
3. Search the application name **serving-based-on-device**, choose the application
4. On the application detail page, check **I acknowledge that this app creates custom IAM roles**
5. Choose **Deploy**. After the deployment is completed, it will redirect to application over page

## Deploy resources by CDK
To download CloudFront+ code and upload it onto CloudShell
> Skip this step if you already have the codes in CloudShell
1. Go to [CloudFront+ code](https://github.com/awslabs/aws-cloudfront-extensions)
2. Choose **Download ZIP**
   ![Github Download ZIP](/images/gh-download.png)
3. Upload the zip package onto CloudShell
   ![CloudShell Upload](/images/cs-upload.png)
4. Unzip the package into home folder

       unzip aws-cloudfront-extensions-main.zip
   {{% notice note %}}
   You can also clone the codes by SSH or Https.
   {{% /notice %}}
   > For SSH, you will need to setup the ssh key in your github account by following this [doc](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

   > For Https, you will need to enter the username and password. If you have enabled two-factor authentication(2FA), a [personal access key](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) is needed to download the codes


To deploy the demo website
1. Go to [CloudShell](https://console.aws.amazon.com/cloudshell/home?region=us-east-1#)
   > In the top right corner of the console, make sure you’re using this region: **N. Virginia (us-east-1)** 
    
2. Navigate to demo folder and deploy it, you need to specify an unique S3 bucket name to store the website content
       
       cd aws-cloudfront-extensions-main/templates/workshop-demo/
       npm install
       npm run build
       cdk deploy --parameters staticSiteBucketName=<your_unique_S3_bucket_name>
   Wait until the deployment is completed
3. Go to [CloudFormation console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1), you will see a stack named **WorkshopDemoStack**
4. Choose **WorkshopDemoStack** and click **Outputs** tab, it will show S3 bucket name, demo website url and CloudFront distribution id
   ![Device output](/images/output_device.png)

## Configuration on the S3 bucket 
1. Go to [S3 console](https://s3.console.aws.amazon.com/s3/home?region=us-east-1)
2. Allow public read access for the objects in the S3 bucket because it will be serving as a public website 

   Choose **Edit Block public access**, uncheck **block all public access**

   > Be aware that every object in this bucket will become readable in public


3. Choose **Objects** tab, choose all the files in the bucket and choose **Actions**, choose **Make public**



## Configuration on the CloudFront distribution
1. Open the [CloudFront console](https://console.aws.amazon.com/cloudfront/home#)
2. Choose the distribution that is shown in the outputs 
3. Choose **Behaviors** tab and edit the default cache behavior
4. Do below configuration
   - For **Cache Based on Selected Request Headers**, choose **Whitelist**
   - For **Whitelist Headers**, add 4 custom headers 
     
     CloudFront-Is-Desktop-Viewer 
     
     CloudFront-Is-Mobile-Viewer

     CloudFront-Is-SmartTV-Viewer

     CloudFront-Is-Tablet-Viewer
     
     > Based on the value of the User-Agent header, CloudFront sets the value of four headers to true or false before forwarding the request to your origin

   - For **Object Caching**, choose **Customize**
     
     For Minimum TTL, enter 0
   
     For Maximum TTL, enter 0

     For Default TTL, enter 0
     > This is to disable cache in CloudFront, it will make sure that every request will be reach origin and miss from CloudFront 
    
   - Choose **Yes, Edit** to save the changes

   ![Device CF config](/images/cf-config-device.png)



## Add a CloudFront Trigger to Run the Function

To configure the CloudFront trigger for your function
1. Go to [Lambda console](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions) and choose serving-based-on-device function which is deployed from SAR 
2. Choose **Configuration** tab and choose **Triggers** 
2. Add Trigger and choose **CloudFront**, choose **Deploy to Lambda@Edge**

   ![CF Trigger](/images/CF_trigger.png)

3. On the **Deploy to Lambda@Edge** page, enter the following information:

    - Distribution

      The CloudFront distribution which has been created in the stack

    - CloudFront event

      In the drop-down list, choose **Origin request**

   Choose **Deploy**

   ![Lambda Deploy](/images/deploy_para.png)

4. Wait for the function to replicate. This typically takes several minutes

   You can check to see if replication is finished by going to the [CloudFront console](https://console.aws.amazon.com/cloudfront/) and viewing your distribution. Wait for the distribution status to change from In Progress back to **Deployed**, which means that your function has been replicated



## Test the function

1. Open the demo website url in your PC which is shown in the stack outputs 
   
   It will show **T-Rex Runner for Desktop** and x-cache will be **miss from cloudfront** or **refreshhit from cloudfront**

   ![Device test result desktop](/images/test_desktop.png)
   
2. Open the demo website url in your mobile phone browser or simulate it in your desktop browser
   
   It will show **T-Rex Runner for Mobile** and x-cache will be **miss from cloudfront** or **refreshhit from cloudfront**

   ![Device test result mobile](/images/test_mobile.png)

