import importlib
import os

def load_handlers(bot, folder: str):
    for filename in os.listdir(folder):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_path = f"{folder.replace('/', '.')}.{filename[:-3]}"
            module = importlib.import_module(module_path)
            if hasattr(module, "setup"):
                module.setup(bot)
                print(f"  ✅ Loaded: {filename}")
            else:
                print(f"  ⚠️  Skipped: {filename} (no setup() found)")