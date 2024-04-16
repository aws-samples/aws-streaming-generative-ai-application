import boto3
import json
import time
import gzip
from botocore.exceptions import ClientError

DATA_DIR = '../data/Movies_and_TV_5.json.gz'
AWS_REGION = 'us-east-1'
STREAM_NAME = 'generative-ai-stream'
BATCH_SIZE = 10


def get_kinesis_client(region: str):
    """
    Get a Kinesis client.

    Args:
        region (str): AWS region

    Returns: 
        kinesis_client (boto3.client): Kinesis client
    """

    kinesis_client = boto3.client('kinesis', region_name=region)
    return kinesis_client


def get_reviews(data_dir: str) -> list:
    """
    Get paths to review files.

    Args:
        data_dir (str): Directory path containing review files

    Returns:
        reviews_paths (list): List of review file paths
    """
    
    reviews_paths = []

    try: 
        reviews_paths = gzip.open(data_dir, 'r')
    except FileNotFoundError:
            print('Error: File not found.')

    return reviews_paths


def main():
    """Main function of the program. """

    client = get_kinesis_client(AWS_REGION)
    reviews_paths = get_reviews(DATA_DIR)
    index = 0
    review_batch = []

    for review_path in reviews_paths:

        review_json = json.loads(review_path)

        index += 1

        # Retrieve review data
        review = {
            'user_id': review_json.get('reviewerID'),
            'review_id': index,
            'date_time': round(time.time()*1000),
            'text': review_json.get('reviewText')
        }

        review_batch.append(
            {
            'Data': json.dumps(review),
            'PartitionKey': str(index)
            }
        )
    
        if index % BATCH_SIZE == 0:

            try:

                client.put_records(
                    Records=review_batch,
                    StreamName=STREAM_NAME
                )

            except ClientError as e:
                print(f'Error: {e.response}')

            review_batch = []
            
            print(f'Sent {BATCH_SIZE} review(s)!')
            time.sleep(5)

        
if __name__ == '__main__':
    main()

