import traceback
import time
import os
import importlib
from email_utils import send_alert_email


def run_sync(request):
    logs = []

    def log(msg):
        print(msg)
        logs.append(msg)

    def run_with_retry(module_name, func, retries=3, delay=3):
        log(f"🔄 Starting {module_name}.run() with retry logic...")
        for attempt in range(1, retries + 1):
            try:
                log(f"🔁 Attempt {attempt} for {module_name}...")
                func()
                log(f"✅ {module_name} succeeded on attempt {attempt}.\n")
                break
            except Exception as e:
                log(f"⚠️ {module_name} failed on attempt {attempt}: {str(e)}")
                log(traceback.format_exc())
                if attempt < retries:
                    log(f"⏳ Retrying {module_name} in {delay} seconds...\n")
                    time.sleep(delay)
                else:
                    log(f"❌ {module_name} failed after {retries} attempts.\n")
                    send_alert_email(module_name, str(e), traceback.format_exc())
        time.sleep(3)

    log("🚀 Starting full sync from dynamic scripts...\n")

    # Auto-load all modules from sync_scripts folder
    script_dir = "sync_scripts"
    for filename in os.listdir(script_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = filename[:-3]
            full_module_path = f"{script_dir}.{module_name}"
            try:
                module = importlib.import_module(full_module_path)
                run_func = getattr(module, "run", None)
                if callable(run_func):
                    run_with_retry(module_name, run_func)
                else:
                    log(f"⚠️ Skipping {module_name}: no `run()` function defined.\n")
            except Exception as e:
                log(f"❌ Failed to import {module_name}: {str(e)}\n")
                log(traceback.format_exc())

    log("🏁 Sync finished.")
    return ("\n".join(logs), 200)
