## The "Analytics" application here is handled in two steps:
### Continuous Build process through AWS CodeBuild
1. Create the CodeBuild template on AWS
2. point to the github repository and fill-in with standard values
3. Add the environment variables needed requested from the buildspec.yml file:
- AWS_ACCOUNT_ID : ...
- AWS_DEFAULT_REGION : ...
- IMAGE_REPO_NAME: ...
- IMAGE_TAG: CODEBUILD_BUILD_NUMBER.

CODEBUILD_BUILD_NUMBER this comes automatically from the CodeBuild process. You don't have to define it.

4. Create the policy "FullECRAccess" with the json provided in ECR_policy_config.json, and attach it to the role that is managing the CodeBuild job.

### Application deployment with kubectl
...