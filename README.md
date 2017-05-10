# deltaNiner aka Devops101

This project is a simple Bluemix catalog powered by elastic search, with the ability to add comments and tags to services if you like that sort of thing. Mostly it exists as a way to demonstrate how to deploy a Flask app to Bluemix, and how to use some of the DevOps services.

## Deploy Automagically
1. Press this button: [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/softlayer/devops101)
2. Make sure your toolchain and application name are set to something you want.
3. Make sure your application has deployed. This might require you to manually run the toolchain on the first deploy.
4. Add monitoring to your toolchain. 
5. Add a Scripted test, and upload the deltaNiner/test/Selenium/devops101-SE-Tests.html file. 
6. To populate the ElasticSearch DB, go to https://yourapp/search , you should be prompted to enter your SSO key (link provided on how to get that). 

### No SSO key 
If you don't have an SSO key, you can add BM_USER and BM_PASSWORD environmental variables to your environment. And then do the following:

1. cf ssh YOURNAMEHERE
2. cd app
3. source .profile.d/python.sh
4. .cloudfoundry/python/bin/python bin/getBMServices.py

## Basic MANUAL Steps
1. get a bluemix log
2. cf login --sso (for sso accounts) 
3. cf create-service compose-for-elasticsearch Standard  YOURNAMEHERE-ES
4. cf push YOURNAMEHERE -b https://github.com/cloudfoundry/buildpack-python.git
5. cf bind-service YOURNAMEHERE YOURNAMEHERE-ES
6. cf push YOURNAMEHERE -b https://github.com/cloudfoundry/buildpack-python.git
7. Add environment variables for CF
8. cf ssh YOURNAMEHERE
9. cd app
10. source .profile.d/python.sh
11. .cloudfoundry/python/bin/python bin/getBMServices.py



## Devops Steps
1. Enable devops in portal. Integrate with github, track deployment of code changes
2. Change Deploy job to add "-b https://github.com/cloudfoundry/buildpack-python.git"

## Monitoring
1. Monitoring should be enabled already
2. Add a new synthetic test
3. Test a specific URL
4. Upload Selenium Test - NOt sure why GIt integration doesn't work
