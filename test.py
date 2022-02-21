import os

import boto3
from boto3.dynamodb.conditions import Attr
from moto import mock_dynamodb2


def main():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    with mock_dynamodb2():
        client = boto3.client("dynamodb")
        resource_client = boto3.resource("dynamodb")

        test_table = resource_client.Table("test")

        try:
            result = test_table.update_item(
                Key={"Index": "something"},
                UpdateExpression="SET owner = :owner",
                ExpressionAttributeValues={":owner": "some_owner"},
                ConditionExpression=Attr("owner").eq("UNOWNED") | Attr("owner").not_exists(),
                ReturnValues="ALL_NEW",
                ReturnConsumedCapacity="TOTAL",
            )

            print(f"{result=}")

        # NOTE I expected this exception
        except client.exceptions.ResourceNotFoundException as error:
            print(f"{error=}")

        # NOTE but instead got this exception
        except ValueError as error:
            print(f"{error=}")


if __name__ == "__main__":
    main()
