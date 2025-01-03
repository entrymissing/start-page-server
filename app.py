from flask import Flask, render_template, request, abort

from googleapiclient.discovery import build
from google.oauth2 import service_account

from apscheduler.schedulers.background import BackgroundScheduler

import random

app = Flask(__name__)


def refresh_file_from_drive(encoding='utf-8'):
  # Set up credentials
  SERVICE_ACCOUNT_FILE = 'credentials.json'
  SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
  credentials = service_account.Credentials.from_service_account_file(
      SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  FILE_ID = '1-mkNdY_PYf-FxQlV1Be0dvCvjHEdkBmn'

  # Build the Drive service
  service = build('drive', 'v3', credentials=credentials)

  request = service.files().get_media(fileId=FILE_ID)
  content_bytes = request.execute()

  try:
    content_str = content_bytes.decode(encoding)
  except UnicodeDecodeError:
    print(f"Error: Could not decode content using encoding {encoding}")
    return

  with open('content.md', 'w+') as f:
    f.writelines(content_str)


def parse_markdown(filepath):
  with open(filepath, 'r') as file:
    lines = [lin.strip() for lin in file.readlines() if lin.strip()]

  content_dict = {}
  current_key = None

  for line in lines:
    if line.startswith('#'):
      current_key = line.lstrip('#').strip().lower()
      content_dict[current_key] = []
    elif line.startswith('-') and current_key:
      content_dict[current_key].append(line.lstrip('-').strip())
  return content_dict


@app.route('/')
def index():
  token = request.args.get('token')
  print()
  if token != 'testtoken':
    abort(403)

  # Get goals and meditations from content.md
  content = parse_markdown('content.md')
  goals = content['goals']
  num_pairs = len(content['meditations']) // 2
  pair_index = random.randint(0, num_pairs - 1)
  meditation = {}
  meditation['title'] = content['meditations'][2 * pair_index]
  meditation['body'] = content['meditations'][2 * pair_index + 1]

  # Render the index.html template
  return render_template('index.html',
                         goals=goals,
                         meditation=meditation)


if __name__ == "__main__":
  scheduler = BackgroundScheduler(daemon=True)
  scheduler.add_job(refresh_file_from_drive, 'interval', minutes=1)
  scheduler.start()
  app.run(host="0.0.0.0", port=8087, debug=True)
