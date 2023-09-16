import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from Configuration import Configuration


class LifeIngest(FileSystemEventHandler):

    def __init__(self, source_dir, target_directory):
        self.source_directory = source_dir
        self.target_directory = target_directory
        self.observer = Observer()

    def on_created(self, event):
        # Handle the file creation event here
        if event.is_directory:
            return
        self.ingest(event.src_path)
        print(f"File created: {event.src_path}")

    def ingest(self, source_file):
        target_directory = self.target_directory
        shutil.copy2(source_file, target_directory)


def main(event_handler):
    observer = Observer()
    observer.schedule(event_handler, path=event_handler.source_directory, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    configuration = Configuration()
    source = configuration.get_source()
    target = configuration.get_target()

    print(source)
    print(target)


    # It doesn't work with cloud (Google Drive) targets. What about NFS?
    # cloud_target = "C:\\Users\\octav\\OneDrive\\Desktop\\target"
    # gcloud_target = "G:\\My Drive\\test"
    # local_target = "C:\\Users\\octav\\Documents\\targetNotCloud"
    #
    # # Define the directory to monitor
    # source_directory = "C:\\Users\\octav\\Documents\\TestMonitor"
    # cloud_source = "C:\\Users\\octav\\OneDrive\\Desktop\\source"

    ingestion_handler = LifeIngest(source, target)
    main(ingestion_handler)
