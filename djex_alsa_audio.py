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
        self.input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        self.input.setchannels(1)
        self.input.setrate(44000)
        self.input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.input.setperiodsize(160)

    def main(self):
        if self.input and hasattr(self.input, 'read'):
            l, data = self.input.read()
            if l:
                self.rms = audioop.rms(data, self.config["rmswinsize"])
        time.sleep(.001)