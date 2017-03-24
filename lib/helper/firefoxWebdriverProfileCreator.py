import os
import time
from lib.helper.firefoxProfileCreator import FirefoxProfileCreator
from selenium import webdriver
from lib.common.logConfig import get_logger
from ..common.environment import Environment

logger = get_logger(__name__)


class FirefoxWebdriverProfileCreator(FirefoxProfileCreator):
    def __init__(self, firefox_profile_path=''):
        self._firefox_profile_path = firefox_profile_path
        self._firefox_profile = None

    def _create_firefox_profile(self):
        logger.info('Creating Profile')
        self._firefox_profile = webdriver.FirefoxProfile()
        self._firefox_profile_path = self._firefox_profile.path
        logger.info('Creating Profile Successfully: {}'.format(self._firefox_profile_path))
        return self._firefox_profile_path

    def _set_prefs(self, prefs={}):
        # load all related preferences
        for k, v in prefs.items():
            self._firefox_profile.set_preference(str(k), v)
        # Skip First Run page
        self._firefox_profile.set_preference("toolkit.startup.last_success", format(int(time.time())))
        self._firefox_profile.set_preference("browser.startup.homepage_override.mstone", "ignore")
        self._firefox_profile.update_preferences()

    def _install_profile_extensions(self, extensions_settings={}):
        if extensions_settings:
            import_extensions_folder = Environment.DEFAULT_EXTENSIONS_DIR

            for name in extensions_settings.keys():
                ext = extensions_settings[name]
                if not ext['enable']:
                    logger.info(name + ' set to be disabled.')
                    continue

                logger.info(name + ' is enabled.')
                if len(ext['XPI']) == 0:
                    logger.info('It requires no additional add-on to be installed')
                    continue

                for xpi in ext['XPI']:
                    logger.info('Installing "' + xpi + '" add-on now.')

                    xpi_loc = os.path.join(import_extensions_folder, xpi, xpi + ".xpi")
                    self._firefox_profile.add_extension(xpi_loc)
