# few variants of encoders, uncomment one of this
cmdtempl=['HandBrakeCLI', '-e', 'x264',  '-q', '20.0', '-a', '1,2,3,4',
          '-E', 'faac', '-B', '160', '-R', 'Auto', '-D', '0.0',
          '--audio-copy-mask', 'aac,ac3,dtshd,dts,mp3', '--audio-fallback', 'ffac3',
          '-f', 'mp4', '--loose-anamorphic', '--modulus', '2', '-m',
          '--x264-preset', 'veryfast', '--h264-profile', 'main',
          '--h264-level', '4.0', '-i', 'SRC', '-o', 'DST']
cmdtempl=['HandBrakeCLI', '-Z', 'Normal', '-i', '"SRC"', '-o', '"DST"']
# cmdtempl=['ffmpeg', '-i', '"SRC"', '-y', '-vcodec', 'libx264', '-b',
#           '2500k', '-preset', 'veryfast', '-acodec', 'libfdk_aac',
#           '-ab', '128k', '-ac', '2', '-ar', '48k',
#           '-map', '0:v', '-map', '0:a', '-f', 'mp4', '"DST"']
# command for file checking
cmdffp=['ffprobe', '-show_streams', '-of', 'json', '"SRC"']
# input directory
indir="/media/films/"
# list of files in input directory
srclist="/home/user/mkvfiles.txt"
logfile="/home/user/tr.log"
# extensions of source files
inext="mkv"
# regexp for renaming
regexpsearch = '(.*)\.%s' % inext
# regexpsearch = '(.*)\.(mkv|avi|mov|ts|mpg)'
