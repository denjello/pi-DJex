import argparse
import atexit
import sys
import logging
import time
import threading

import djex_config
import djex_alsa_audio
#import djex_dummy_audio
import djex_pi_gpio
#import djex_dummy_gpio

if __name__ == "__main__":

    #
    #
    # Get the command line args

    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default='INFO', help="specify log level")
    parser.add_argument("--config", type=bool, default=False, help="only update config db, do not start service")
    parser.add_argument("--threshold", type=int, help="db threshold")
    parser.add_argument("--rmswinsize", type=int, help="size for rms sampling window")
    args = parser.parse_args()

    #
    #
    # Set log level

    numeric_level = getattr(logging, args.log.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('invalid log level: %s' % args.log)

    logging.basicConfig(level=numeric_level)

    #
    #
    # Initialize config

    logging.debug('Initializing config')

    config = djex_config.DjexConfig()
    config.update()

    dump_config = False

    if args.threshold:
        config.set("threshold", args.rmswinsize)
        dump_config = True

    if args.rmswinsize:
        config.set("rmswinsize", args.rmswinsize)
        dump_config = True

    if dump_config:
        config.dump()

    # Exit if --config switch set

    if args.config:
        sys.exit(0)

    #
    #
    # Setup ALSA audio

    logging.debug('Initializing ALSA audio')

    audio = djex_alsa_audio.DjexDummyAudio()
    #audio = djex_dummy_audio.DjexDummyAudio()
    audio.configure(config.data)
    audio.initaudio()

    #
    #
    # Setup GPIO

    logging.debug('Initializing GPIO')

    gpio = djex_pi_gpio.DjexPiGpio()
    #gpio = djex_dummy_gpio.DjexDummyGpio()
    gpio.setup(config.data)
    atexit.register(gpio.cleanup)

    #
    #
    # Main

    def update_audio():
        while True:
            audio.main()

    to = threading.Thread(target=update_audio)
    to.start()

    while True:
        if config.update():
            logging.debug('Updating config')
            audio.configure(config.data)
        if audio.rms >= config.data["threshold"]:
            gpio.send_warning()
        time.sleep(0.1)



