sys.path.append(sys.argv[2])
import browser
import common

com = common.General()
ff = browser.Firefox()

wait(2)
ff.focus()
type("a", Key.CTRL)
type(Key.DELETE)
