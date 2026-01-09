import boto3

def lambda_handler(event, context):
    intent_name = event['request']['intent']['name']
    
    # 固定のインスタンスIDとリージョン
    instance_id = '＜インスタンスID＞'
    region = 'ap-northeast-1'
    ec2 = boto3.client('ec2', region_name=region)

    if intent_name == 'StartServerInstanceIntent':
        # EC2インスタンスを起動
        try:
            response = ec2.start_instances(InstanceIds=[instance_id])
            message = "サーバーを起動しました。"
        except Exception as e:
            message = f"サーバーの起動に失敗しました: {str(e)}"

    elif intent_name == 'StopServerInstanceIntent':
        # EC2インスタンスを停止
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id])
            message = "サーバーを停止しました。"
        except Exception as e:
            message = f"サーバーの停止に失敗しました: {str(e)}"

    elif intent_name == 'QueryInstanceStatusIntent':
        # EC2インスタンスの状態を確認
        try:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            state = response['Reservations'][0]['Instances'][0]['State']['Name']
            status_map = {
                'running': '起動中',
                'stopped': '停止中',
                'pending': '起動処理中',
                'stopping': '停止処理中',
                'terminated': '削除済み'
            }
            message = f"サーバーは{status_map.get(state, state)}です。"
        except Exception as e:
            message = f"ステータスの取得に失敗しました: {str(e)}"

    else:
        message = '申し訳ありません、その操作には対応していません。'

    # Alexaへの応答を返す
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': message
            },
            'shouldEndSession': True
        }
    }
