#!/usr/bin/env python3

import argparse
import atexit
import sys
import logging
import time
import threading
import signal
import pprint

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
    parser.add_argument("--log", default="WARN", help="specify log level")
    parser.add_argument("--config", type=bool, default=False, help="only update config db, do not start service")
    parser.add_argument("--threshold", type=int, help="db threshold")
    parser.add_argument("--rmswinsize", type=int, help="size for rms sampling window")
    args = parser.parse_args()

    #
    #
    # Set log level

    numeric_level = getattr(logging, args.log.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)

    pp = pprint.PrettyPrinter(indent=4)

    logging.basicConfig(level=numeric_level)

    #
    #
    # Initialize config

    logging.info('Initializing config')

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

    logging.debug('Dumping current config')
    logging.debug(pp.pformat(config.data))

    # Exit if --config switch set

    if args.config:
        sys.exit(0)

    #
    #
    # Setup ALSA audio

    logging.info('Initializing ALSA audio')

    audio = djex_alsa_audio.DjexAlsaAudio()
    #audio = djex_dummy_audio.DjexDummyAudio()
    audio.configure(config.data)
    audio.initaudio()

    #
    #
    # Setup GPIO

    logging.info('Initializing GPIO')

    gpio = djex_pi_gpio.DjexPiGpio()
    #gpio = djex_dummy_gpio.DjexDummyGpio()
    gpio.setup(config.data)
    atexit.register(gpio.cleanup)

    #
    #
    # Threads

    def update_audio():
        while True:
            audio.main()

    audio_thread = threading.Thread(target=update_audio)
    audio_thread.daemon = True
    audio_thread.start()

    def update_config():
        while True:
            if config.update():
                logging.info('Config was updated')
                logging.debug('Dumping current config')
                logging.debug(pp.pformat(config.data))
                audio.configure(config.data)
            time.sleep(1)

    config_thread = threading.Thread(target=update_config)
    config_thread.daemon = True
    config_thread.start()

    #
    #
    # Signal handler

    def signal_handler(signal, frame):
        logging.debug('Caught signal')
        logging.debug(pp.pformat(signal))
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    #
    #
    # Main loop

    while True:
        if audio.rms >= config.data["threshold"]:
            gpio.send_warning()
        time.sleep(.1)
