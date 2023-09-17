import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from Configuration import Configuration


class LifeIngest(FileSystemEventHandler):
    configuration = Configuration()
    source = configuration.get_source()
    target = configuration.get_target()

    def __init__(self):
        self.observer = Observer()

    def on_created(self, event):
        # Handle the file creation event here
        if event.is_directory:
            return
        self.ingest(event.src_path)
        print(f"File created: {event.src_path}")

    def ingest(self, source_file):
        target_directory = self.target
        try:
            shutil.copy2(source_file, target_directory)
        except OSError as err:
            print(err)

    def start_observing(self):
        observer = Observer()
        observer.schedule(self, path=self.source, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def start(self):
        self.start_observing()


if __name__ == "__main__":
    life_ingestion = LifeIngest()
    LifeIngest.start(life_ingestion)
