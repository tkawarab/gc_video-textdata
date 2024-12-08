from flask import Flask, render_template, request, Markup, send_from_directory, send_file, jsonify, Response
from flask_bootstrap import Bootstrap
from tklib import gc_upload, video_parse, data_shaping, create_sbv_file, middleware
import os
import json
import shutil
app = Flask(__name__)
bootstrap = Bootstrap(app)

bucket_name = os.getenv("BUCKET_NAME")

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route("/", methods=["POST"])
@middleware.jwt_authenticated
def main_auth():
    print("processing login")
    return "ログイン成功"

@app.route('/upload_file', methods=['POST'])
@middleware.jwt_authenticated
def upload_file(**kwargs):
    print("processing generate_signed_url," + kwargs['uid'])
    file_name = request.form['file_name']
    print(file_name)
    url = gc_upload.sign_url(bucket_name,file_name)
    print(url)
    return jsonify(url)

@app.route('/video_text_detection', methods=['POST'])
@middleware.jwt_authenticated
def video_text_detection(**kwargs):
    # cleanup temp folder
    shutil.rmtree('./temp')
    os.mkdir('./temp')
    print("processing video_text_detection," + kwargs['uid'])
    #print(kwargs['email'])
    data = request.data.decode('utf-8')
    data = json.loads(data)    
    
    sbv_files = []
    for file_name in data:
        g_uri = "gs://" + bucket_name + "/" + file_name
        annotation_result = video_parse.load_video_textdetection_uri(g_uri)
        array_tbl = video_parse.get_textdetection(annotation_result)
        sbv_data = data_shaping.tbl_2_sbv_format_2(bucket_name,array_tbl,file_name)
        sbv_file_name = create_sbv_file.create_sbv_file(g_uri,sbv_data)
        sbv_files.append(sbv_file_name)        
    downloadFile = create_sbv_file.compress_file(sbv_files) 
    str_shift = downloadFile.rfind("/")
    downloadFileName = downloadFile[str_shift+1:]
    # Clean up
    for file_name in data:
        gc_upload.delete_file(bucket_name,os.path.join(file_name))
        os.remove(os.path.join("./temp/",file_name[:-4] + ".sbv"))
    return send_file(downloadFile, as_attachment = True, \
        download_name = downloadFileName, \
        mimetype = "application/zip")    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
