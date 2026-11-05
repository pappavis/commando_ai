leernaam = "Commando (1986)(Torquemada).prg"

with open(leernaam, "rb") as f:
    data = f.read()

# De machinecode begint na de BASIC-regel (wat overeenkomt met de 18e byte in het bestand)
start_index = 16 
code_bytes = data[start_index:start_index+15]

print("--- DE EERSTE UITPAK-INSTRUCTIES ---")
print("Hexadecimaal: ", " ".join([f"{b:02x}" for b in code_bytes]))
print("------------------------------------")


