import subprocess
import psutil

def find_keysec_process():
    """Find the KeySec process."""
    for proc in psutil.process_iter():
        try:
            if "keysec_executable" in proc.name():
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def restart_keysec():
    """Restart KeySec."""
    keysec_process = find_keysec_process()
    if keysec_process:
        try:
            keysec_process.kill()
            print("KeySec process terminated.")
        except Exception as e:
            print("Error terminating KeySec process:", e)
    
    # Start KeySec again
    try:
        subprocess.Popen(['keysec_executable'])
        print("KeySec restarted successfully.")
    except Exception as e:
        print("Error restarting KeySec:", e)

if __name__ == "__main__":
    restart_keysec()
