from multiprocessing import Process
import os

class PcapDispacher(Process):
    def __init__(self, context):
        self._context = context
        super().__init__()

    def run(self):
        pcap_queue = self._context.queue['pcap']
        pcap_dir = self._context.pcap_dir
        for pcap in absolute_file_paths(pcap_dir):
            pcap_queue.put(pcap)

        # pcap directory

def absolute_file_paths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
