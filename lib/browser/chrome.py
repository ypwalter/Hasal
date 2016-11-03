from base import BrowserBase
import subprocess


class BrowserChrome(BrowserBase):
    windows_chrome_command = 'chrome'
    ubuntu_chrome_command = 'google-chrome'
    darwin_chrome_command = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    def get_browser_settings(self, **kwargs):
        default_tracing_capture_period = 900  # sec
        self.browser_process = "chrome"
        self.process_name = "chrome"
        if self.current_platform_name == "darwin":
            self.command = self.darwin_chrome_command
        elif self.current_platform_name == "linux2":
            self.command = self.ubuntu_chrome_command
        else:
            self.command = self.windows_chrome_command
        self.launch_cmd = [self.command,
                           "--window-size=" + str(self.windows_size_width) + "," + str(self.window_size_height)]

        if "tracing_path" in kwargs:
            self.launch_cmd.extend(["--trace-startup", "--trace-startup-file=" + kwargs['tracing_path'], "--trace-startup-duration=" + str(default_tracing_capture_period)])

    def get_version_command(self):
        if self.current_platform_name == "darwin" or self.current_platform_name == "linux2":
            return [self.command, "--version"]
        else:
            return ['reg', 'query', 'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon', '/v', 'version']

    def get_version(self):
        cmd = self.get_version_command()
        if self.current_platform_name == "darwin" or self.current_platform_name == "linux2":
            return_version = subprocess.check_output(cmd).splitlines()[0].split(" ")[2]
        else:
            return_version = subprocess.check_output(cmd).splitlines()[2].split()[2]
        return return_version
