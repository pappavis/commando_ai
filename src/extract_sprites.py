"""
PROJEK RETRORECON - COMMODORE 64 COMMANDO SPRITE ONTTREKKER
Werkstroom A: Bronontleding van Grafiese Bates
"""

import os

PRG_FILE = "extracted_d64/COMMANDO.prg"
OUT_DIR = "/tmp/onttrekte_sprites"
os.makedirs(OUT_DIR, exist_ok=True)

# Commodore 64 RGB Kleurpalet
C64_PALETTE = {
    0: (0, 0, 0),        # Swart
    1: (255, 255, 255),  # Wit
    2: (136, 0, 0),      # Rooi
    3: (170, 255, 238),  # Siaan
    4: (204, 68, 204),   # Pers
    5: (0, 204, 85),     # Groen
    6: (0, 0, 170),      # Blou
    7: (238, 238, 119),  # Geel
    8: (221, 136, 85),   # Oranje
    9: (102, 68, 0),     # Bruin
    10: (255, 119, 119), # Ligrooi
    11: (51, 51, 51),    # Donkergrys
    12: (119, 119, 119), # Mediumgrys
    13: (170, 255, 102), # Liggroen
    14: (0, 136, 255),   # Ligblou
    15: (187, 187, 187), # Ligrys
}

with open(PRG_FILE, "rb") as f:
    raw = f.read()

payload = raw[2:]
base_addr = 0x0801

# Ons soek alle geldige 64-greep sprite-blokke
sprites_found = []
for i in range(0, len(payload) - 64, 64):
    blk = payload[i:i+64]
    non_zero = sum(1 for r in range(21) if any(blk[r*3:r*3+3]))
    bits = sum(bin(b).count("1") for b in blk[:63])
    if 4 <= non_zero <= 21 and 15 <= bits <= 200:
        addr = base_addr + i
        sprites_found.append((addr, i, blk))

print(f"Totaal kandidate geïdentifiseer: {len(sprites_found)}")

# Stoor as PPM-beeldlêers (kan direk op Mac oopgemaak word met Preview)
# Kleurkonfigurasie soos in Commando masjienkode ($3D44-$3D49):
# $D025 = 15 (Ligrys), $D026 = 0 (Swart), Speler-kleur = 5 (Groen), Agtergrond = Deursigtig/Wit
def save_ppm(filename, blk, main_color=5, mc1=15, mc2=0):
    width, height = 24, 21
    pixels = []
    
    color_map = {
        0: (255, 255, 255),      # Deursigtig (as wit vertoon vir voorskou)
        1: C64_PALETTE[mc1],     # Multi-color 1 ($D025)
        2: C64_PALETTE[main_color], # Speler-kleur ($D027)
        3: C64_PALETTE[mc2],     # Multi-color 2 ($D026)
    }
    
    for r in range(21):
        row = blk[r*3 : r*3+3]
        for b in row:
            for s in (6, 4, 2, 0):
                c_idx = (b >> s) & 3
                rgb = color_map[c_idx]
                pixels.extend([rgb, rgb]) # Dubbele wydte vir C64 multi-color
                
    # Skryf PPM P6 (binêre formaat)
    with open(filename, "wb") as f_out:
        header = f"P6\n{width} {height}\n255\n".encode("ascii")
        f_out.write(header)
        for r, g, b in pixels:
            f_out.write(bytes([r, g, b]))

for idx, (addr, offset, blk) in enumerate(sprites_found[:30]):
    ppm_name = os.path.join(OUT_DIR, f"sprite_{idx:02d}_addr_{addr:04X}.ppm")
    save_ppm(ppm_name, blk)

print(f"Die eerste 30 sprites is suksesvol gestoor in gids '{OUT_DIR}/'.")
