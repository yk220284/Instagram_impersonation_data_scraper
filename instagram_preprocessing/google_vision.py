from google.oauth2 import service_account

from utils import Authenticator

authenticator = Authenticator('auth.yaml')
json_acct_info = authenticator.read_config('google')
credentials = service_account.Credentials.from_service_account_info(
    json_acct_info)

scoped_credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return texts[0].description


if __name__ == '__main__':
    detect_text("data/img/CKwiuf5MZ5l.png")
