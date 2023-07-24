import secrets
import sys

if __name__ == "__main__":
    print(secrets.token_hex(int(sys.argv[1])))
