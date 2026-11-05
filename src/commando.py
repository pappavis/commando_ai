"""
PROJEK RETRORECON — COMMODORE 64 COMMANDO REKONSTRUKSIE (v0.4.0-release)
Vrystelling-ChatID: RRC-D00-13
Metodologie: RETRORECON (D00 v1.3 & D01 v1.1-RC)
Oorspronklike Spel: Commando (Commodore 64, Capcom / Elite Systems 1985)
Programmering: Chris Butler | Grafika: Rory Green & Chris Harvey | Musiek: Rob Hubbard
Inkrement 2: Rob Hubbard Musiek (Opsie A), Vyand-AI & Vragmotors (Opsie B) en Vlak 2 Hangbrug (Opsie C)
"""

import os
import json
import math
import random
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any
from sound_effects import sounds

# ==============================================================================
# 1. RIGTINGE EN KONSTANTES (Chris Butler se 8-rigting hoekkodes)
# ==============================================================================

class GameMode(Enum):
    TITLE = "TITLE"
    DEMO = "DEMO"
    PLAYING = "PLAYING"
    NAME_ENTRY = "NAME_ENTRY"
    HALL_OF_FAME = "HALL_OF_FAME"

class Direction(Enum):
    UP = 0
    UP_RIGHT = 2
    RIGHT = 4
    DOWN_RIGHT = 6
    DOWN = 8
    DOWN_LEFT = 10
    LEFT = 12
    UP_LEFT = 14

DIRECTION_VECTORS = {
    Direction.UP:         ( 0.0, -1.0),
    Direction.UP_RIGHT:   ( 0.7071, -0.7071),
    Direction.RIGHT:      ( 1.0,  0.0),
    Direction.DOWN_RIGHT: ( 0.7071,  0.7071),
    Direction.DOWN:       ( 0.0,  1.0),
    Direction.DOWN_LEFT:  (-0.7071,  0.7071),
    Direction.LEFT:       (-1.0,  0.0),
    Direction.UP_LEFT:    (-0.7071, -0.7071),
}

# Commodore 64 RGB Kleurpalet
C64_PALETTE = {
    0:  "#000000",  # Swart
    1:  "#FFFFFF",  # Wit
    2:  "#880000",  # Rooi (Super Joe kopband)
    3:  "#AAFFEE",  # Siaan / Waterglans
    4:  "#CC44CC",  # Pers
    5:  "#00CC55",  # Groen (Super Joe uniform)
    6:  "#0000AA",  # Blou (Vyand uniform)
    7:  "#EEEE77",  # Geel / Velkleur
    8:  "#DD8855",  # Oranje
    9:  "#664400",  # Bruin (Houtbrug & stewels)
    10: "#FF7777",  # Ligrooi
    11: "#333333",  # Donkergrys
    12: "#777777",  # Mediumgrys
    13: "#AAFF66",  # Liggroen (Palmbome)
    14: "#0088FF",  # Ligblou (Rivierwater)
    15: "#BBBBBB",  # Liggrys
}

class ObstacleType(Enum):
    SANDBAGS = 1
    TREE = 2
    TRENCH = 3
    BARRICADE = 4
    FORTRESS_WALL = 5
    FORTRESS_GATE = 6
    RIVER = 7
    BRIDGE = 8

class EnemyType(Enum):
    SOLDIER = 1
    CROUCHING_GUNNER = 2
    OFFICER_RUNNER = 3
    GATE_GUARD = 4

# ==============================================================================
# 2. HINDERNISSE, ONTPLOFFINGS EN GRANATE
# ==============================================================================

class Obstacle:
    def __init__(self, x: float, y: float, kind: ObstacleType, width: float = 24.0, height: float = 16.0):
        self.x = float(x)
        self.y = float(y)
        self.kind = kind
        self.width = width
        self.height = height
        self.is_alive = True
        self.is_destructible = kind in (ObstacleType.SANDBAGS, ObstacleType.BARRICADE)

    def contains_point(self, px: float, py: float) -> bool:
        hw = self.width / 2.0
        hh = self.height / 2.0
        return (self.x - hw <= px <= self.x + hw) and (self.y - hh <= py <= self.y + hh)


class Explosion:
    def __init__(self, x: float, y: float, radius: float = 24.0):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.timer = 18
        self.max_timer = 18
        self.is_alive = True

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.is_alive = False


class Grenade:
    def __init__(self, start_x: float, start_y: float, direction: Direction, distance: float = 54.0):
        self.start_x = float(start_x)
        self.start_y = float(start_y)
        dx, dy = DIRECTION_VECTORS[direction]
        self.target_x = self.start_x + dx * distance
        self.target_y = self.start_y + dy * distance
        self.x = self.start_x
        self.y = self.start_y
        self.total_ticks = 20
        self.ticks_left = 20
        self.altitude = 0.0
        self.is_alive = True

    def update(self, game_state: "GameState"):
        if not self.is_alive:
            return

        self.ticks_left -= 1
        progress = 1.0 - (self.ticks_left / self.total_ticks)
        self.x = self.start_x + (self.target_x - self.start_x) * progress
        self.y = self.start_y + (self.target_y - self.start_y) * progress
        self.altitude = math.sin(progress * math.pi) * 16.0

        if self.ticks_left <= 0:
            self.is_alive = False
            exp = Explosion(self.target_x, self.target_y, radius=26.0)
            game_state.explosions.append(exp)
            sounds.play("explosion", volume=0.7)

            # Area of Effect skade teen vyande (tref selfs hurkende vyande in loopgrawe!)
            for enemy in game_state.enemies:
                if enemy.is_alive and math.hypot(enemy.x - self.target_x, enemy.y - self.target_y) <= exp.radius + 10:
                    enemy.is_alive = False
                    game_state.player.score += 250
                    sounds.play("enemy_hit", volume=0.45)

            # Vernietig sandsakke
            for obs in game_state.obstacles:
                if obs.is_alive and obs.is_destructible and math.hypot(obs.x - self.target_x, obs.y - self.target_y) <= exp.radius:
                    obs.is_alive = False
                    game_state.player.score += 500


# ==============================================================================
# 3. KOEËLS, VYANDE, VRAGMOTORS EN SPELER
# ==============================================================================

class Bullet:
    def __init__(self, x: float, y: float, direction: Direction, speed: float = 6.0, is_player: bool = True):
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.speed = speed
        self.is_player = is_player
        self.is_alive = True
        dx, dy = DIRECTION_VECTORS[direction]
        self.dx = dx * speed
        self.dy = dy * speed
        self.range_left = 180.0

    def update(self, game_state: "GameState"):
        self.x += self.dx
        self.y += self.dy
        self.range_left -= self.speed

        if self.range_left <= 0:
            self.is_alive = False
            return

        if self.x < game_state.min_x or self.x > game_state.max_x or self.y < 0 or self.y > game_state.world_height:
            self.is_alive = False
            return

        for obs in game_state.obstacles:
            if obs.is_alive and obs.kind not in (ObstacleType.TRENCH, ObstacleType.RIVER, ObstacleType.BRIDGE) and obs.contains_point(self.x, self.y):
                self.is_alive = False
                return


class Enemy:
    def __init__(self, x: float, y: float, kind: EnemyType = EnemyType.SOLDIER):
        self.x = float(x)
        self.y = float(y)
        self.kind = kind
        self.direction = Direction.DOWN
        self.is_alive = True
        self.anim_frame = 0
        self.anim_timer = 0

        # Spoed en gedrag volgens tipe
        if kind == EnemyType.OFFICER_RUNNER:
            self.speed = 2.4  # Vinnige stormloop
            self.shoot_timer = 9999  # Storm met mes
        elif kind == EnemyType.CROUCHING_GUNNER:
            self.speed = 0.0  # Hurk agter dekking
            self.shoot_timer = 45
        elif kind == EnemyType.GATE_GUARD:
            self.speed = 0.0
            self.shoot_timer = 35
        else:
            self.speed = 1.0  # Standaard infanterie
            self.shoot_timer = 50

        self.is_crouching = (kind == EnemyType.CROUCHING_GUNNER)
        self.crouch_timer = 40

    def update(self, game_state: "GameState"):
        if not self.is_alive:
            return

        # 1. Hurkende vyande wissel tussen dekking en skiet
        if self.kind == EnemyType.CROUCHING_GUNNER:
            self.crouch_timer -= 1
            if self.crouch_timer <= 0:
                self.is_crouching = not self.is_crouching
                self.crouch_timer = 45 if self.is_crouching else 35
                if not self.is_crouching:
                    # Staan op en skiet 2 koeëls na speler!
                    game_state.bullets.append(Bullet(self.x, self.y + 6, Direction.DOWN, speed=3.8, is_player=False))
            return

        # 2. Vinnige offisiere storm direk na die speler
        if self.kind == EnemyType.OFFICER_RUNNER:
            dx = game_state.player.x - self.x
            dy = game_state.player.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
            self.anim_timer += 1
            if self.anim_timer >= 4:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 4
            return

        # 3. Hekwagte patrolleer horisontaal
        if self.kind == EnemyType.GATE_GUARD:
            self.x += math.sin(game_state.ticks * 0.08) * 1.4

        # 4. Standaard soldate beweeg af en soek lyn
        if self.kind == EnemyType.SOLDIER:
            dx = game_state.player.x - self.x
            if abs(dx) > 10:
                self.x += math.copysign(0.4, dx)
            self.y += self.speed

        self.anim_timer += 1
        if self.anim_timer >= 6:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4

        # Skiet periodiek
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = 65
            dy = game_state.player.y - self.y
            if 0 < dy < 170:
                game_state.bullets.append(
                    Bullet(self.x, self.y + 8, Direction.DOWN, speed=3.5, is_player=False)
                )

        if self.y > game_state.camera_y + game_state.height + 40:
            self.is_alive = False


