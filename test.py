import boto3
from moto import mock_dynamodb2
from boto3.dynamodb.conditions import Attr


def main():
    with mock_dynamodb2():
        client = boto3.resource("dynamodb")

        test_table = client.Table("test")

        result = test_table.update_item(
            Key={"Index": "something"},
            UpdateExpression="SET owner = :owner",
            ExpressionAttributeValues={":owner": "some_owner"},
            ConditionExpression=Attr("owner").eq("UNOWNED") | Attr("owner").not_exists(),
            ReturnValues="ALL_NEW",
            ReturnConsumedCapacity="TOTAL",
        )

        print(f"{result=}")


if __name__ == "__main__":
    main()