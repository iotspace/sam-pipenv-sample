# 1. Setup process

```
# install the packages
pipenv install --dev

# enter the env 
pipenv shell
```

In VSCode choose : `Python 3.7.7 64-bit ('sam-pipenv-sample':pipenv)` 


# 2. Run development

Collect python codes to ./package directoy:
```
make prepare-package
```

Make `template.yaml`:
```
cp template.yaml.sample template.yaml
```

Invoke local function
```
sam local invoke ProverbFunction --event event.json
```

Mix make package and invoke function
```
make prepare-package && sam local invoke ProverbFunction --event event.json
```

Make clean package
```
make clean-package
```

# 3. Deploy to AWS

Create S3 bucket to store package artifact
```
# Create S3 bucket
aws s3 mb s3://vsii-aws-artifacts
```

Package Lambda function defined locally and upload to S3 as an artifact
```
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket vsii-aws-artifacts
```

Deploy SAM template as a CloudFormation stack
```
sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-pipenv-sample \
    --capabilities CAPABILITY_IAM
```

Describe Output section of CloudFormation stack previously created
```
aws cloudformation describe-stacks \
    --stack-name sam-pipenv-sample \
    --query 'Stacks[].Outputs[?OutputKey==`HelloWorldApi`]' \
    --output table
```