class Truck:
    """Militêre vragmotor wat soldate aflaai en wegry."""
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.speed = 1.6
        self.has_deployed = False
        self.is_alive = True
        self.stop_timer = 40
        self.state = "ARRIVING"  # ARRIVING -> STOPPED -> DEPARTING

    def update(self, game_state: "GameState"):
        if not self.is_alive:
            return

        if self.state == "ARRIVING":
            self.y += self.speed
            # Stop by ontplooiingsposisie
            if self.stop_timer > 0:
                self.stop_timer -= 1
            else:
                self.state = "STOPPED"
                self.stop_timer = 30
        elif self.state == "STOPPED":
            if not self.has_deployed:
                self.has_deployed = True
                # Ontplooi 3 vyandelike soldate!
                game_state.enemies.append(Enemy(self.x - 18, self.y, kind=EnemyType.SOLDIER))
                game_state.enemies.append(Enemy(self.x + 18, self.y, kind=EnemyType.SOLDIER))
                game_state.enemies.append(Enemy(self.x, self.y + 12, kind=EnemyType.OFFICER_RUNNER))
            self.stop_timer -= 1
            if self.stop_timer <= 0:
                self.state = "DEPARTING"
        elif self.state == "DEPARTING":
            self.y += self.speed * 1.5
            if self.y > game_state.camera_y + game_state.height + 60:
                self.is_alive = False


class Hostage:
    """Geallieerde soldaat wat as gyselaar / krygsgevangene (POW) aangehou word."""
    def __init__(self, x: float, y: float, guard: Optional["Enemy"] = None):
        self.x = float(x)
        self.y = float(y)
        self.guard = guard
        self.is_rescued = False
        self.is_alive = True
        self.speed = 2.4
        self.anim_frame = 0
        self.anim_timer = 0
        self.score_awarded = False

    def update(self, game_state: "GameState"):
        if not self.is_alive:
            return

        # Kontroleer of wag dood is of Joe naby gekom het om te red
        if not self.is_rescued:
            guard_dead = (self.guard is not None and not self.guard.is_alive)
            dist_to_joe = math.hypot(self.x - game_state.player.x, self.y - game_state.player.y)
            if guard_dead or dist_to_joe < 22:
                self.is_rescued = True
                if not self.score_awarded:
                    self.score_awarded = True
                    game_state.player.score += 1000
                    sounds.play("rescue", volume=0.55)

        # As gyselaar bevry is, hardloop hy vinnig ondertoe na veiligheid!
        if self.is_rescued:
            self.y += self.speed
            self.anim_timer += 1
            if self.anim_timer >= 5:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 4
            if self.y > game_state.camera_y + game_state.height + 40:
                self.is_alive = False


class SupplyCrate:
    """Voorraadkis met handgranate (gemerk met 'G')."""
    def __init__(self, x: float, y: float, kind: str = "GRENADES"):
        self.x = float(x)
        self.y = float(y)
        self.kind = kind
        self.is_alive = True

    def update(self, game_state: "GameState"):
        if not self.is_alive:
            return
        # Botsing met Super Joe
        if abs(self.x - game_state.player.x) < 14 and abs(self.y - game_state.player.y) < 14:
            self.is_alive = False
            game_state.player.grenades += 3
            game_state.player.score += 500
            sounds.play("pickup", volume=0.5)


