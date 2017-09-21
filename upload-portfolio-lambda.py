import boto3
import StringIO
import zipfile



def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    
    topic = sns.Topic('arn:aws:sns:ap-southeast-2:198641624864:deployPortfolioTopic')
    try:
        portfolio_bucket = s3.Bucket('portfolio.maunder.link')
        build_bucket = s3.Bucket('portfolio-build.maunder.link')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('buildPortfolio.zip',portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm)
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    
        print "Job done!"
    
    
        topic.publish(Subject="Portfolio Deployed", Message="Its done!")
    except:
        topic.publish(Subject="Portfolio FAILED", Message="Its NOT done!")
        raise
