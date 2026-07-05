from datetime import datetime

APP_NAME = "NiftyAI Pro"
VERSION = "0.1.0"

def main():
    print("=" * 50)
    print(f"{APP_NAME}")
    print(f"Version : {VERSION}")
    print(f"Started : {datetime.now()}")
    print("=" * 50)

if __name__ == "__main__":
    main()