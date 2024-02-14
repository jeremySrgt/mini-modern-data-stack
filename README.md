# Mini Modern Data Stack
Deploy a complete data stack that can run in production in just a couple of minutes.

![alt text](images/high_level_design.jpg "Stack HLD")

## Infrastructure
The stack is made to be deployed on AWS and tries to be as simple as possible without compromising security
- instances are in a private subnet with no direct access to internet
- a NAT Gateway is used to enable instances to make request to external services
- SSH port on instance are not open
- connecting to an instance or using port forwarding is made through AWS Session Manager (act kind of like a bastion)
- SSH keypair are still needed in order to execute ansible script on the instances
- There is 2 private subnet, because RDS always needs 2 subnet even if on a single-AZ deployment

![alt text](images/infra_schema.jpg "Infra schema")

## Deploying the stack

There is a couple of step you should follow in order to deploy the stack

Clone the repo and cd into it
```bash
git clone git@github.com:jeremySrgt/mini-modern-data-stack.git
cd mini-modern-data-stack
```

You need 2 things to be able to run this deployment :
- an AWS account with AWS CLI configured (follow [instruction here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) then run `aws configure`)
- aws ssm plugin to securely manage instance (follow [instruction here](https://docs.aws.amazon.com/systems-manager/latest/userguide/install-plugin-macos-overview.html) to install it)
Be careful to be on the right AWS profile (if you have several) when executing command. If you need run all of this on another AWS profile, you set it up for your current terminal session like so :
```bash
export AWS_PROFILE=<profile_name>
```

Create a python virtual env (note that this stack is tested on python 3.11)
```bash
python -m venv data_stack_venv
```

Activate the virtual env
```bash
source data_stack_venv/bin/activate
````

Install requirements
```bash
pip install -r requirements.txt
```

In order to configure the future AWS instances we need to create a keypair. Don't worry there is a .gitignore rules to prevent them from getting pushed into github

```bash
ssh-keygen -f dev-keypair
```

Now you need a pulumi cloud account in order to manage the state of your infrastructure. It's completly free and you can do pretty much everything with the free tier account

Go to https://app.pulumi.com/signup and create your account

Now cd into stack > pulumi and login into pulumi with your credentials

``` bash
pulumi login
```

Now you have to set a couple of required environnement variable and secrets. Here is the list :

| Config name               | Required | Default value | Description                                     |
| --------------------------|:--------:| :------------:| -----------------------------------------------:|
| env                       | false    | dev           | name of the env you are deploying to            |
| public_key_path           | true     |               | path to your public key (ending with .pub)      |
| airbyte_instance_type     | false    | t3.medium     | type of Airbyte instance                        |
| metabase_instance_type    | false    | t3.small      | type of Metabase instance                       |
| warehouse_instance_class  | false    | db.t3.micro   | type of RDS instance class for the warehouse    |
| warehouse_db_name         | false    | company_data_warehouse| name of the default database            |
| dwh_master_user*          | true     |               | master user of the database                     |
| dwh_master_password*      | true     |               | master user's password of the database          |

To set a config variable :
```bash
pulumi config set <config_name> <config_value>
```

config name marked with a * are secrets and needs to be set as one in pulumi :
```bash
pulumi config set --secret <secret_name> <secret_value>
```

Once it's all done you can preview what will be deployed
```bash
pulumi preview
```

Then run the deployment
```bash
pulumi up --yes
```

It takes about 10-15 minutes to deploy all the resources. it's actually deploying an RDS database that takes a bit of time

When it's done the last thing remaining is to configure our instances to deploy Metabase and Airbyte on it. cd into the ansible directory then :

```bash
ansible-playbook --private-key ../dev-keypair -i inventories/dev/aws_ec2.yml playbooks/airbyte_playbook.yml
```
and
```bash
ansible-playbook --private-key ../dev-keypair -i inventories/dev/aws_ec2.yml playbooks/metabase_playbook.yml
```

Note that, by default, ansible will look for instance in eu-west-3 region, if you are deploying on another region set the AWS_REGION env in your terminal session, for example : `export AWS_REGION=eu-central-1`

If everything worked well, you should now have a complete mini data stack running on AWS, that can sync data from sources to your warehouse, run dbt and python transformation and visualize data thanks to Metabase !

## Accessing Airbyte and Metabase
Airbyte and Metabase are quite sensible instance because manage your company's data. That is why they are not exposed to the internet for security reason. To access them you need something similar to an SSH tunnel to forward port.

Since we are using AWS securely connect to our instance with the aws ssm plugin, we will execute a command to run a port forwarding session to access our instances.

```bash
aws ssm start-session --target <airbyte_instance_id> --document-name AWS-StartPortForwardingSession --parameters '{"portNumber":["8000"],"localPortNumber":["8000"]}'
```

Now you should be able to acces airbyte on http://localhost:8000/

do the same for Metabase, but replace the port number to 3000

Don't close the aws ssm session until you are done with your instance

## Monthly cost


## Enhancements
Here is a list of enhancement to be made, either to follow engineering best practices or to make the stack more scalable

* [ ] Configure a CI/CD deployement of the stack 
* [ ] Tag docker image based on commit SHA, for better version tracking
* [ ] Migrate Metabase and Airbyte deployment to ECS for better resiliency and less instance configuration (Airbyte doesn't support ECS out of the box for now, so it's a bit of a challenge)