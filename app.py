from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class Ec2InstanceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear el rol usando LabRole
        role = iam.Role.from_role_arn(self, "LabRole", "arn:aws:iam::118248464783:role/LabRole")

        # Crear la VPC (Virtual Private Cloud)
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Crear la instancia EC2
        instance = ec2.Instance(self, "Instance",
                                instance_type=ec2.InstanceType("t2.micro"),
                                machine_image=ec2.MachineImage.latest_amazon_linux(),
                                vpc=vpc,
                                role=role)

        # Configurar los archivos websimple y webplantilla en la instancia EC2
        user_data_script = """
        #!/bin/bash
        sudo yum update -y
        sudo yum install -y httpd git
        sudo systemctl start httpd
        sudo systemctl enable httpd

        # Clonar el repositorio websimple
        cd /var/www/html
        sudo git clone https://github.com/KarTaGo124/websimple.git
        sudo mv websimple/* /var/www/html/
        sudo rm -rf websimple

        # Clonar el repositorio webplantilla
        sudo git clone https://github.com/KarTaGo124/webplantilla.git
        sudo mv webplantilla/* /var/www/html/
        sudo rm -rf webplantilla

        # Dar permisos a los archivos y reiniciar httpd
        sudo chmod -R 755 /var/www/html
        sudo systemctl restart httpd
        """
        instance.add_user_data(user_data_script)

