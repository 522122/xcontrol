import os
import decky
import asyncio
import json
from settings import SettingsManager

class Api:
    CLI_PATH = os.path.join(decky.DECKY_PLUGIN_DIR, "bin", "cli")
    LOG_PATH = os.path.join(decky.DECKY_PLUGIN_LOG_DIR, "cli.log")

    def __init__(self):
        self.tasks = {}
    
    def _args_to_key(self, args):
        flags = [arg for arg in args if arg.startswith('-')]
        return "".join(flags)
    
    async def _spawn(self, args):
        await asyncio.sleep(2)
        with open(Api.LOG_PATH, "w") as f:
            await asyncio.create_subprocess_exec(
                Api.CLI_PATH, 
                *args,
                stdout=f,
                stderr=asyncio.subprocess.STDOUT,
            )
            
    # run command and return output
    async def read(self, args):
        with open(Api.LOG_PATH, "w") as f:
            process = await asyncio.create_subprocess_exec(
                Api.CLI_PATH,
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=f,
            )
        
        stdout, _ = await process.communicate()
            
        return stdout.decode().strip()
        
    # debounced process spawning without output
    def run(self, args):
        id = self._args_to_key(args)
        if id in self.tasks:
            self.tasks[id].cancel()
            self.tasks.pop(id)
            
        task = asyncio.create_task(self._spawn(args))
        self.tasks[id] = task
        
        def cleanup(task):
            if not task.cancelled():
                self.tasks.pop(id)
        
        task.add_done_callback(cleanup)

class Services:
    CLI_PATH = "/usr/bin/systemctl"

    def __init__(self):
        self.tasks = {}
        
    async def _spawn(self, args):
        await asyncio.sleep(2)
        await asyncio.create_subprocess_exec(
            Services.CLI_PATH, 
            *args,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        
    async def read(self, args):
        process = await asyncio.create_subprocess_exec(
            Services.CLI_PATH,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await process.communicate()            
        return stdout.decode().strip()
        
    def run(self, args):
        id = args[1]
        if id in self.tasks:
            self.tasks[id].cancel()
            self.tasks.pop(id)
            
        task = asyncio.create_task(self._spawn(args))
        self.tasks[id] = task
        
        def cleanup(task):
            if not task.cancelled():
                self.tasks.pop(id)
        
        task.add_done_callback(cleanup)

class Plugin:        
        
    async def write(self, args):
        flag, value = args
        if flag == "start" or flag == "stop":
            self.settings.setSetting(f"service-{value}", flag)
            self.services.run([flag, value])
            return
        else:
            flag = f"-{flag}"
            value = str(value)
            self.settings.setSetting(flag, value)
            self.api.run([flag, value])
        
    async def read(self):
        cli_data = await self.api.read(["-json"])
        is_sshd_active = await self.services.read(["is-active", "sshd"])
        json_cli_data = json.loads(cli_data)
        return {**json_cli_data, **{"sshd": "start" if is_sshd_active == "active" else "stop"}}
    
    def write_on_load(self):
        cli_cmd = []
        for arg, value in self.settings.settings.items():
            if arg.startswith("service-"):
                service_name = arg.split("-")[1]
                decky.logger.info(f"Initializing services: {service_name} {value}")
                self.services.run([value, service_name])
            else:
                cli_cmd.append(arg)
                cli_cmd.append(value)
        if len(cli_cmd) == 0:
            return
        decky.logger.info(f"Initializing cli: {cli_cmd}")
        self.api.run(cli_cmd)
        
    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        self.settings = SettingsManager("settings", decky.DECKY_PLUGIN_SETTINGS_DIR)
        # self.settings.read()
        self.api = Api()
        self.services = Services()
        self.write_on_load()
        # self.loop = asyncio.get_event_loop()
        decky.logger.info("Initialized")

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky.logger.info("Goodnight World!")

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky.logger.info("Goodbye World!")

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky.logger.info("Migrating")
        # Here's a migration example for logs:
        # - `~/.config/decky-template/template.log` will be migrated to `decky.decky_LOG_DIR/template.log`
        # decky.migrate_logs(os.path.join(decky.DECKY_USER_HOME,
        #                                        ".config", "decky-template", "template.log"))
        # Here's a migration example for settings:
        # - `~/homebrew/settings/template.json` is migrated to `decky.decky_SETTINGS_DIR/template.json`
        # - `~/.config/decky-template/` all files and directories under this root are migrated to `decky.decky_SETTINGS_DIR/`
        # decky.migrate_settings(
        #     os.path.join(decky.DECKY_HOME, "settings", "template.json"),
        #     os.path.join(decky.DECKY_USER_HOME, ".config", "decky-template"))
        # Here's a migration example for runtime data:
        # - `~/homebrew/template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        # - `~/.local/share/decky-template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        # decky.migrate_runtime(
        #     os.path.join(decky.DECKY_HOME, "template"),
        #     os.path.join(decky.DECKY_USER_HOME, ".local", "share", "decky-template"))
