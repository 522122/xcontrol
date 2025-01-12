import os
import decky
import asyncio
import json

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
    
class Plugin:        
        
    async def write(self, args):
        flag, value = args
        self.api.run([f"-{flag}", str(value)])
        
    async def read(self):
        data = await self.api.read(["-json"])
        return json.loads(data)
        
    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        self.api = Api()
        self.loop = asyncio.get_event_loop()
        decky.logger.info("Hello World!")

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
