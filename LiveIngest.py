import datetime
import os
import stat
import time
import shutil
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

from Configuration import Configuration
from Filter import Filter


class LiveIngest(FileSystemEventHandler):
    configuration = Configuration()
    source = configuration.get_source()
    target = configuration.get_target()
    owner = configuration.get_owner()
    group = configuration.get_group()
    separator = configuration.get_separator()
    not_required = configuration.get_not_required()

    def __init__(self):
        self.observer = PollingObserver()

    def on_created(self, event):
        # Handle the file creation event here
        if event.is_directory:
            return
        self.ingest(event.src_path)
        print(f"File created: {event.src_path}")

    def ingest(self, source_file):
        target_directory = self.target
        file_name = source_file.split(self.separator)[len(source_file.split(self.separator)) - 1]
        target_file = target_directory + self.separator + file_name
        rejected_filter = Filter(self.not_required)
        print(target_file)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        if rejected_filter.reject(file_name):
            print("Not required: " + file_name + " .Date: " + now)
        else:
            try:
                shutil.copy2(source_file, target_directory)
                #shutil.copystat(source_file, target_directory)
                shutil.chown(target_file, self.owner, self.group)
                os.chmod(target_file,
                         stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
            except OSError as err:
                print(err)

    def start_observing(self):
        self.observer = PollingObserver()
        self.observer.schedule(self, path=self.source, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def start(self):
        self.start_observing()


if __name__ == "__main__":
    live_ingestion = LiveIngest()
    LiveIngest.start(live_ingestion)