class HighScoreManager:
    """Bestuur plaaslike hoëtellings op skyf vir C64 Hall of Fame."""
    DEFAULT_SCORES = [
        {"name": "BUTLER", "score": 30000},
        {"name": "HUBBARD", "score": 25000},
        {"name": "GREEN", "score": 20000},
        {"name": "HARVEY", "score": 15000},
        {"name": "JOE", "score": 10000},
    ]

    def __init__(self, filepath: str = "highscores.json"):
        self.filepath = filepath
        self.scores = self.load_scores()

    def load_scores(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return sorted(data, key=lambda x: int(x["score"]), reverse=True)[:5]
            except Exception:
                pass
        return list(self.DEFAULT_SCORES)

    def save_scores(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, indent=2)
        except Exception:
            pass

    def get_scores(self) -> List[Dict[str, Any]]:
        return self.scores

    def is_high_score(self, score: int) -> bool:
        if len(self.scores) < 5:
            return True
        return score > self.scores[-1]["score"]

    def add_score(self, name: str, score: int) -> int:
        """Voeg nuwe telling by en skryf na skyf. Gee rang (1..5) of -1."""
        cleaned_name = (name.strip().upper() or "PLAYER")[:8]
        self.scores.append({"name": cleaned_name, "score": int(score)})
        self.scores.sort(key=lambda x: int(x["score"]), reverse=True)
        self.scores = self.scores[:5]
        self.save_scores()
        for idx, entry in enumerate(self.scores):
            if entry["name"] == cleaned_name and entry["score"] == int(score):
                return idx + 1
        return -1


class ConfigManager:
    """Bestuur konfigurasie-instellings via 'config.json'."""
    DEFAULT_CONFIG = {
        "scanlines": True,
        "music_enabled": True,
        "sound_volume": 0.5,
        "music_volume": 0.35,
    }

    def __init__(self, filepath: str = "config.json"):
        self.filepath = filepath
        self.data: Dict[str, Any] = dict(self.DEFAULT_CONFIG)
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    if isinstance(saved, dict):
                        self.data.update(saved)
            except Exception:
                pass

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self.save()


class DemoAI:
    """Outomatiese AI-beheerder vir Super Joe in Demo / Attract-modus."""
    def __init__(self):
        self.steer_x = 0.0

    def update(self, game_state: "GameState"):
        p = game_state.player
        if not p.is_alive:
            return

        up = True
        down = False
        left = False
        right = False
        fire = False
        grenade = False

        # Vermy hindernisse voor Joe
        for obs in game_state.obstacles:
            if not obs.is_alive: continue
            dy = p.y - obs.y
            dx = obs.x - p.x
            if 0 < dy < 45 and abs(dx) < (obs.width / 2.0 + 12):
                up = False
                if dx >= 0:
                    left = True
                else:
                    right = True

        # Vyande voor Joe
        enemies_ahead = [
            e for e in game_state.enemies
            if e.is_alive and 0 < (p.y - e.y) < 170 and abs(p.x - e.x) < 40
        ]
        if enemies_ahead:
            fire = (game_state.ticks % 4 < 2)

        # Granate gooi teen bunkers of troepe
        if len(enemies_ahead) >= 2 or any(e.is_crouching for e in enemies_ahead):
            if game_state.ticks % 60 == 0:
                grenade = True

        # Flankgrense
        if p.x < 60:
            right = True
            left = False
        elif p.x > game_state.width - 60:
            left = True
            right = False

        p.set_input(up=up, down=down, left=left, right=right, fire=fire, grenade=grenade)


class Player:
    def __init__(self, x: float = 160.0, y: float = 1150.0):
        self.x = float(x)
        self.y = float(y)
        self.direction = Direction.UP
        self.speed = 2.0
        self.is_alive = True
        self.score = 0
        self.grenades = 6
        self.lives = 3
        self.anim_frame = 0
        self.anim_timer = 0
        self.is_moving = False

        self.input_up = False
        self.input_down = False
        self.input_left = False
        self.input_right = False
        self.input_fire = False
        self.input_grenade = False
        self.fire_cooldown = 0
        self.grenade_cooldown = 0

    def set_input(self, up: bool = False, down: bool = False, left: bool = False, right: bool = False, fire: bool = False, grenade: bool = False):
        self.input_up = up
        self.input_down = down
        self.input_left = left
        self.input_right = right
        self.input_fire = fire
        self.input_grenade = grenade

    def fire_weapon(self, game_state: "GameState"):
        if self.fire_cooldown <= 0 and self.is_alive:
            dx, dy = DIRECTION_VECTORS[self.direction]
            bx = self.x + dx * 8
            by = self.y + dy * 8
            game_state.bullets.append(Bullet(bx, by, self.direction, speed=6.0, is_player=True))
            self.fire_cooldown = 8
            sounds.play("shoot", volume=0.35)

    def throw_grenade(self, game_state: "GameState"):
        if self.grenades > 0 and self.grenade_cooldown <= 0 and self.is_alive:
            self.grenades -= 1
            self.grenade_cooldown = 18
            g = Grenade(self.x, self.y, self.direction, distance=54.0)
            game_state.grenades.append(g)
            sounds.play("grenade_throw", volume=0.5)

    def update(self, game_state: "GameState"):
        if not self.is_alive:
            return

        if self.fire_cooldown > 0: self.fire_cooldown -= 1
        if self.grenade_cooldown > 0: self.grenade_cooldown -= 1

        up, down = self.input_up, self.input_down
        left, right = self.input_left, self.input_right

        if up and down: up = down = False
        if left and right: left = right = False

        if up and right: self.direction = Direction.UP_RIGHT
        elif up and left: self.direction = Direction.UP_LEFT
        elif down and right: self.direction = Direction.DOWN_RIGHT
        elif down and left: self.direction = Direction.DOWN_LEFT
        elif up: self.direction = Direction.UP
        elif down: self.direction = Direction.DOWN
        elif left: self.direction = Direction.LEFT
        elif right: self.direction = Direction.RIGHT

        self.is_moving = up or down or left or right

        if self.is_moving:
            dx, dy = DIRECTION_VECTORS[self.direction]
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed

            # Hindernisbotsings
            blocked = False
            on_bridge = any(o.contains_point(new_x, new_y) for o in game_state.obstacles if o.kind == ObstacleType.BRIDGE)
            for obs in game_state.obstacles:
                if not obs.is_alive: continue
                # Soliede versperrings
                if obs.kind in (ObstacleType.SANDBAGS, ObstacleType.TREE, ObstacleType.BARRICADE, ObstacleType.FORTRESS_WALL):
                    if obs.contains_point(new_x, new_y):
                        blocked = True
                        break
                # Rivier blokkeer tensy speler op brug is!
                elif obs.kind == ObstacleType.RIVER and not on_bridge:
                    if obs.contains_point(new_x, new_y):
                        blocked = True
                        break

            if not blocked:
                self.x = new_x
                self.y = new_y

            self.anim_timer += 1
            if self.anim_timer >= 4:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 4
        else:
            self.anim_frame = 0

        self.x = max(game_state.min_x, min(self.x, game_state.max_x))
        self.y = max(game_state.min_y, min(self.y, game_state.max_y))

        if self.input_fire: self.fire_weapon(game_state)
        if self.input_grenade: self.throw_grenade(game_state)


# ==============================================================================
# 4. SPELTOESTAND EN VLAKKE 1 & 2 (GameState)
# ==============================================================================

class GameState:
    def __init__(self, width: int = 320, height: int = 200, world_height: int = 1200, start_mode: GameMode = GameMode.PLAYING):
        self.width = width
        self.height = height
        self.world_height = world_height
        self.min_x = 24.0
        self.max_x = width - 24.0
        self.min_y = 50.0
        self.max_y = world_height - 24.0

        self.mode = start_mode
        self.is_demo = (start_mode == GameMode.DEMO)
        self.demo_timer = 400
        self.demo_ai = DemoAI()
        self.config = ConfigManager()
        self.name_entry_buffer = ""

        self.current_stage = 1
        self.camera_y = float(world_height - height)
        self.player = Player(x=width / 2.0, y=world_height - 50.0)
        self.bullets: List[Bullet] = []
        self.grenades: List[Grenade] = []
        self.explosions: List[Explosion] = []
        self.enemies: List[Enemy] = []
        self.obstacles: List[Obstacle] = []
        self.trucks: List[Truck] = []
        self.hostages: List[Hostage] = []
        self.supply_crates: List[SupplyCrate] = []
        self.high_score_mgr = HighScoreManager()
        self.game_won = False
        self.spawn_timer = 0
        self.ticks = 0

        self.level_completed = False
        self.gate_open = False
        self.gate_guards_cleared = False
        self.stage_transition_timer = 0
        self.stage_banner_text = ""

        self.load_stage(1)

    def update_title(self):
        self.ticks += 1
        if self.demo_timer > 0:
            self.demo_timer -= 1
            if self.demo_timer <= 0:
                self.start_demo()

    def start_demo(self):
        self.mode = GameMode.DEMO
        self.is_demo = True
        self.load_stage(1)
        self.demo_timer = 900  # ~18 sekondes

    def start_game(self):
        self.mode = GameMode.PLAYING
        self.is_demo = False
        self.load_stage(1)
        self.player.score = 0
        self.player.lives = 3
        self.player.grenades = 6
        self.game_won = False
        if self.config.get("music_enabled", True):
            sounds.start_music("theme", volume=self.config.get("music_volume", 0.35))

    def handle_text_input(self, char: str):
        if self.mode == GameMode.NAME_ENTRY:
            if len(self.name_entry_buffer) < 8 and (char.isalnum() or char in " _-"):
                self.name_entry_buffer += char.upper()

    def handle_backspace(self):
        if self.mode == GameMode.NAME_ENTRY and len(self.name_entry_buffer) > 0:
            self.name_entry_buffer = self.name_entry_buffer[:-1]

    def confirm_name_entry(self):
        name = (self.name_entry_buffer.strip() or "PLAYER")[:8]
        self.high_score_mgr.add_score(name, self.player.score)
        self.mode = GameMode.HALL_OF_FAME
        if self.config.get("music_enabled", True):
            sounds.start_music("highscore", volume=self.config.get("music_volume", 0.35))

    def load_stage(self, stage_num: int):
        """Bou en stel Vlak 1, 2 of 3 op."""
        self.current_stage = stage_num
        self.obstacles.clear()
        self.enemies.clear()
        self.bullets.clear()
        self.grenades.clear()
        self.explosions.clear()
        self.trucks.clear()
        self.hostages.clear()
        self.supply_crates.clear()

        self.camera_y = float(self.world_height - self.height)
        self.player.x = self.width / 2.0
        self.player.y = self.world_height - 50.0
        self.gate_open = False
        self.gate_guards_cleared = False
        self.level_completed = False

        if stage_num == 1:
            self.stage_banner_text = "AREA 1: THE OUTPOST"
            # Bome langs die flanke
            for y in range(140, self.world_height - 80, 110):
                self.obstacles.append(Obstacle(36, y, ObstacleType.TREE, width=24, height=24))
                self.obstacles.append(Obstacle(self.width - 36, y + 45, ObstacleType.TREE, width=24, height=24))

            # Encampment 1 & Hurkende vyand
            self.obstacles.append(Obstacle(110, 1000, ObstacleType.SANDBAGS, width=34, height=14))
            self.obstacles.append(Obstacle(210, 1000, ObstacleType.SANDBAGS, width=34, height=14))
            self.enemies.append(Enemy(210, 995, kind=EnemyType.CROUCHING_GUNNER))
            self.obstacles.append(Obstacle(160, 950, ObstacleType.TRENCH, width=50, height=16))

            # Granaatkrat by Encampment 1
            self.supply_crates.append(SupplyCrate(210, 850))

            # Encampment 2
            self.obstacles.append(Obstacle(85, 750, ObstacleType.BARRICADE, width=38, height=14))
            self.obstacles.append(Obstacle(160, 710, ObstacleType.SANDBAGS, width=42, height=12))
            self.enemies.append(Enemy(160, 705, kind=EnemyType.CROUCHING_GUNNER))
            self.obstacles.append(Obstacle(235, 750, ObstacleType.BARRICADE, width=38, height=14))

            # Gyselaar met wag by y=600
            pow_guard = Enemy(130, 600, kind=EnemyType.SOLDIER)
            self.enemies.append(pow_guard)
            self.hostages.append(Hostage(115, 600, guard=pow_guard))

            # Encampment 3
            self.obstacles.append(Obstacle(115, 430, ObstacleType.SANDBAGS, width=36, height=12))
            self.obstacles.append(Obstacle(205, 430, ObstacleType.SANDBAGS, width=36, height=12))
            self.obstacles.append(Obstacle(160, 370, ObstacleType.TRENCH, width=64, height=16))

            # Vlak 1 Vestinghek
            self.obstacles.append(Obstacle(80, 70, ObstacleType.FORTRESS_WALL, width=120, height=20))
            self.obstacles.append(Obstacle(240, 70, ObstacleType.FORTRESS_WALL, width=120, height=20))
            self.gate_obstacle = Obstacle(160, 70, ObstacleType.FORTRESS_GATE, width=40, height=20)
            self.obstacles.append(self.gate_obstacle)

            # Hekwagte
            self.enemies.append(Enemy(140, 100, kind=EnemyType.GATE_GUARD))
            self.enemies.append(Enemy(180, 100, kind=EnemyType.GATE_GUARD))

            # Vragmotor wat troepe bring op y=800
            self.trucks.append(Truck(160, 800))

        elif stage_num == 2:
            # VLAK 2: DIE RIVIER EN HANGBRUG
            self.stage_banner_text = "AREA 2: RIVER CROSSING"
            # RIVIER sny dwarsdeur die slagveld by y=650
            self.obstacles.append(Obstacle(self.width / 2.0, 650, ObstacleType.RIVER, width=self.width, height=44))
            # HOUT HANGBRUG in die middel
            self.obstacles.append(Obstacle(160, 650, ObstacleType.BRIDGE, width=44, height=52))

            # Brugwagte aan die oorkant
            self.obstacles.append(Obstacle(125, 615, ObstacleType.SANDBAGS, width=30, height=12))
            self.obstacles.append(Obstacle(195, 615, ObstacleType.SANDBAGS, width=30, height=12))
            self.enemies.append(Enemy(125, 610, kind=EnemyType.CROUCHING_GUNNER))
            self.enemies.append(Enemy(195, 610, kind=EnemyType.CROUCHING_GUNNER))

            # Gyselaar voor die rivier
            g2 = Enemy(200, 850, kind=EnemyType.SOLDIER)
            self.enemies.append(g2)
            self.hostages.append(Hostage(218, 850, guard=g2))

            # Gyselaar en voorrade na die rivier
            self.hostages.append(Hostage(160, 480))
            self.supply_crates.append(SupplyCrate(110, 520))
            self.supply_crates.append(SupplyCrate(220, 300))

            # Bome en loopgrawe in Vlak 2
            for y in range(200, 1050, 140):
                self.obstacles.append(Obstacle(36, y, ObstacleType.TREE, width=24, height=24))
                self.obstacles.append(Obstacle(self.width - 36, y + 40, ObstacleType.TREE, width=24, height=24))

            # Vlak 2 Boonste Vestinghek by y=70
            self.obstacles.append(Obstacle(80, 70, ObstacleType.FORTRESS_WALL, width=120, height=20))
            self.obstacles.append(Obstacle(240, 70, ObstacleType.FORTRESS_WALL, width=120, height=20))
            self.gate_obstacle = Obstacle(160, 70, ObstacleType.FORTRESS_GATE, width=40, height=20)
            self.obstacles.append(self.gate_obstacle)

            self.enemies.append(Enemy(130, 95, kind=EnemyType.GATE_GUARD))
            self.enemies.append(Enemy(190, 95, kind=EnemyType.GATE_GUARD))
            self.trucks.append(Truck(160, 400))

        elif stage_num == 3:
            # VLAK 3: WOESTYN-VESTING EN FINALE HOOFKWARTIER
            self.stage_banner_text = "AREA 3: DESERT FORTRESS"
            # Versperrings langs die sye
            for y in range(120, self.world_height - 60, 95):
                self.obstacles.append(Obstacle(36, y, ObstacleType.BARRICADE, width=28, height=18))
                self.obstacles.append(Obstacle(self.width - 36, y + 45, ObstacleType.BARRICADE, width=28, height=18))

            # Versterkte loopgrawe en bunkers
            self.obstacles.append(Obstacle(160, 1020, ObstacleType.TRENCH, width=80, height=20))
            self.obstacles.append(Obstacle(110, 960, ObstacleType.SANDBAGS, width=40, height=14))
            self.obstacles.append(Obstacle(210, 960, ObstacleType.SANDBAGS, width=40, height=14))
            self.enemies.append(Enemy(110, 955, kind=EnemyType.CROUCHING_GUNNER))
            self.enemies.append(Enemy(210, 955, kind=EnemyType.CROUCHING_GUNNER))

            # Gyselaar met wagte by y=850
            g_stage3_1 = Enemy(140, 850, kind=EnemyType.SOLDIER)
            g_stage3_2 = Enemy(180, 850, kind=EnemyType.OFFICER_RUNNER)
            self.enemies.extend([g_stage3_1, g_stage3_2])
            self.hostages.append(Hostage(160, 850, guard=g_stage3_1))

            # Granaatkrat by y=780
            self.supply_crates.append(SupplyCrate(160, 780))

            # Spervuur loopgraaf by y=620
            self.obstacles.append(Obstacle(100, 620, ObstacleType.TRENCH, width=54, height=16))
            self.obstacles.append(Obstacle(220, 620, ObstacleType.TRENCH, width=54, height=16))
            self.obstacles.append(Obstacle(160, 580, ObstacleType.SANDBAGS, width=50, height=14))
            self.enemies.append(Enemy(160, 575, kind=EnemyType.CROUCHING_GUNNER))

            # Tweede gyselaar en voorraadkrat by y=480
            g_stage3_3 = Enemy(190, 480, kind=EnemyType.OFFICER_RUNNER)
            self.enemies.append(g_stage3_3)
            self.hostages.append(Hostage(210, 480, guard=g_stage3_3))
            self.supply_crates.append(SupplyCrate(110, 480))

            # Swaar vragmotor by y=500
            self.trucks.append(Truck(160, 500))

            # Finale Vestinghek 3 (Vyandelike Hoofkwartier) by y=70
            self.obstacles.append(Obstacle(80, 70, ObstacleType.FORTRESS_WALL, width=120, height=20))
            self.obstacles.append(Obstacle(240, 70, ObstacleType.FORTRESS_WALL, width=120, height=20))
            self.gate_obstacle = Obstacle(160, 70, ObstacleType.FORTRESS_GATE, width=40, height=20)
            self.obstacles.append(self.gate_obstacle)

            # 4 Elite Vestingwagte
            self.enemies.append(Enemy(120, 95, kind=EnemyType.GATE_GUARD))
            self.enemies.append(Enemy(150, 95, kind=EnemyType.GATE_GUARD))
            self.enemies.append(Enemy(170, 95, kind=EnemyType.GATE_GUARD))
            self.enemies.append(Enemy(200, 95, kind=EnemyType.GATE_GUARD))

    def update(self):
        self.ticks += 1

        if self.mode == GameMode.TITLE:
            self.update_title()
            return

        if self.mode == GameMode.DEMO:
            self.demo_ai.update(self)
            self.demo_timer -= 1
            if self.demo_timer <= 0 or not self.player.is_alive or self.level_completed:
                self.mode = GameMode.TITLE
                self.demo_timer = 400
                return

        if self.mode in (GameMode.NAME_ENTRY, GameMode.HALL_OF_FAME):
            return

        self.player.update(self)

        # Kamera volg speler
        scroll_threshold = self.camera_y + self.height * 0.55
        if self.player.y < scroll_threshold and self.camera_y > 0:
            target_cam = self.player.y - self.height * 0.55
            self.camera_y = max(0.0, target_cam)

        # Hekwagte kontrole
        guards_alive = [e for e in self.enemies if e.is_alive and e.kind == EnemyType.GATE_GUARD]
        if not guards_alive and not self.gate_guards_cleared:
            self.gate_guards_cleared = True
            self.gate_open = True
            self.gate_obstacle.is_alive = False
            self.player.score += 5000

        # Speler loop deur hek -> oorgang
        if self.gate_open and self.player.y < 70 and not self.level_completed:
            self.level_completed = True
            if self.current_stage == 1:
                self.player.score += 10000
                self.load_stage(2)
                return
            elif self.current_stage == 2:
                self.player.score += 15000
                self.load_stage(3)
                return
            elif self.current_stage == 3:
                self.player.score += 25000
                self.game_won = True
                sounds.play("victory", volume=0.7)
                if self.mode == GameMode.PLAYING:
                    if self.high_score_mgr.is_high_score(self.player.score):
                        self.mode = GameMode.NAME_ENTRY
                        self.name_entry_buffer = ""
                    else:
                        self.mode = GameMode.HALL_OF_FAME
                        if self.config.get("music_enabled", True):
                            sounds.start_music("highscore", volume=self.config.get("music_volume", 0.35))
                return

        # Spawneer gereelde vyande en stormloop offisiere
        self.spawn_timer += 1
        if self.spawn_timer >= 45 and not self.level_completed:
            self.spawn_timer = 0
            if len(self.enemies) < 9 and self.camera_y > 100:
                spawn_x = 40.0 + ((self.ticks * 53) % int(self.max_x - 80))
                spawn_y = self.camera_y - 15
                # 30% kans vir 'n vinnige offisier
                kind = EnemyType.OFFICER_RUNNER if (self.ticks % 3 == 0) else EnemyType.SOLDIER
                self.enemies.append(Enemy(spawn_x, spawn_y, kind=kind))

        # Opdateer vragmotors
        for t in self.trucks:
            t.update(self)
        self.trucks = [t for t in self.trucks if t.is_alive]

        # Opdateer gyselaars (POWs)
        for h in self.hostages:
            h.update(self)
        self.hostages = [h for h in self.hostages if h.is_alive]

        # Opdateer voorraadkratte
        for c in self.supply_crates:
            c.update(self)
        self.supply_crates = [c for c in self.supply_crates if c.is_alive]

        for bullet in self.bullets:
            bullet.update(self)
        self.bullets = [b for b in self.bullets if b.is_alive]

        for grenade in self.grenades:
            grenade.update(self)
        self.grenades = [g for g in self.grenades if g.is_alive]

        for exp in self.explosions:
            exp.update()
        self.explosions = [e for e in self.explosions if e.is_alive]

        for enemy in self.enemies:
            enemy.update(self)
        self.enemies = [e for e in self.enemies if e.is_alive]

        # Botsings: Speler-koeëls teen gyselaars (friendly fire)
        for bullet in self.bullets:
            if not bullet.is_player or not bullet.is_alive:
                continue
            for hostage in self.hostages:
                if not hostage.is_alive:
                    continue
                if abs(bullet.x - hostage.x) < 8 and abs(bullet.y - hostage.y) < 10:
                    bullet.is_alive = False
                    hostage.is_alive = False
                    sounds.play("enemy_hit", volume=0.45)

        # Botsings: Speler-koeëls teen vyande (hurkende vyande is beskerm!)
        for bullet in self.bullets:
            if not bullet.is_player or not bullet.is_alive:
                continue
            for enemy in self.enemies:
                if not enemy.is_alive:
                    continue
                # Hurkende vyand kan NIE raakgeskiet word nie
                if enemy.is_crouching:
                    continue
                if abs(bullet.x - enemy.x) < 8 and abs(bullet.y - enemy.y) < 10:
                    bullet.is_alive = False
                    enemy.is_alive = False
                    self.player.score += 150
                    sounds.play("enemy_hit", volume=0.45)

        for bullet in self.bullets:
            if bullet.is_player or not bullet.is_alive:
                continue
            if abs(bullet.x - self.player.x) < 6 and abs(bullet.y - self.player.y) < 8:
                bullet.is_alive = False
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.player.is_alive = False
                    if self.mode == GameMode.PLAYING:
                        if self.high_score_mgr.is_high_score(self.player.score):
                            self.mode = GameMode.NAME_ENTRY
                            self.name_entry_buffer = ""
                        else:
                            self.mode = GameMode.HALL_OF_FAME
                            if self.config.get("music_enabled", True):
                                sounds.start_music("highscore", volume=self.config.get("music_volume", 0.35))
                else:
                    self.player.y += 30


# ==============================================================================
# 5. RETRO C64 GRAFIESE RENDERING
# ==============================================================================

def draw_c64_super_joe(canvas, sx: int, sy: int, direction: Direction, frame: int, s: int):
    # Kopband (Rooi)
    canvas.create_rectangle(sx - 3*s, sy - 8*s, sx + 3*s, sy - 6*s, fill=C64_PALETTE[2], outline=C64_PALETTE[0])
    # Gesig
    canvas.create_rectangle(sx - 3*s, sy - 6*s, sx + 3*s, sy - 4*s, fill=C64_PALETTE[7], outline=C64_PALETTE[0])
    # Oë
    canvas.create_oval(sx - 2*s, sy - 6*s, sx - 1*s, sy - 5*s, fill=C64_PALETTE[0], outline="")
    canvas.create_oval(sx + 1*s, sy - 6*s, sx + 2*s, sy - 5*s, fill=C64_PALETTE[0], outline="")
    # Uniform
    canvas.create_rectangle(sx - 4*s, sy - 4*s, sx + 4*s, sy + 3*s, fill=C64_PALETTE[5], outline=C64_PALETTE[0])
    canvas.create_line(sx - 3*s, sy - 3*s, sx + 3*s, sy + 2*s, fill=C64_PALETTE[15], width=s)
    canvas.create_rectangle(sx - 4*s, sy + 3*s, sx + 4*s, sy + 5*s, fill=C64_PALETTE[0], outline="")
    # Bene
    leg_off = (frame % 2) * 2 - 1
    canvas.create_rectangle(sx - 4*s, sy + 5*s, sx - 1*s, sy + (9 + leg_off)*s, fill=C64_PALETTE[5], outline=C64_PALETTE[0])
    canvas.create_rectangle(sx + 1*s, sy + 5*s, sx + 4*s, sy + (9 - leg_off)*s, fill=C64_PALETTE[5], outline=C64_PALETTE[0])
    # Stewels
    canvas.create_rectangle(sx - 4*s, sy + (8 + leg_off)*s, sx - 1*s, sy + (10 + leg_off)*s, fill=C64_PALETTE[9], outline=C64_PALETTE[0])
    canvas.create_rectangle(sx + 1*s, sy + (8 - leg_off)*s, sx + 4*s, sy + (10 - leg_off)*s, fill=C64_PALETTE[9], outline=C64_PALETTE[0])
    # Geweer
    dx, dy = DIRECTION_VECTORS[direction]
    gx = sx + int(dx * 10 * s)
    gy = sy + int(dy * 10 * s)
    canvas.create_line(sx, sy - s, gx, gy, fill=C64_PALETTE[11], width=3*s)
    canvas.create_line(sx, sy - s, gx, gy, fill=C64_PALETTE[15], width=s)


def draw_c64_enemy(canvas, enemy: Enemy, cam_y: float, s: int):
    sx = int(enemy.x * s)
    sy = int((enemy.y - cam_y) * s)
    frame = enemy.anim_frame

    if enemy.kind == EnemyType.CROUCHING_GUNNER and enemy.is_crouching:
        # Hurkende vyand — slegs kop en helm loer uit
        canvas.create_oval(sx - 3*s, sy - 4*s, sx + 3*s, sy + 2*s, fill=C64_PALETTE[6], outline=C64_PALETTE[0], width=2)
        canvas.create_rectangle(sx - 2*s, sy - 2*s, sx + 2*s, sy, fill=C64_PALETTE[7], outline="")
        return

    # Helm (Rooi vir offisier, blou vir soldaat)
    helmet_col = C64_PALETTE[2] if enemy.kind == EnemyType.OFFICER_RUNNER else C64_PALETTE[6]
    canvas.create_rectangle(sx - 3*s, sy - 8*s, sx + 3*s, sy - 5*s, fill=helmet_col, outline=C64_PALETTE[0])
    # Gesig
    canvas.create_rectangle(sx - 2*s, sy - 5*s, sx + 2*s, sy - 3*s, fill=C64_PALETTE[7], outline=C64_PALETTE[0])
    # Uniform
    canvas.create_rectangle(sx - 3*s, sy - 3*s, sx + 3*s, sy + 3*s, fill=C64_PALETTE[6], outline=C64_PALETTE[0])
    # Bene
    leg_off = (frame % 2) * 2 - 1
    canvas.create_rectangle(sx - 3*s, sy + 3*s, sx - 1*s, sy + (8 + leg_off)*s, fill=C64_PALETTE[11], outline=C64_PALETTE[0])
    canvas.create_rectangle(sx + 1*s, sy + 3*s, sx + 3*s, sy + (8 - leg_off)*s, fill=C64_PALETTE[11], outline=C64_PALETTE[0])
    # Geweer of mes
    weapon_col = C64_PALETTE[15] if enemy.kind == EnemyType.OFFICER_RUNNER else C64_PALETTE[0]
    canvas.create_line(sx, sy - s, sx, sy + 8*s, fill=weapon_col, width=2*s)


def draw_truck(canvas, truck: Truck, cam_y: float, s: int):
    sx = int(truck.x * s)
    sy = int((truck.y - cam_y) * s)
    # Vragmotor bakwerk (Olyfgroen / Kamoeflering)
    canvas.create_rectangle(sx - 16*s, sy - 22*s, sx + 16*s, sy + 18*s, fill="#4A5828", outline=C64_PALETTE[0], width=2)
    # Kajuit
    canvas.create_rectangle(sx - 14*s, sy + 6*s, sx + 14*s, sy + 20*s, fill="#3A4818", outline=C64_PALETTE[0], width=2)
    # Voorruit
    canvas.create_rectangle(sx - 11*s, sy + 10*s, sx + 11*s, sy + 16*s, fill=C64_PALETTE[3], outline=C64_PALETTE[0])
    # Seilkap / Canvas dak
    canvas.create_rectangle(sx - 14*s, sy - 20*s, sx + 14*s, sy + 4*s, fill="#706040", outline=C64_PALETTE[0])
    # Wiele
    canvas.create_rectangle(sx - 18*s, sy - 14*s, sx - 15*s, sy - 6*s, fill=C64_PALETTE[0])
    canvas.create_rectangle(sx + 15*s, sy - 14*s, sx + 18*s, sy - 6*s, fill=C64_PALETTE[0])
    canvas.create_rectangle(sx - 18*s, sy + 6*s, sx - 15*s, sy + 14*s, fill=C64_PALETTE[0])
    canvas.create_rectangle(sx + 15*s, sy + 6*s, sx + 18*s, sy + 14*s, fill=C64_PALETTE[0])


def draw_obstacle(canvas, obs: Obstacle, cam_y: float, s: int):
    sx = int(obs.x * s)
    sy = int((obs.y - cam_y) * s)
    hw = int((obs.width / 2.0) * s)
    hh = int((obs.height / 2.0) * s)

    if obs.kind == ObstacleType.SANDBAGS:
        canvas.create_rectangle(sx - hw, sy - hh, sx + hw, sy + hh, fill="#D89848", outline=C64_PALETTE[0], width=2)
        canvas.create_line(sx - hw, sy, sx + hw, sy, fill=C64_PALETTE[9])
    elif obs.kind == ObstacleType.TREE:
        # Stam
        canvas.create_line(sx, sy + 12*s, sx, sy, fill=C64_PALETTE[9], width=3*s)
        for angle in (-50, -25, 0, 25, 50):
            rad = math.radians(angle - 90)
            bx = sx + math.cos(rad) * 14 * s
            by = sy + math.sin(rad) * 14 * s
            canvas.create_line(sx, sy, bx, by, fill=C64_PALETTE[5], width=2*s)
    elif obs.kind == ObstacleType.TRENCH:
        canvas.create_rectangle(sx - hw, sy - hh, sx + hw, sy + hh, fill="#382008", outline=C64_PALETTE[9], width=2)
    elif obs.kind == ObstacleType.BARRICADE:
        canvas.create_rectangle(sx - hw, sy - hh, sx + hw, sy + hh, fill=C64_PALETTE[12], outline=C64_PALETTE[11], width=2)
    elif obs.kind == ObstacleType.FORTRESS_WALL:
        canvas.create_rectangle(sx - hw, sy - hh, sx + hw, sy + hh, fill="#707070", outline=C64_PALETTE[0], width=3)
        for i in range(-hw, hw, 14*s):
            canvas.create_line(sx + i, sy - hh, sx + i, sy + hh, fill="#505050")
    elif obs.kind == ObstacleType.FORTRESS_GATE:
        canvas.create_rectangle(sx - hw, sy - hh, sx + hw, sy + hh, fill="#403020", outline=C64_PALETTE[0], width=2)
        for i in range(-hw + 3*s, hw, 6*s):
            canvas.create_line(sx + i, sy - hh, sx + i, sy + hh, fill=C64_PALETTE[15], width=2)
    elif obs.kind == ObstacleType.RIVER:
        # Vloeiende Blou Rivier
        canvas.create_rectangle(sx - hw, sy - hh, sx + hw, sy + hh, fill=C64_PALETTE[14], outline=C64_PALETTE[6], width=3)
        # Golfies
        for rx in range(sx - hw, sx + hw, 24*s):
            canvas.create_line(rx, sy - 4*s, rx + 12*s, sy - 4*s, fill=C64_PALETTE[3], width=s)
            canvas.create_line(rx + 6*s, sy + 6*s, rx + 18*s, sy + 6*s, fill=C64_PALETTE[3], width=s)
    elif obs.kind == ObstacleType.BRIDGE:
        # Hout Hangbrug oor die rivier
        canvas.create_rectangle(sx - hw, sy - hh, sx + hw, sy + hh, fill=C64_PALETTE[9], outline=C64_PALETTE[0], width=2)
        # Houtplanke
        for by in range(sy - hh, sy + hh, 6*s):
            canvas.create_line(sx - hw, by, sx + hw, by, fill="#885520", width=1)
        # Tousye
        canvas.create_line(sx - hw, sy - hh, sx - hw, sy + hh, fill="#AA8844", width=3)
        canvas.create_line(sx + hw, sy - hh, sx + hw, sy + hh, fill="#AA8844", width=3)


def draw_c64_hostage(canvas, hostage: Hostage, cam_y: float, s: int):
    sx = int(hostage.x * s)
    sy = int((hostage.y - cam_y) * s)
    frame = hostage.anim_frame

    # Gesig en hare (Bruin hare, velkleur gesig)
    canvas.create_rectangle(sx - 2*s, sy - 8*s, sx + 2*s, sy - 6*s, fill=C64_PALETTE[9], outline=C64_PALETTE[0])
    canvas.create_rectangle(sx - 2*s, sy - 6*s, sx + 2*s, sy - 3*s, fill=C64_PALETTE[7], outline=C64_PALETTE[0])

    if not hostage.is_rescued:
        # Gyselaar vasgebind: Hemp is wit, bene vasgemaak
        canvas.create_rectangle(sx - 3*s, sy - 3*s, sx + 3*s, sy + 3*s, fill=C64_PALETTE[1], outline=C64_PALETTE[0])
        # Tou om die lyf
        canvas.create_line(sx - 3*s, sy - s, sx + 3*s, sy - s, fill="#AA8844", width=2*s)
        canvas.create_line(sx - 3*s, sy + s, sx + 3*s, sy + s, fill="#AA8844", width=2*s)
        # Bene
        canvas.create_rectangle(sx - 2*s, sy + 3*s, sx + 2*s, sy + 8*s, fill=C64_PALETTE[11], outline=C64_PALETTE[0])
        # Houtpaal agter hom
        canvas.create_line(sx, sy - 11*s, sx, sy + 10*s, fill="#553311", width=2*s)
    else:
        # Bevryde soldaat: hande in die lug, hardloop vorentoe!
        canvas.create_rectangle(sx - 3*s, sy - 3*s, sx + 3*s, sy + 3*s, fill=C64_PALETTE[13], outline=C64_PALETTE[0])
        # Arms in die lug (jubelend)
        canvas.create_line(sx - 3*s, sy - 2*s, sx - 6*s, sy - 8*s, fill=C64_PALETTE[7], width=2*s)
        canvas.create_line(sx + 3*s, sy - 2*s, sx + 6*s, sy - 8*s, fill=C64_PALETTE[7], width=2*s)
        # Hardloop bene
        leg_off = (frame % 2) * 2 - 1
        canvas.create_rectangle(sx - 3*s, sy + 3*s, sx - 1*s, sy + (8 + leg_off)*s, fill=C64_PALETTE[11], outline=C64_PALETTE[0])
        canvas.create_rectangle(sx + 1*s, sy + 3*s, sx + 3*s, sy + (8 - leg_off)*s, fill=C64_PALETTE[11], outline=C64_PALETTE[0])
        # Kennisgewing "THANKS!"
        canvas.create_text(sx, sy - 13*s, text="THANKS!", fill=C64_PALETTE[7], font=("Courier", max(8, 3*s), "bold"))


LOGO_LETTERS = {
    'C': [
        " ####",
        "#    ",
        "#    ",
        "#    ",
        " ####",
    ],
    'O': [
        " ### ",
        "#   #",
        "#   #",
        "#   #",
        " ### ",
    ],
    'M': [
        "#   #",
        "## ##",
        "# # #",
        "#   #",
        "#   #",
    ],
    'A': [
        " ### ",
        "#   #",
        "#####",
        "#   #",
        "#   #",
    ],
    'N': [
        "#   #",
        "##  #",
        "# # #",
        "#  ##",
        "#   #",
    ],
    'D': [
        "#### ",
        "#   #",
        "#   #",
        "#   #",
        "#### ",
    ],
}

def draw_c64_commando_logo(canvas, cx: int, cy: int, s: int):
    """Teken die reuse C64 COMMANDO militêre stensil-logo met 3D reliëf."""
    word = "COMMANDO"
    block_s = max(2, int(3.2 * s))
    letter_w = 6 * block_s
    total_w = len(word) * letter_w
    start_x = cx - total_w // 2

    for l_idx, ch in enumerate(word):
        grid = LOGO_LETTERS.get(ch, LOGO_LETTERS['O'])
        lx = start_x + l_idx * letter_w
        for row_idx, row in enumerate(grid):
            for col_idx, pixel in enumerate(row):
                if pixel == '#':
                    bx = lx + col_idx * block_s
                    by = cy + row_idx * block_s
                    # 1. Donker 3D skaduwee
                    canvas.create_rectangle(bx + 2*s, by + 2*s, bx + block_s + 2*s, by + block_s + 2*s, fill="#3A1000", outline="")
                    # 2. Hoofliggaam (Rooi-oranje)
                    canvas.create_rectangle(bx, by, bx + block_s, by + block_s, fill=C64_PALETTE[2], outline="")
                    # 3. Geel randjie en glans
                    canvas.create_line(bx, by, bx + block_s - 1, by, fill=C64_PALETTE[7], width=1)
                    canvas.create_line(bx, by, bx, by + block_s - 1, fill=C64_PALETTE[7], width=1)
                    # 4. Oranje middel
                    canvas.create_rectangle(bx + s, by + s, bx + block_s - s, by + block_s - s, fill=C64_PALETTE[8], outline="")


def draw_c64_title_screen(canvas, game: GameState, width: int, height: int, s: int, intro_img=None):
    cx = (width * s) // 2
    cy = (height * s) // 2

    if intro_img is not None:
        canvas.create_image(0, 0, anchor="nw", image=intro_img)
        # Donker C64-balkie onderaan vir leesbare spelerprompts
        bar_y1 = (height - 40) * s
        bar_y2 = (height - 6) * s
        canvas.create_rectangle(18 * s, bar_y1, (width - 18) * s, bar_y2, fill=C64_PALETTE[0], outline=C64_PALETTE[14], width=2)

        # Knipperende 'PRESS SPACE TO PLAY'
        if (game.ticks // 25) % 2 == 0:
            canvas.create_text(cx, bar_y1 + 12 * s, text="*** PRESS SPACE OR ENTER TO PLAY ***", fill=C64_PALETTE[1], font=("Courier", 13, "bold"))
        else:
            canvas.create_text(cx, bar_y1 + 12 * s, text="[ COMMODORE 64 COMMANDO - CAPCOM / ELITE 1985 ]", fill=C64_PALETTE[7], font=("Courier", 11, "bold"))

        demo_sec = max(0, game.demo_timer // 50 + 1)
        canvas.create_text(cx, bar_y1 + 25 * s, text=f"[ ATTRACT DEMO IN: {demo_sec}s | C: SCANLINES | H: HALL OF FAME ]", fill=C64_PALETTE[3], font=("Courier", 9, "bold"))
    else:
        canvas.create_rectangle(0, 0, width * s, height * s, fill=C64_PALETTE[6], outline="")
        canvas.create_rectangle(12 * s, 10 * s, (width - 12) * s, (height - 10) * s, fill=C64_PALETTE[0], outline=C64_PALETTE[14], width=3)

        # COMMANDO Logo
        draw_c64_commando_logo(canvas, cx, 30 * s, s)

        # Sub-titels en lisensie
        canvas.create_text(cx, 85 * s, text="TM & (C) 1985 CAPCOM CO. LTD", fill=C64_PALETTE[3], font=("Courier", 11, "bold"))
        canvas.create_text(cx, 97 * s, text="LICENSED TO ELITE SYSTEMS LTD", fill=C64_PALETTE[3], font=("Courier", 10, "bold"))

        # Krediete
        canvas.create_text(cx, 116 * s, text="PROGRAMMED BY CHRIS BUTLER", fill=C64_PALETTE[1], font=("Courier", 10, "bold"))
        canvas.create_text(cx, 127 * s, text="GRAPHICS BY RORY GREEN & CHRIS HARVEY", fill=C64_PALETTE[13], font=("Courier", 10, "bold"))
        canvas.create_text(cx, 138 * s, text="MUSIC & SOUND BY ROB HUBBARD", fill=C64_PALETTE[7], font=("Courier", 10, "bold"))

        # Knipperende 'PRESS SPACE TO PLAY'
        if (game.ticks // 25) % 2 == 0:
            canvas.create_text(cx, 160 * s, text="*** PRESS SPACE OR ENTER TO PLAY ***", fill=C64_PALETTE[1], font=("Courier", 13, "bold"))

        # Aftelling na Demo
        demo_sec = max(0, game.demo_timer // 50 + 1)
        canvas.create_text(cx, 175 * s, text=f"[ ATTRACT DEMO IN: {demo_sec}s ]", fill=C64_PALETTE[14], font=("Courier", 9, "bold"))
        canvas.create_text(cx, 186 * s, text="[ C: CRT SCANLINES | H: HALL OF FAME | M: MUSIC ]", fill=C64_PALETTE[15], font=("Courier", 8, "bold"))


def draw_c64_name_entry(canvas, game: GameState, width: int, height: int, s: int):
    cx = (width * s) // 2
    cy = (height * s) // 2
    box_w = 125 * s
    box_h = 75 * s

    canvas.create_rectangle(cx - box_w, cy - box_h, cx + box_w, cy + box_h, fill=C64_PALETTE[6], outline=C64_PALETTE[7], width=4)
    canvas.create_rectangle(cx - box_w + 4, cy - box_h + 4, cx + box_w - 4, cy + box_h - 4, fill=C64_PALETTE[0], outline="")

    canvas.create_text(cx, cy - box_h + 16*s, text="GREAT HEROIC EFFORT, COMMANDO!", fill=C64_PALETTE[7], font=("Courier", 13, "bold"))
    canvas.create_text(cx, cy - box_h + 28*s, text=f"FINAL SCORE: {game.player.score:06d}", fill=C64_PALETTE[1], font=("Courier", 12, "bold"))
    canvas.create_text(cx, cy - box_h + 40*s, text="ENTER YOUR NAME:", fill=C64_PALETTE[3], font=("Courier", 11, "bold"))

    cursor = "_" if (game.ticks // 15) % 2 == 0 else " "
    display_name = f">  {game.name_entry_buffer}{cursor}  <"
    canvas.create_text(cx, cy - box_h + 54*s, text=display_name, fill=C64_PALETTE[1], font=("Courier", 16, "bold"))

    canvas.create_text(cx, cy + box_h - 10*s, text="[ TYPE LETTERS | BACKSPACE | ENTER TO SAVE ]", fill=C64_PALETTE[14], font=("Courier", 9, "bold"))


def draw_c64_scanlines(canvas, width: int, height: int, s: int):
    for y in range(0, height * s, 4):
        canvas.create_line(0, y, width * s, y, fill="#080808", width=1)


def draw_c64_supply_crate(canvas, crate: SupplyCrate, cam_y: float, s: int):
    sx = int(crate.x * s)
    sy = int((crate.y - cam_y) * s)
    canvas.create_rectangle(sx - 7*s, sy - 7*s, sx + 7*s, sy + 7*s, fill="#986020", outline=C64_PALETTE[0], width=2)
    canvas.create_line(sx - 7*s, sy - 7*s, sx + 7*s, sy + 7*s, fill="#704010", width=1)
    canvas.create_line(sx - 7*s, sy + 7*s, sx + 7*s, sy - 7*s, fill="#704010", width=1)
    canvas.create_text(sx, sy, text="G", fill=C64_PALETTE[1], font=("Courier", int(9*s), "bold"))


def draw_c64_hall_of_fame(canvas, high_score_mgr: HighScoreManager, width: int, height: int, s: int):
    cx = (width * s) // 2
    cy = (height * s) // 2
    box_w = 125 * s
    box_h = 82 * s

    canvas.create_rectangle(cx - box_w, cy - box_h, cx + box_w, cy + box_h, fill=C64_PALETTE[6], outline=C64_PALETTE[14], width=4)
    canvas.create_rectangle(cx - box_w + 4, cy - box_h + 4, cx + box_w - 4, cy + box_h - 4, fill=C64_PALETTE[0], outline="")

    canvas.create_text(cx, cy - box_h + 14*s, text="COMMODORE 64 HALL OF FAME", fill=C64_PALETTE[7], font=("Courier", 14, "bold"))
    canvas.create_text(cx, cy - box_h + 24*s, text="RANK   COMMANDO   SCORE", fill=C64_PALETTE[3], font=("Courier", 11, "bold"))

    scores = high_score_mgr.get_scores()
    for idx, item in enumerate(scores[:5]):
        y_pos = cy - box_h + (35 + idx * 8) * s
        line_text = f" {idx+1}     {item['name']:<8}  {int(item['score']):06d}"
        col = C64_PALETTE[1] if idx == 0 else C64_PALETTE[15]
        canvas.create_text(cx, y_pos, text=line_text, fill=col, font=("Courier", 11, "bold"))

    canvas.create_text(cx, cy + box_h - 8*s, text="[ PRESS 'R' OR SPACE FOR TITLE ]", fill=C64_PALETTE[14], font=("Courier", 10, "bold"))


# ==============================================================================
# 6. HOOFSPEL-LUS & VENSTER
# ==============================================================================

def run_commando():
    import tkinter as tk

    scale = 3
    width = 320
    height = 200

    root = tk.Tk()
    root.title("RETRORECON — Commando C64 (Volle Spesifikasie)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=width * scale, height=height * scale, bg="#986828", highlightthickness=0)
    canvas.pack()

    game = GameState(width=width, height=height, world_height=1250, start_mode=GameMode.TITLE)

    # Laai die amptelike Commando C64 intro-beeld indien beskikbaar
    intro_img = None
    intro_png_path = os.path.join(os.path.dirname(__file__), "intro.png")
    if not os.path.exists(intro_png_path):
        intro_jpg_path = os.path.join(os.path.dirname(__file__), "intro.jpg")
        if os.path.exists(intro_jpg_path):
            try:
                from PIL import Image
                img = Image.open(intro_jpg_path)
                resized = img.resize((width * scale, height * scale), Image.Resampling.LANCZOS)
                resized.save(intro_png_path)
            except Exception:
                pass

    if os.path.exists(intro_png_path):
        try:
            intro_img = tk.PhotoImage(file=intro_png_path)
        except Exception:
            intro_img = None

    # Begin outentieke Rob Hubbard SID musiek!
    if game.config.get("music_enabled", True):
        sounds.start_music("theme", volume=game.config.get("music_volume", 0.35))

    keys = {"Up": False, "Down": False, "Left": False, "Right": False, "space": False, "g": False}

    def on_key_press(event):
        sym = event.keysym.lower()

        # In naam-invoer modus
        if game.mode == GameMode.NAME_ENTRY:
            if sym in ("return", "enter"):
                game.confirm_name_entry()
            elif sym in ("backspace", "delete"):
                game.handle_backspace()
            elif len(event.char) == 1 and (event.char.isalnum() or event.char in " _-"):
                game.handle_text_input(event.char)
            return

        # Algemene sleutels
        if sym in ("space", "return", "enter"):
            if game.mode in (GameMode.TITLE, GameMode.DEMO):
                game.start_game()
                return
            elif game.mode == GameMode.HALL_OF_FAME:
                game.mode = GameMode.TITLE
                game.demo_timer = 400
                if game.config.get("music_enabled", True):
                    sounds.start_music("theme", volume=game.config.get("music_volume", 0.35))
                return

        if sym == "c":
            cur_scan = game.config.get("scanlines", True)
            game.config.set("scanlines", not cur_scan)
        elif sym == "m":
            cur_mus = game.config.get("music_enabled", True)
            game.config.set("music_enabled", not cur_mus)
            if not cur_mus:
                track = "highscore" if game.mode == GameMode.HALL_OF_FAME else "theme"
                sounds.start_music(track, volume=game.config.get("music_volume", 0.35))
            else:
                sounds.stop_music()
        elif sym == "h":
            if game.mode == GameMode.HALL_OF_FAME:
                game.mode = GameMode.TITLE
                game.demo_timer = 400
                if game.config.get("music_enabled", True):
                    sounds.start_music("theme", volume=game.config.get("music_volume", 0.35))
            else:
                game.mode = GameMode.HALL_OF_FAME
                if game.config.get("music_enabled", True):
                    sounds.start_music("highscore", volume=game.config.get("music_volume", 0.35))
        elif sym == "r":
            game.start_game()
        elif sym in ("q", "escape"):
            on_close()

        # Spel-beweging kontroles
        if sym in ("up", "w"): keys["Up"] = True
        elif sym in ("down", "s"): keys["Down"] = True
        elif sym in ("left", "a"): keys["Left"] = True
        elif sym in ("right", "d"): keys["Right"] = True
        elif sym == "space": keys["space"] = True
        elif sym in ("g", "x", "shift_l", "shift_r"): keys["g"] = True

    def on_key_release(event):
        sym = event.keysym.lower()
        if sym in ("up", "w"): keys["Up"] = False
        elif sym in ("down", "s"): keys["Down"] = False
        elif sym in ("left", "a"): keys["Left"] = False
        elif sym in ("right", "d"): keys["Right"] = False
        elif sym == "space": keys["space"] = False
        elif sym in ("g", "x", "shift_l", "shift_r"): keys["g"] = False

    def on_close():
        sounds.stop_music()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)

    def game_loop():
        # Opdateer toestand
        if game.mode == GameMode.PLAYING:
            game.player.set_input(
                up=keys["Up"],
                down=keys["Down"],
                left=keys["Left"],
                right=keys["Right"],
                fire=keys["space"],
                grenade=keys["g"],
            )

        game.update()

        canvas.delete("all")

        # 1. Titelskerm
        if game.mode == GameMode.TITLE:
            draw_c64_title_screen(canvas, game, width, height, scale, intro_img)
            if game.config.get("scanlines", True):
                draw_c64_scanlines(canvas, width, height, scale)
            root.after(20, game_loop)
            return

        # 2. Hall of Fame
        if game.mode == GameMode.HALL_OF_FAME:
            draw_c64_title_screen(canvas, game, width, height, scale, intro_img)
            draw_c64_hall_of_fame(canvas, game.high_score_mgr, width, height, scale)
            if game.config.get("scanlines", True):
                draw_c64_scanlines(canvas, width, height, scale)
            root.after(20, game_loop)
            return

        # 3. Speelveld (PLAYING of DEMO)
        cam_y = game.camera_y

        # Grondkleure: Vlak 3 Woestyn vs Vlak 1/2 Oerwoud
        if game.current_stage == 3:
            fill_flank = "#C29B38"
            fill_mid = "#D2AB48"
        else:
            fill_flank = "#A87830"
            fill_mid = "#B88838"

        canvas.create_rectangle(0, 0, width * scale, height * scale, fill=fill_flank, outline="")
        canvas.create_rectangle(36 * scale, 0, (width - 36) * scale, height * scale, fill=fill_mid, outline="")

        # Hindernisse & Rivier
        for obs in game.obstacles:
            if obs.is_alive and (cam_y - 60 <= obs.y <= cam_y + height + 60):
                draw_obstacle(canvas, obs, cam_y, scale)

        # Voorraadkratte
        for crate in game.supply_crates:
            if crate.is_alive and (cam_y - 30 <= crate.y <= cam_y + height + 30):
                draw_c64_supply_crate(canvas, crate, cam_y, scale)

        # Gyselaars (POWs)
        for hostage in game.hostages:
            if hostage.is_alive and (cam_y - 30 <= hostage.y <= cam_y + height + 30):
                draw_c64_hostage(canvas, hostage, cam_y, scale)

        # Vragmotors
        for t in game.trucks:
            if cam_y - 40 <= t.y <= cam_y + height + 40:
                draw_truck(canvas, t, cam_y, scale)

        # Vyande
        for enemy in game.enemies:
            if cam_y - 20 <= enemy.y <= cam_y + height + 20:
                draw_c64_enemy(canvas, enemy, cam_y, scale)

        # Koeëls
        for b in game.bullets:
            bx = int(b.x * scale)
            by = int((b.y - cam_y) * scale)
            col = C64_PALETTE[1] if b.is_player else C64_PALETTE[2]
            canvas.create_oval(bx - scale, by - scale, bx + scale, by + scale, fill=col, outline="")

        # Granate
        for g in game.grenades:
            gx = int(g.x * scale)
            gy = int((g.y - cam_y) * scale)
            shadow_y = gy
            air_y = gy - int(g.altitude * scale)
            canvas.create_oval(gx - 2*scale, shadow_y - scale, gx + 2*scale, shadow_y + scale, fill="#403010", outline="")
            canvas.create_oval(gx - 2*scale, air_y - 2*scale, gx + 2*scale, air_y + 2*scale, fill=C64_PALETTE[0], outline=C64_PALETTE[11])

        # Ontploffings
        for exp in game.explosions:
            ex = int(exp.x * scale)
            ey = int((exp.y - cam_y) * scale)
            r = int(exp.radius * scale * (1.0 - exp.timer / exp.max_timer * 0.4))
            canvas.create_oval(ex - r, ey - r, ex + r, ey + r, fill=C64_PALETTE[8], outline=C64_PALETTE[2], width=2*scale)
            r2 = r // 2
            canvas.create_oval(ex - r2, ey - r2, ex + r2, ey + r2, fill=C64_PALETTE[7], outline=C64_PALETTE[1])

        # Super Joe
        if game.player.is_alive:
            px = int(game.player.x * scale)
            py = int((game.player.y - cam_y) * scale)
            draw_c64_super_joe(canvas, px, py, game.player.direction, game.player.anim_frame, scale)

        # Boodskappe en Banier
        if game.mode == GameMode.DEMO:
            canvas.create_rectangle(20*scale, 26*scale, (width-20)*scale, 44*scale, fill=C64_PALETTE[0], outline=C64_PALETTE[2], width=2)
            canvas.create_text(width*scale//2, 35*scale, text="** ATTRACT DEMO - PRESS SPACE TO PLAY **", fill=C64_PALETTE[7], font=("Courier", 11, "bold"))
        elif game.game_won:
            canvas.create_rectangle(20*scale, 50*scale, (width-20)*scale, 150*scale, fill=C64_PALETTE[0], outline=C64_PALETTE[7], width=4)
            canvas.create_text(width*scale//2, 70*scale, text="MISSION ACCOMPLISHED!", fill=C64_PALETTE[7], font=("Courier", 18, "bold"))
            canvas.create_text(width*scale//2, 92*scale, text="SUPER JOE SAVED THE DAY!", fill=C64_PALETTE[1], font=("Courier", 13, "bold"))
            canvas.create_text(width*scale//2, 110*scale, text=f"FINAL SCORE: {game.player.score:06d}", fill=C64_PALETTE[14], font=("Courier", 14, "bold"))
            canvas.create_text(width*scale//2, 132*scale, text="[ PRESS 'H' FOR HALL OF FAME | 'R' RESTART ]", fill=C64_PALETTE[3], font=("Courier", 10, "bold"))
        elif not game.player.is_alive and game.mode == GameMode.PLAYING:
            canvas.create_rectangle(30*scale, 65*scale, (width-30)*scale, 135*scale, fill=C64_PALETTE[0], outline=C64_PALETTE[2], width=4)
            canvas.create_text(width*scale//2, 85*scale, text="GAME OVER", fill=C64_PALETTE[2], font=("Courier", 20, "bold"))
            canvas.create_text(width*scale//2, 107*scale, text=f"FINAL SCORE: {game.player.score:06d}", fill=C64_PALETTE[1], font=("Courier", 13, "bold"))
            canvas.create_text(width*scale//2, 123*scale, text="[ PRESS 'H' FOR HALL OF FAME | 'R' RESTART ]", fill=C64_PALETTE[7], font=("Courier", 10, "bold"))
        elif game.level_completed:
            canvas.create_rectangle(35*scale, 70*scale, (width-35)*scale, 130*scale, fill=C64_PALETTE[0], outline=C64_PALETTE[7], width=4)
            canvas.create_text(width*scale//2, 90*scale, text=f"AREA {game.current_stage} CLEARED!", fill=C64_PALETTE[7], font=("Courier", 18, "bold"))
            canvas.create_text(width*scale//2, 112*scale, text="BONUS: 10000 PTS", fill=C64_PALETTE[1], font=("Courier", 14, "bold"))
        elif game.gate_open:
            canvas.create_text(width*scale//2, 35*scale, text="GATE IS OPEN! ENTER FORTRESS!", fill=C64_PALETTE[7], font=("Courier", 12, "bold"))
        elif game.player.y < 350:
            canvas.create_text(width*scale//2, 35*scale, text="DEFEAT GATE GUARDS TO OPEN!", fill=C64_PALETTE[2], font=("Courier", 12, "bold"))

        # Naam-invoer oorleg
        if game.mode == GameMode.NAME_ENTRY:
            draw_c64_name_entry(canvas, game, width, height, scale)

        # HUD boaan
        canvas.create_rectangle(0, 0, width * scale, 22 * scale, fill=C64_PALETTE[0], outline="")
        hud_text = f"1UP {game.player.score:06d}  STAGE {game.current_stage}  GRENADES:{game.player.grenades}  LIVES:{game.player.lives}"
        canvas.create_text(width * scale // 2, 11 * scale, text=hud_text, fill=C64_PALETTE[1], font=("Courier", 14, "bold"))

        # 4. CRT Skandeerlyne oorleg
        if game.config.get("scanlines", True):
            draw_c64_scanlines(canvas, width, height, scale)

        root.after(20, game_loop)

    root.after(20, game_loop)
    root.mainloop()

if __name__ == "__main__":
    run_commando()
