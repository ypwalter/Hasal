# if you are putting your test script folders under {git project folder}/tests/, it will work fine.
# otherwise, you either add it to system path before you run or hard coded it in here.

INPUT_LIB_PATH = sys.argv[1]
sys.path.append(INPUT_LIB_PATH)

import os
import common
import basecase
import gsearch

import shutil
import browser
import time


class Case(basecase.SikuliInputLatencyCase):

    def run(self):
        sample1_fp = os.path.join(self.INPUT_IMG_SAMPLE_DIR_PATH, self.INPUT_IMG_OUTPUT_SAMPLE_1_NAME)
        sample2_fp = os.path.join(self.INPUT_IMG_SAMPLE_DIR_PATH, self.INPUT_IMG_OUTPUT_SAMPLE_1_NAME.replace('sample_1', 'sample_2'))

        # Disable Sikuli action and info log
        com = common.General()
        com.infolog_enable(0)
        com.set_mouse_delay(0)

        chrome = browser.Chrome()
        gs = gsearch.Gsearch()

        chrome.clickBar()
        chrome.enterLink(sys.argv[3])
        gs.wait_gimage_loaded()

        sleep(2)
        gs.hover_result_image(1, 1)

        sleep(2)
        capture_width = int(sys.argv[6])
        capture_height = int(sys.argv[7])

        t1 = time.time()
        capimg1 = capture(0, 0, capture_width, capture_height)

        mouseDown(Button.LEFT)
        com.system_print('[log]  Mouse up on first image')
        mouseUp(Button.LEFT)
        # gs.click_result_image(1, 1)
        sleep(2)
        t2 = time.time()
        capimg2 = capture(0, 0, capture_width, capture_height)
        com.updateJson({'t1': t1, 't2': t2}, sys.argv[8])
        shutil.move(capimg1, sample1_fp.replace(os.path.splitext(sample1_fp)[1], '.png'))
        shutil.move(capimg2, sample2_fp.replace(os.path.splitext(sample1_fp)[1], '.png'))
        com.set_mouse_delay()


case = Case(sys.argv)
case.run()

