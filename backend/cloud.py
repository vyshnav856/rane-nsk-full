import boto3

access_key = ""
secret_access_key = ""
bucket_name = ""

def save_to_cloud():
	s3 = boto3.resource(
		service_name="s3",
		region_name="ap-south-1",
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_access_key
	)

	s3 = boto3.client("s3",
					aws_access_key_id=access_key,
					aws_secret_access_key=secret_access_key)

	image = "final_image.png"
	output = "output.txt"

	response = s3.upload_file(image, bucket_name, image)
	response2 = s3.upload_file(output, bucket_name, output)

save_to_cloud()