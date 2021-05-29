import hashlib
import json

def cryptohash(*args):
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringified_args)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"cryptohash('one', 2, [3]): {cryptohash('one', 2, [3])}")
    print(f"cryptohash(2, [3], 'one': {cryptohash(2, [3], 'one')}")

if __name__ == '__main__':
    main()
