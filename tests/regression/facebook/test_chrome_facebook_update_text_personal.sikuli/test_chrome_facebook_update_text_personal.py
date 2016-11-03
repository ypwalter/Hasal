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
click(fb.non_club_post_marker.targetOffset(75, 35))
click(fb.non_club_post_menu_edit)
wait(fb.save_button)
type(Key.ENTER)
paste('add new line')
sleep(1)
click(fb.save_button)
wait(fb.personal_post_area)
