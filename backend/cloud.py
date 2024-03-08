import boto3

access_key = ""
secret_access_key = ""

def save_to_cloud():
	s3 = boto3.resource(
		service_name="s3",
		region_name="ap-south-1",
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_access_key
	)

	s3 = boto3.client("s3",
					aws_access_key_id="AKIAWT4JAZLZ2WSVTRDB",
					aws_secret_access_key="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")

	bucket_name = "ranensk-bucket"
	image = "final_image.png"
	output = "output.txt"

	response = s3.upload_file(image, bucket_name, image)
	response2 = s3.upload_file(output, bucket_name, output)

save_to_cloud()