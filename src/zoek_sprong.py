leernaam = "Commando (1986)(Torquemada).prg"

with open(leernaam, "rb") as f:
    data = f.read()

# We zoeken in het uitpak-gedeelte naar de instructie '4c' (JMP)
print("--- ZOEKEN NAAR DE START SPRONG ---")
for i in range(17, 150):
    if data[i] == 0x4c:  # 0x4c is de JMP (Jump) instructie
        doel_adres = data[i+1] + (data[i+2] << 8)
        print(f"JMP instructie gevonden op byte-positie {i}")
        print(f"Het spel start op het adres: {hex(doel_adres)}")
        break
print("-----------------------------------")

