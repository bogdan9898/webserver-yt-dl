from flask import Flask, request, url_for, session
from flask_sieve import validate, Sieve
import Validators
import youtube_dl
import json
import os

import config
from Logger import YDL_Logger


app = Flask(__name__)
app.secret_key = config.app_key
Sieve(app)


@app.route('/')
def ping():
    return app.response_class(
        response=json.dumps({
            'status': 200,
            'server_status': 'online'
        }),
        status=200,
        mimetype='application/json'
    )


@app.route('/shareable-link', methods=['POST'])
@app.route('/shareable-link/<vid>', methods=['GET'])
# todo: write your own validator that works only for specified methods
# @validate(Validators.ShareableLink)
def get_shareable_link(vid=None):
    if request.method == "GET":
        # deliver requested file
        if not os.path.exists(config.save_dir + vid):
            return app.response_class(
                response=json.dumps({
                    'status': 404,
                    'error': 'VID not found'
                }),
                status=200,
                mimetype='application/json'
            )
        data = None
        with open(config.save_dir + vid, 'rb') as file:
            data = file.read()
        return app.response_class(
            response=data,
            status=200,
            mimetype='application/octet-stream'
        )

    elif request.method == "POST":
        # generate shareable link
        body = request.json
        print("body:")
        print(body)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            # 'outtmpl': '/tmp/%(title)s.%(ext)s'
            'outtmpl': '/tmp/%(id)s.%(ext)s',
            'logger': YDL_Logger(),
            # 'progress_hooks': [finished],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([body['url']])
            except Exception as e:
                print(e)

        return app.response_class(
            response=json.dumps({
                'status': 200,
                'uri': url_for('get_shareable_link') + "/" + session['vid']
            }),
            status=200,
            mimetype='application/json'
        )


# def finished(d):
#     print("!"*100)
#     print(d)
#     print("!"*100)



if __name__ == '__main__':
    # host = "127.0.0.1"
    host = "192.168.100.2"
    app.run(host=host, port=8080, debug=True)



