from sensor import Glasses
import time

if __name__ == '__main__':

    glasses = Glasses(None)
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        glasses.shutdown()