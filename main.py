import argparse

from src.ui.initialize_app import initialize_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--en', action='store_true', help='Set language to English')
    args = parser.parse_args()

    if args.en:
        language = 'en'
    else:
        language = 'pl'
    
    initialize_app(language)