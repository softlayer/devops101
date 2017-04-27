# deltaNiner

## Basic Steps
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
