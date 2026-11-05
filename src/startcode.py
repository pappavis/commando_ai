leernaam = "Commando (1986)(Torquemada).prg"

try:
    with open(leernaam, "rb") as f:
        data = f.read()

    # De eerste 2 bytes zijn het laadadres (0x0801), dus we kijken naar wat daarna komt
    code_bytes = data[2:34]

    print("--- EERSTE 32 BYTES VAN DE CODE ---")
    hex_weergave = " ".join([f"{b:02x}" for b in code_bytes])
    print(hex_weergave)
    print("-----------------------------------")
except FileNotFoundError:
    print(f"Fout: Kan {leernaam} niet vinden.")
    
