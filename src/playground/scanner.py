import os
import fnmatch
from threading import Thread, Event
from Queue import Queue, Empty
import kaa.metadata
import time
import pyhash
import signal

from file import ScanFile

# Constants
SCAN_BASE = "/home/jevans/test-music-library/music"
AUDIO_EXT = ['flac', 'mp3', 'm4a']
VIDEO_EXT = ['avi', 'mp4', 'mpg', 'mkv']

# Globals
file_queue = Queue()
shutdown_event = Event()
scanner_done_event = Event()
tagger_done_event = Event()


# Handle interrupt
def sigint_handler(sig, stack):
    print "Caught signal"
    shutdown_event.set()


# Scanner: finds files to add to file_queue
class Scanner(Thread):

    def __init__(self, path):
        self.path = path
        self.num_scanned = 0
        Thread.__init__(self)
        self.hasher = pyhash.murmur3_32()
        #self.hasher = pyhash.super_fast_hash()

    def run(self):
        targets = []
        start = time.time()
        for root, dirs, files in os.walk(self.path):
            for ext in AUDIO_EXT:
                pattern = "*.%s" % ext
                for fname in fnmatch.filter(files, pattern):
                    fp = os.path.join(root, fname)
                    hsh = self.hasher(str(os.stat(fp)))
                    targets.append(ScanFile(fp, hsh, 'audio'))
                    self.num_scanned += 1
                    if shutdown_event.isSet():
                        return

        for target in targets:
            file_queue.put(target)

        end = time.time()
        print "Scanner done after %0.5f seconds." % (end - start)
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
                    tagger_done_event.set()
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
        self.scanned = 0
        self.tagged = 0
        self.time = 0.0

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
            time.sleep(1)
            dt = time.time() - last_time
            last_time = time.time()
            ns = self.scanner.num_scanned
            nt = 0
            for t in self.ts:
                nt += t.num_tagged
            if ns > last_ns:
                print "%0.1f scans/sec" % ((ns - last_ns) / dt)
            if nt > last_nt:
                print "%0.1f tags/sec" % ((nt - last_nt) / dt)
            last_ns = ns
            last_nt = nt
            self.tagged = nt
            self.time += dt

    def get_stats(self):
        return "%d scanned and tagged in %0.1f seconds." % (self.tagged, self.time)

if __name__ == "__main__":
    print "Scanning %s:" % SCAN_BASE

    signal.signal(signal.SIGINT, sigint_handler)
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

    while (not shutdown_event.isSet()) or ((not tagger_done_event.isSet()) and (not scanner_done_event.isSet())):
        pass

    for i in ts:
        i.join()
    end = time.time()
    shutdown_event.set()
    mon.join()
    print mon.get_stats()
