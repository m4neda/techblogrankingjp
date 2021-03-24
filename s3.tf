resource "aws_s3_bucket" "techblogrank-com" {
    bucket = "techblogrank.com"
    acl    = "private"
    policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::techblogrank.com/*"
    },
    {
      "Sid": "2",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E1IK4JYQO4KK4J"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::techblogrank.com/*"
    }
  ]
}
POLICY
}

resource "aws_s3_bucket" "techblogrank-com-logs" {
    bucket = "techblogrank.com-logs"
    acl    = "private"
}

resource "aws_s3_bucket" "techblogrank-com-redirect" {
    bucket = "techblogrank.com-redirect"
    acl    = "private"
}

resource "aws_s3_bucket" "techblogrank-com-root" {
    bucket = "techblogrank.com-root"
    acl    = "private"
    policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "PolicyForWebsiteEndpointsPublicContent",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::techblogrank.com-root/*",
        "arn:aws:s3:::techblogrank.com-root"
      ]
    }
  ]
}
POLICY
}

