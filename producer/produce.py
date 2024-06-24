import boto3
import json
import time
import os
import glob
import random
import uuid
import gzip
from botocore.exceptions import ClientError


DATA_DIR = '../data/aclImdb/train/'
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


def get_review_paths(data_dir: str) -> str:
    """
    Get paths to review files.

        data_dir (str): Directory path containing review files

    Returns:
        review_paths (list): List of paths to review files
    """

    neg_review_paths = glob.glob(os.path.join(data_dir, 'neg', '*.txt'))
    post_review_paths = glob.glob(os.path.join(data_dir, 'pos', '*.txt'))
    
    # Combine both files and shuffle 
    review_paths = neg_review_paths + post_review_paths
    random.shuffle(review_paths)

    return review_paths


def main():
    """Main function of the program. """

    client = get_kinesis_client(AWS_REGION)
    review_paths = get_review_paths(DATA_DIR)
    index = 0
    review_batch = []

    # Go over all file paths
    for review_path in review_paths: 

        index += 1

        # Retrieve review data
        try: 
            with open(review_path, 'r', encoding='utf-8') as file:
                review_text = file.read()
        except FileNotFoundError:
                print('Error: File not found.')

        review = {
            'user_id': str(uuid.uuid4()),
            'review_id': index,
            'date_time': round(time.time()*1000),
            'text': review_text
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
            time.sleep(10)

        
if __name__ == '__main__':
    main()
