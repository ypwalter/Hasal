# if you are putting your test script folders under {git project folder}/tests/, it will work fine.
# otherwise, you either add it to system path before you run or hard coded it in here.
sys.path.append(sys.argv[2])
import browser
import common
import facebook

com = common.General()
chrome = browser.Chrome()
fb = facebook.facebook()

chrome.clickBar()
chrome.enterLink(sys.argv[3])

sleep(2)
setAutoWaitTimeout(10)
fb.wait_for_loaded()
fb.click_post_area_home()

sample2_fp = os.path.join(sys.argv[4], sys.argv[5].replace('sample_1', 'sample_2'))

sleep(2)
capture_width = int(sys.argv[6])
capture_height = int(sys.argv[7])

t1 = time.time()
capimg2 = capture(0, 0, capture_width, capture_height)

print('[log]  TYPE "a"')
type("a")
sleep(1)
t2 = time.time()
with open(sys.argv[8], "r+") as fh:
    timestamp = json.load(fh)
    timestamp['t1'] = t1
    timestamp['t2'] = t2
    fh.seek(0)
    fh.write(json.dumps(timestamp))
shutil.move(capimg2, sample2_fp.replace(os.path.splitext(sample2_fp)[1], '.png'))


