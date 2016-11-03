import os
import time
from base import BaseProfiler
from ..common.logConfig import get_logger
logger = get_logger(__name__)


class HarProfiler(BaseProfiler):

    def start_recording(self):
        pass

    def stop_recording(self, **kwargs):
        har_dir_path = os.path.join(kwargs['profile_path'], "har", "logs")
        for i in range(10):
            if os.path.exists(har_dir_path):
                har_file_list = os.listdir(har_dir_path)
                if len(har_file_list) == 1:
                    har_file_path = os.path.join(har_dir_path, har_file_list[0])
                    os.rename(har_file_path, self.env.profile_har_file_fp)
                    break
                elif len(har_file_list) == 0:
                    logger.error("can't find any har file in log folder %s" % har_dir_path)
                else:
                    logger.error("find more than one har file in log folder %s" % har_dir_path)
            else:
                logger.error("har log folder is not exist %s " % har_dir_path)

            time.sleep(1)
