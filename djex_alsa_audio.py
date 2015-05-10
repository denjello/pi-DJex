import alsaaudio
import audioop
import time

class DjexAlsaAudio():

    input = False
    config = {}
    rms = 0

    def configure(self, config):
        self.config = config

    def initaudio(self):
        input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        input.setchannels(2)
        input.setrate(44000)
        input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        input.setperiodsize(160)

    def main(self):
        l, data = input.read()
        if l:
            self.rms = audioop.rms(data, 2)
        time.sleep(.001)