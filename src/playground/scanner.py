import os
import fnmatch
from threading import Thread, Event
from Queue import Queue, Empty
import kaa.metadata
import time

from file import ScanFile

# Constants
SCAN_BASE = "/home/jevans/test-music-library/music"
AUDIO_EXT = ['flac', 'mp3', 'm4a']
VIDEO_EXT = ['avi', 'mp4', 'mpg', 'mkv']

# Globals
file_queue = Queue()
shutdown_event = Event()
scanner_done_event = Event()


# Scanner: finds files to add to file_queue
class Scanner(Thread):

    def __init__(self, path):
        self.path = path
        self.num_scanned = 0
        Thread.__init__(self)

    def run(self):
        targets = []

        for root, dirs, files in os.walk(self.path):
            for ext in AUDIO_EXT:
                pattern = "*.%s" % ext
                for fname in fnmatch.filter(files, pattern):
                    targets.append(ScanFile(os.path.join(root, fname), 0, 'audio'))

        for target in targets:
            file_queue.put(target)

        self.num_scanned = len(targets)
        print "Scanner: added %d targets" % len(targets)

        scanner_done_event.set()


# Tagger:  pulls files off the queue and gets metadata
class Tagger(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.num_tagged = 0

    def run(self):
        while not shutdown_event.isSet():
            try:
                f = file_queue.get(block=True, timeout=0.1)
            except Empty:
                if scanner_done_event.isSet():
                    return
                else:
                    continue

            info = kaa.metadata.parse(f.name)
            self.num_tagged += 1
            #print "%s - %s" % (info.artist, info.title)


class Monitor(Thread):

    def __init__(self, scanner):
        Thread.__init__(self)
        self.ts = []
        self.scanner = scanner

    def add_tagger(self, t):
        self.ts.append(t)

    def run(self):
        last_ns = 0
        last_nt = 0
        last_time = time.time()
        dt = 0.0
        ns = 0
        nt = 0
        while not shutdown_event.isSet():
            dt = time.time() - last_time
            ns = self.scanner.num_scanned
            nt = 0
            for t in self.ts:
                nt += t.num_tagged
            print "%f scanned per second" % ((ns - last_ns) / dt)
            print "%f tagged per second" % ((nt - last_nt) / dt)
            last_ns = ns
            last_nt = nt

            last_time = time.time()
            time.sleep(1)

if __name__ == "__main__":
    print "Scanning %s:" % SCAN_BASE

    scanner = Scanner(SCAN_BASE)
    mon = Monitor(scanner)

    ts = []
    for i in range(5):
        ts.append(Tagger())

    start = time.time()
    scanner.start()

    for i in ts:
        mon.add_tagger(i)
        i.start()

    mon.start()

    for i in ts:
        i.join()
    end = time.time()
    shutdown_event.set()

    print "Runtime: %f s" % (end - start)
    print "Exiting"
