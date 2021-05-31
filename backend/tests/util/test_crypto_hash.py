from backend.util.cryptohash import cryptohash

# It should create the same hash with arguements of data types in different order
def test_crypto_hash():
    
    assert cryptohash(1 , [2], 'three') == cryptohash('three', 1, [2])
    assert cryptohash('Ultimate') == '899332326e9912504026e5901cbd228d388ea6808b35e1029fc58bb9c0fc9f5c'
