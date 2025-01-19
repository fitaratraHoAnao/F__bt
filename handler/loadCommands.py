import os
import importlib

commands = {}

def loadCommands(_prefix):
    global commands
    if commands:
        return commands
    files = list(filter(lambda file: file.endswith('.py') and file != '__init__.py', os.listdir('./commands')))
    print("\033[97m⦿━━━━━━━━━━━━━━━⦿ \033[96mLoad Commands\033[97m ⦿━━━━━━━━━━━━━━━⦿")
    
    for file in files:
        filepath = f"commands.{os.path.splitext(file)[0]}"
        try:
            module = importlib.import_module(filepath)
            config = getattr(module, 'config', None)
            if config:
                name = config.get('name')
                function = config.get('def')
                if not name:
                    print(f"\033[31m[COMMAND]\033[0m{file} NOT LOADED - Missing command name")
                elif not function:
                    print(f"\033[31m[COMMAND]\033[0m{file} NOT LOADED - Missing command function")
                else:
                    usePrefix = config.get('usePrefix', True)
                    if not name.isalnum():
                        print(f"\033[31m[COMMAND]\033[0m{file} NOT LOADED - Invalid command name")
                    elif name.lower() in commands:
                        print(f"\033[31m[COMMAND]\033[0m{file} NOT LOADED - Command name already exists")
                    elif usePrefix not in [True, False]:
                        print(f"\033[31m[COMMAND]\033[0m{file} NOT LOADED - Invalid usePrefix value")
                    else:
                        admin_only = config.get('admin_only', False)
                        config["usage"] = config.get("usage", "").replace('{p}', _prefix)
                        config["description"] = config.get("description", 'No description.').replace('{p}', _prefix)
                        commands[name.lower()] = config
                        print(f"\033[36m[COMMAND] \033[0mLOADED \033[33m{name} \033[0m- \033[35m({file})\033[0m")
        except Exception as e:
            print(f"\033[31m[COMMAND] Error loading {file}: {e}\033[0m")
    print()
    return commands
