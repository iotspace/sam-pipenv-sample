# 1. Setup process

```bash
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
```bash
cp template.yaml.sample template.yaml
```

Invoke local function
```bash
sam local invoke ProverbFunction --event event.json
```

Mix make package and invoke function
```bash
make prepare-package && sam local invoke ProverbFunction --event event.json
```

Make clean package
```bash
make clean-package
```

# 3. Deploy to AWS

Create S3 bucket to store package artifact
```bash
# Create S3 bucket
aws s3 mb s3://vsii-aws-artifacts
```

Package Lambda function defined locally and upload to S3 as an artifact
```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket vsii-aws-artifacts
```

Deploy SAM template as a CloudFormation stack
```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-pipenv-sample \
    --capabilities CAPABILITY_IAM
```

Describe Output section of CloudFormation stack previously created
```bash
aws cloudformation describe-stacks \
    --stack-name sam-pipenv-sample \
    --query 'Stacks[].Outputs[?OutputKey==`ProverbFunction`]' \
    --output table
```

Tail Lambda function Logs using Logical name defined in SAM Template
```bash
sam logs -n ProverbFunction --stack-name sam-pipenv-sample --tail
```

# 4. Cleanup

In order to delete our Serverless Application recently deployed you can use the following AWS CLI Command:

```bash
aws cloudformation delete-stack --stack-name sam-pipenv-sample
make clean-package
```

# 5. Testing

Next, we install test dependencies and we run `pytest` against our `tests` folder to run our initial unit tests:

```bash
pipenv install --dev
pipenv shell
python -m pytest tests/ -v
```