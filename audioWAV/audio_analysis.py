__author__ = 'eleanor.cui'
# import pymedia
import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia

def open_ogg(filePath):
    data=open(filePath,'r')
    s=data.read(10000)

def get_audio_analysis(audio):
    dm=muxer.Demuxer('ogg')
    frames=dm.parse(audio)
    print len(frames)
    #return dm
    #get_audio_decoder
    dec=acodec.Decoder(dm.streams[0])

if __name__ == '__main__':
    data=open_ogg('test/audio/20150807173157-room-0-user-1.ogg')
    get_audio_analysis(data)