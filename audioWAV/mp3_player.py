__author__ = 'eleanor.cui'
#1.???????? 10000 ????????????????
f = open( u'test/audio/20150807173157-room-0-user-1.ogg', 'rb' )
data= f.read(10000)

#2.????????????????????
import pymedia.muxer as muxer
dm = muxer.Demuxer('ogg')
frames = dm.parse(data)
print len(frames)

#3.??????? Mp3 ????????????
import pymedia.audio.acodec as acodec
dec = acodec.Decoder( dm.streams[ 0 ] )
#???????
#params = {'id': acodec.getCodecID('mp3'), 'bitrate': 128000, 'sample_rate': 44100, 'ext': 'mp3', 'channels': 2}
#dec= acodec.Decoder(params)


#4.?????????
frame = frames[0]
#????? frame ?????????
r= dec.decode( frame[ 1 ] )
print "sample_rate:%s , channels:%s " % (r.sample_rate,r.channels)
#???????????? r=dec.decode( data)?????????????
#??????????????????????????????????????

#5.????????
import pymedia.audio.sound as sound
snd = sound.Output( r.sample_rate, r.channels, sound.AFMT_S16_LE )

#6.??
if r: snd.play( r.data )

#7.??????????
while True:
    data = f.read(512)
    if len(data)>0:
        r = dec.decode( data )
        if r: snd.play( r.data )
    else:
        break

#8.?????????
import time
while snd.isPlaying(): time.sleep( .5 )