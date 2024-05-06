import subprocess

def start_keysec():
    try:
        # Replace 'keysec_executable' with the actual path to the KeySec executable
        subprocess.Popen(['keysec_executable'])
        print("KeySec started successfully.")
    except Exception as e:
        print("Error starting KeySec:", e)

if __name__ == "__main__":
    start_keysec()
