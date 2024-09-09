import itertools
from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip39MnemonicDecoder, Bip32Slip10Secp256k1
import hashlib
import base58

# Liste der 12 identifizierten Wörter
words = ["moon", "tower", "food", "matter", "police", "this", "subject", "real", "black", "hold", "liberty", "rain"]
#words = ["abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "abandon", "about", "abandon", "abandon"]
# 12!=479,001,600, 24!=620,448,401,733,239,439,360,000
 

# Zieladresse
#target_address = "13iX7DteNj1gV7zhe4t6o9FX9CArR5wZxz" # abadon...
target_address = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ" 

def generate_btc_address_from_seed(seed):
    bip32_ctx = Bip32Slip10Secp256k1.FromSeed(seed)
    # Ableitung des Pfades m/0/0
    child_ctx = bip32_ctx.ChildKey(0).ChildKey(0)
    child_public_key = child_ctx.PublicKey().RawCompressed().ToHex()

    # Bitcoin-Adresse generieren
    public_key_bytes = bytes.fromhex(child_public_key)
    sha256 = hashlib.sha256(public_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    network_byte = b'\x00' + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    address = base58.b58encode(network_byte + checksum)
    return address.decode()

# Prüfe jede Permutation
i = 0
for permutation in itertools.permutations(words):
    mnemonic = " ".join(permutation)
    
    if (i % 1000) == 0:
       print(i)
    #	break
    print(i)
    i += 1
    
    # Überprüfe, ob die Mnemonic gültig ist
    if Bip39MnemonicValidator().IsValid(mnemonic):
        # Generiere den Seed
        seed = Bip39SeedGenerator(mnemonic).Generate()
        #print(i)
        #print(" " +  mnemonic )
        # Generiere die Bitcoin-Adresse
        btc_address = generate_btc_address_from_seed(seed)
        #print(btc_address + " ist gültig" )
        # Prüfe, ob die generierte Adresse der Zieladresse entspricht
        if btc_address == target_address:
            print(f"Gefunden! Die richtige Seed-Phrase lautet: {mnemonic}")
            break
else:
    print("Keine passende Seed-Phrase gefunden.")
