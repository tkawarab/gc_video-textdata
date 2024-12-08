import io
import zipfile
import datetime



def create_sbv_file(gsutil_path,sbv_data):
    str_shift = gsutil_path.rfind("/")
    file_name = gsutil_path[str_shift+1:-4]
    output_path = "./temp/" + file_name + ".sbv"
    ot_file = open(output_path,"w",encoding="utf-8")
    ot_file.write(sbv_data)
    ot_file.close()
    return file_name

def compress_file(filename_list):
    compress_file_path = './temp/sbvfiles_' + yyyymmddhhmmss() + '.zip'
    with zipfile.ZipFile(compress_file_path, 'w',compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for filename in filename_list:
            file_path = './temp/' + filename + ".sbv"
            zf.write(file_path,arcname=filename + ".sbv")
    return compress_file_path
    
def yyyymmddhhmmss():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    return now.strftime('%Y%m%d%H%M%S')

    