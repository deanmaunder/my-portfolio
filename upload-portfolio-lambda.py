import boto3
import StringIO
import zipfile

s3 = boto3.resource('s3')

portfolio_bucket = s3.Bucket('portfolio.maunder.link')
build_bucket = s3.Bucket('portfolio-build.maunder.link')

portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('buildPortfolio.zip',portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm)
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
