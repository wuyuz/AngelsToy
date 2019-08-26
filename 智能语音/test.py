import subprocess,os

def get_file_content(filePath):
    # cmd = f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm"
    # cmd = 'dir'
    r = subprocess.Popen('ffmpeg',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    stdout = r.stdout.read().decode('gbk')
    print(stdout)
    stderr =  r.stderr.read().decode('gbk')
    print(stderr)


    # with open(f'{filePath}.pcm','rb') as fp:
    #     return fp.read()




#0xc7

get_file_content('wyn')