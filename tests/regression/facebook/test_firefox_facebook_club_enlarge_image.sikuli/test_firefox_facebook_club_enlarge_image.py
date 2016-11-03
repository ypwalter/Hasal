# if you are putting your test script folders under {git project folder}/tests/, it will work fine.
# otherwise, you either add it to system path before you run or hard coded it in here.
sys.path.append(sys.argv[2])
import browser
import common
import facebook

com = common.General()
ff = browser.Firefox()
fb = facebook.facebook()

ff.clickBar()
ff.enterLink(sys.argv[3])

sleep(2)
fb.wait_for_loaded()
fb.focus_window()
wait(fb.club_post_header)
click(fb.club_post_header.targetOffset(0, 200))
mouseMove(Location(0, 0))
fb.wait_post_area_vanish(location='club')
