import os
import json
import time
import copy
import numpy as np
from baseGenerator import BaseGenerator
from inputLatencyAnimationDctGenerator import InputLatencyAnimationDctGenerator
from frameThroughputDctGenerator import FrameThroughputDctGenerator
from ..helper.terminalHelper import find_terminal_view
from ..common.visualmetricsWrapper import find_tab_view
from ..common.visualmetricsWrapper import find_image_viewport
from ..common.imageUtil import generate_crop_data
from ..common.imageUtil import crop_images
from ..common.imageUtil import convert_to_dct
from ..common.imageUtil import find_browser_view
from ..common.imageUtil import compare_with_sample_image_multi_process
from ..common.imageUtil import CropRegion
from ..common.commonUtil import CommonUtil
from ..common.logConfig import get_logger

logger = get_logger(__name__)


class InputLatencyFrameThroughputGenerator(BaseGenerator):

    def __init__(self, index_config, exec_config, online_config, global_config, input_env):
        super(InputLatencyFrameThroughputGenerator, self).__init__(index_config, exec_config, online_config,
                                                                   global_config, input_env)
        self.ft_generator = FrameThroughputDctGenerator()
        self.il_generator = InputLatencyAnimationDctGenerator()
        self.compare_result = {}

    @staticmethod
    def generate_sample_result(input_generator_name, input_sample_dict, input_sample_index):
        ft_return_result = FrameThroughputDctGenerator.generate_sample_result("FrameThroughputDctGenerator",
                                                                              input_sample_dict,
                                                                              input_sample_index)
        il_return_result = InputLatencyAnimationDctGenerator.generate_sample_result("InputLatencyAnimationDctGenerator",
                                                                                    input_sample_dict,
                                                                                    input_sample_index)
        return ft_return_result.update(il_return_result)

    def crop_images_based_on_samplefiles(self, input_data):
        ft_input_image_list = self.ft_generator.crop_images_based_on_samplefiles(input_data)
        il_input_image_list = self.il_generator.crop_images_based_on_samplefiles(input_data)

        return ft_input_image_list.update(il_input_image_list)

    def generate_result(self, input_data):
        il_compare_result = self.il_generator.generate_result(input_data)
        il_compare_result['il_run_time'] = il_compare_result['run_time']
        del il_compare_result['run_time']

        ft_compare_result = self.ft_generator.generate_result(input_data)
        ft_compare_result['ft_run_time'] = ft_compare_result['run_time']
        del ft_compare_result['run_time']

        self.compare_result = il_compare_result.update(ft_compare_result)

        return self.compare_result

    def output_case_result(self, suite_upload_dp):

        if self.compare_result.get('ft_run_time', None) and self.compare_result.get('il_run_time', None):
            self.record_runtime_current_status(self.compare_result['ft_run_time'])

            history_result_data = CommonUtil.load_json_file(self.env.DEFAULT_TEST_RESULT)
            event_time_dict = self.compare_result.get('event_time_dict', {})
            long_frame = self.compare_result.get('long_frame', 0)
            frame_throughput = self.compare_result.get('frame_throughput', 0)
            freeze_frames = self.compare_result.get('freeze_frames', 0)
            expected_frames = self.compare_result.get('expected_frames', 0)
            actual_paint_frames = self.compare_result.get('actual_paint_frames', 0)

            run_time_dict = {'ft_run_time': self.compare_result['ft_run_time'],
                             'il_run_time': self.compare_result['il_run_time'],
                             'folder': self.env.output_name,
                             'freeze_frames': freeze_frames,
                             'long_frame': long_frame,
                             'frame_throughput': frame_throughput,
                             'expected_frames': expected_frames,
                             'actual_paint_frames': actual_paint_frames,
                             'event_time': event_time_dict}

            # init result dict if not exist
            init_result_dict = self.init_result_dict_variable(
                ['total_run_no', 'error_no'], ['time_list', 'detail'])
            update_result = history_result_data.get(self.env.test_name, init_result_dict)

            # based on current result add the data to different field
            history_result_data[self.env.test_name] = self.generate_update_result_for_combination(
                                                                   update_result, self.compare_result, run_time_dict)

            # dump to json file
            with open(self.env.DEFAULT_TEST_RESULT, "wb") as fh: 
                json.dump(history_result_data, fh, indent=2)
            self.status_recorder.record_current_status({self.status_recorder.STATUS_TIME_LIST_COUNTER: str(len(history_result_data[self.env.test_name]['time_list']))})
        else:
            self.status_recorder.record_current_status({self.status_recorder.STATUS_IMG_COMPARE_RESULT: self.status_recorder.ERROR_COMPARE_RESULT_IS_NONE})

        if self.exec_config['output-result-video-file']:
            start_time = time.time()
            self.output_runtime_result_video(self.compare_result['running_time_result'], suite_upload_dp)
            current_time = time.time()
            elapsed_time = current_time - start_time
            logger.debug("Generate Video Elapsed: [%s]" % elapsed_time)
