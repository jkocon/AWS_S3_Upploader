import os
import boto3
import yaml
import logging
from datetime import datetime
from botocore.exceptions import ClientError

# Initialize logger globally
logger = logging.getLogger()

def setup_logger():
    """
    Sets up the logger to write to a file with the current date and time,
    and also logs to the console.

    Returns:
    logging.Logger: Configured logger instance.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_filename = os.path.join(script_dir, '../logs', datetime.now().strftime("LOG_%d_%m_%Y_%H_%M_%S.log"))
    logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_filename)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def load_config():
    """
    Loads configuration from a YAML file located in the same directory as the script.

    Returns:
    dict: Configuration dictionary.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '../config/config.yaml')

    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Error: Configuration file {config_path} not found.")
        exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing {config_path}: {e}")
        exit(1)

def upload_files_from_folder(aws_access_key_id, aws_secret_access_key, region_name, bucket_name, local_folder, s3_prefix=""):
    """
    Uploads all files from the specified local folder to the given S3 bucket.

    Parameters:
    aws_access_key_id (str): AWS Access Key ID.
    aws_secret_access_key (str): AWS Secret Access Key.
    region_name (str): AWS region.
    bucket_name (str): The name of the S3 bucket.
    local_folder (str): The local folder path.
    s3_prefix (str): (Optional) A prefix to add to the S3 object keys.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    if not os.path.isdir(local_folder):
        logger.error(f"Error: The folder {local_folder} does not exist.")
        return

    for file_name in os.listdir(local_folder):
        local_file_path = os.path.join(local_folder, file_name)
        if os.path.isfile(local_file_path):
            s3_key = f"{s3_prefix}{file_name}" if s3_prefix else file_name
            try:
                logger.info(f"Uploading {local_file_path} to s3://{bucket_name}/{s3_key}")
                s3_client.upload_file(local_file_path, bucket_name, s3_key)
                logger.info("Upload successful.")
            except ClientError as e:
                logger.error(f"Error uploading {local_file_path}: {e}")
            except Exception as ex:
                logger.error(f"Unexpected error uploading {local_file_path}: {ex}")

def list_s3_objects(aws_access_key_id, aws_secret_access_key, region_name, bucket_name, s3_prefix=""):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    try:
        logger.info(f"Listing objects in s3://{bucket_name}/{s3_prefix}")
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                logger.info(f"{obj['Key']} - Last Modified: {obj['LastModified']} - Size: {obj['Size']} bytes")
        else:
            logger.info("No objects found.")
    except ClientError as e:
        logger.error(f"Error listing objects: {e}")

if __name__ == '__main__':
    logger = setup_logger()
    logger.info("Script started.")

    config = load_config()

    aws_access_key_id = config.get('aws_access_key_id')
    aws_secret_access_key = config.get('aws_secret_access_key')
    region_name = config.get('region_name')
    bucket_name = config.get('bucket_name')
    local_folder = config.get('local_folder')
    s3_prefix = config.get('s3_prefix', "")

    if not all([aws_access_key_id, aws_secret_access_key, region_name, bucket_name, local_folder]):
        logger.error("Error: Missing required configuration parameters.")
        exit(1)
    
    upload_files_from_folder(aws_access_key_id, aws_secret_access_key, region_name, bucket_name, local_folder, s3_prefix)

    list_s3_objects(aws_access_key_id, aws_secret_access_key, region_name, bucket_name, s3_prefix)
    
    logger.info("Script finished.")
