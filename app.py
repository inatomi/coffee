import boto3
import json
import decimal
from chalice import Chalice
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from chalice import NotFoundError

app = Chalice(app_name='coffee')
app.debug = True

coffee = boto3.resource('dynamodb').Table('coffee')

#Decimal Decoder
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
            return super(DecimalEncoder, self).default(o)


@app.route('/coffee/{key}', methods=['GET', 'PUT'])
def order(key):
    request = app.current_request
    if request.method == 'PUT':
        coffee.put_item(
            Item={
                json.dumps(request.json_body)
            }
        )
    elif request.method == 'GET':
        response = coffee.query(KeyConditionExpression=Key('user_id').eq(key))
        return json.dumps(response['Items'],cls=DecimalEncoder)
