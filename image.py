from g4f.client import Client

client = Client()
response = client.images.generate(
  model="gemini",
  prompt="""
        generate image that that maches the context of the following, Amazon S3 is a highly scalable object-based cloud storage service provided by Amazon Web Services that can be used to store static and media files for Django projects. To set up an S3 bucket, we need to create it in the AWS management console by providing a bucket name and selecting a region. In addition, we also need to replace the access key ID and secret with the appropriate 
        values for our S3 bucket.

        To test the integration, we can add a new product with an image field in the Django admin interface and upload it to the S3 bucket using the booto3 package. After this, we can verify that the image has been successfully uploaded by checking if it is present in the S3 bucket.

        Once the S3 integration has been tested, we can configure the S3 bucket to store static and media files for our Django project by adding a line of code in the settings.py file. We also need to replace the AWS region name with 
        the correct value obtained from our S3 bucket in the AWS management console. Finally, we can run `python manage.py collectstatic` to move existing media files to the S3 bucket.

        In addition to these main points, it is important to encourage viewers to like, share, and subscribe to the YouTube channel and provide contact information for questions or feedback."""
  
)
image_url = response.data[0].url
print(image_url)