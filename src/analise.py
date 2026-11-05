import os
import hashlib

# Maak seker die naam pas presies by jou lêer
leernaam = "Commando (1986)(Torquemada).prg"

try:
    grootte = os.path.getsize(leernaam)
    with open(leernaam, "rb") as f:
        data = f.read()
        laai_adres = data[0] + (data[1] << 8)
        kontrolesom = hashlib.sha256(data).hexdigest()

    print("--- LÊER ANALISE ---")
    print(f"Lêergrootte: {grootte} grepe")
    print(f"Laai-adres (heksadesimaal): {hex(laai_adres)}")
    print(f"SHA-256 Kontrolesom: {kontrolesom}")
    print("--------------------")
except FileNotFoundError:
    print(f"Fout: Kon nie die lêer '{leernaam}' in hierdie gids vind nie.")
  
