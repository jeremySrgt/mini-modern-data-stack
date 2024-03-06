import pulumi_aws as aws

available_az = aws.get_availability_zones(state="available")
primary_az = available_az.names[0]
secondary_az = available_az.names[1]