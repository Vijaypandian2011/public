import urllib.parse
from datetime import datetime

# Function to parse and extract information from the URL
def parse_s3_url(url):
    try:
        # Step 1: Parse the URL
        parsed_url = urllib.parse.urlparse(url)

        # Step 2: Extract bucket name and file path
        bucket_name = parsed_url.netloc.split('.')[0]  # Extract the bucket name from the netloc
        file_path = parsed_url.path.lstrip('/')  # Remove leading slash for the path

        # Step 3: Extract the query parameters
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Extract specific parameters
        aws_access_key_id = query_params.get('AWSAccessKeyId', ['N/A'])[0]
        signature = query_params.get('Signature', ['N/A'])[0]
        security_token = query_params.get('x-amz-security-token', ['N/A'])[0]
        expires_timestamp = query_params.get('Expires', ['N/A'])[0]

        # Convert the expiry time from string to a datetime object
        if expires_timestamp != 'N/A':
            expires_datetime = datetime.utcfromtimestamp(int(expires_timestamp))
        else:
            expires_datetime = None

        # Return the extracted details as a dictionary
        return {
            "Bucket Name": bucket_name,
            "File Path": file_path,
            "AWS Access Key ID": aws_access_key_id,
            "Signature": signature,
            "Security Token": security_token,
            "Expires Timestamp": expires_timestamp,
            "Expires Time (UTC)": expires_datetime.strftime('%Y-%m-%d %H:%M:%S') if expires_datetime else "N/A"
        }

    except Exception as e:
        print(f"Error while processing the URL: {e}")
        return None

# Function to print out the extracted information neatly
def print_extracted_info(info):
    if info:
        print("\nParsed URL Information:")
        for key, value in info.items():
            print(f"{key}: {value}")
    else:
        print("Failed to extract information.")

# Main function to handle user input and execution
def main():
    # Step 1: Ask the user for the URL
    url = input("Please enter the S3 URL: ")

    # Step 2: Parse the URL and extract information
    extracted_info = parse_s3_url(url)

    # Step 3: Print out the extracted information
    print_extracted_info(extracted_info)

if __name__ == "__main__":
    main()
