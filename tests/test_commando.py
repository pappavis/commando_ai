"""
PROJEK RETRORECON — TOETSE VIR COMMANDO PYTHON-REKONSTRUKSIE
TDD Fase: RED -> GREEN -> REFACTOR
Dokumente: D00 v1.3 & D01 v1.1-RC
Inkrement 2: Rob Hubbard Musiek, Gevorderde Vyand-AI, Vragmotors en Vlak 2 (Hangbrug)
Ligging: ./tests/test_commando.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from commando import (
    Player, Direction, GameState, Bullet, Grenade, Obstacle, ObstacleType,
    Enemy, EnemyType, Truck, Hostage, SupplyCrate, HighScoreManager,
    GameMode, ConfigManager, DemoAI
)
from sound_effects import sounds, SoundManager

class TestCommandoInkrement2(unittest.TestCase):
    def setUp(self):
        sounds.enabled = False
        self.game = GameState(width=320, height=200, world_height=1200)
        self.player = self.game.player

    def test_player_initial_state(self):
        """Toets dat speler begin met geldige koördinate, rigting UP en lewendig."""
        self.assertEqual(self.player.direction, Direction.UP)
        self.assertTrue(self.player.is_alive)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.grenades, 6)

    def test_player_8_way_directions(self):
        """Toets dat Chris Butler se 8-rigting kodes (0..14) korrek gestel word."""
        self.player.set_input(up=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.UP)
        self.assertEqual(self.player.direction.value, 0)

        self.player.set_input(up=True, right=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.UP_RIGHT)
        self.assertEqual(self.player.direction.value, 2)

        self.player.set_input(right=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.RIGHT)
        self.assertEqual(self.player.direction.value, 4)

        self.player.set_input(down=True, right=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.DOWN_RIGHT)
        self.assertEqual(self.player.direction.value, 6)

        self.player.set_input(down=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.DOWN)
        self.assertEqual(self.player.direction.value, 8)

        self.player.set_input(down=True, left=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.DOWN_LEFT)
        self.assertEqual(self.player.direction.value, 10)

        self.player.set_input(left=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.LEFT)
        self.assertEqual(self.player.direction.value, 12)

        self.player.set_input(up=True, left=True)
        self.game.update()
        self.assertEqual(self.player.direction, Direction.UP_LEFT)
        self.assertEqual(self.player.direction.value, 14)

    def test_grenade_throw_and_area_damage(self):
        """Toets dat granaat gegooi word, teller afneem en ontplof."""
        self.assertEqual(self.player.grenades, 6)
        self.player.throw_grenade(self.game)
        self.assertEqual(self.player.grenades, 5)

        for _ in range(25):
            self.game.update()
        self.assertGreaterEqual(len(self.game.explosions), 1)

    def test_obstacle_blocks_bullets(self):
        """Toets dat sand-sakke koeëls blokkeer."""
        obs = Obstacle(x=self.player.x, y=self.player.y - 30, kind=ObstacleType.SANDBAGS)
        self.game.obstacles.append(obs)
        self.player.direction = Direction.UP
        self.player.fire_weapon(self.game)
        self.assertEqual(len(self.game.bullets), 1)
        for _ in range(10):
            self.game.update()
        self.assertEqual(len(self.game.bullets), 0)

    # --------------------------------------------------------------------------
    # NUWE TOETSE VIR INKREMENT 2 (OPSIE A, B, C)
    # --------------------------------------------------------------------------

    def test_crouching_enemy_mechanic(self):
        """Toets dat 'n hurkende vyand agter dekking nie deur koeëls getref word nie."""
        gunner = Enemy(x=160, y=900, kind=EnemyType.CROUCHING_GUNNER)
        gunner.is_crouching = True
        self.game.enemies.append(gunner)

        # Skiet reguit op die hurkende vyand
        bullet = Bullet(x=160, y=905, direction=Direction.UP, is_player=True)
        self.game.bullets.append(bullet)

        self.game.update()
        # Terwyl hy hurk, leef hy nog
        self.assertTrue(gunner.is_alive)

        # Wanneer hy opstaan, kan hy getref word
        gunner.is_crouching = False
        bullet2 = Bullet(x=160, y=905, direction=Direction.UP, is_player=True)
        self.game.bullets.append(bullet2)
        self.game.update()
        self.assertFalse(gunner.is_alive)

    def test_officer_runner_speed(self):
        """Toets dat 'n offisier vinniger hardloop as 'n gewone soldaat."""
        regular = Enemy(x=100, y=500, kind=EnemyType.SOLDIER)
        officer = Enemy(x=200, y=500, kind=EnemyType.OFFICER_RUNNER)
        self.assertGreater(officer.speed, regular.speed)

    def test_truck_troop_deployment(self):
        """Toets dat 'n militêre vragmotor troepe in die veld ontplooi."""
        truck = Truck(x=160, y=800)
        self.game.trucks.append(truck)
        initial_enemy_count = len(self.game.enemies)

        # Loop tot vragmotor stop en soldate aflaai (stop_timer is 40 ticks)
        for _ in range(50):
            truck.update(self.game)

        self.assertGreater(len(self.game.enemies), initial_enemy_count)

    def test_stage_progression_to_level_2(self):
        """Toets oorgang vanaf Vlak 1 (Vesting) na Vlak 2 (Rivier & Hangbrug)."""
        self.assertEqual(self.game.current_stage, 1)
        self.game.gate_open = True
        self.player.y = 50  # Hardloop deur hek

        self.game.update()
        # Moet nou in Vlak 2 wees
        self.assertEqual(self.game.current_stage, 2)
        self.assertGreaterEqual(self.player.score, 10000)
        # Vlak 2 moet rivier en brug hindernisse hê
        has_river_or_bridge = any(
            o.kind in (ObstacleType.RIVER, ObstacleType.BRIDGE)
            for o in self.game.obstacles
        )
        self.assertTrue(has_river_or_bridge)

    def test_rob_hubbard_theme_synthesized(self):
        """Toets dat die Rob Hubbard SID-tema korrek gesintetiseer is."""
        self.assertIn("theme", sounds.sound_paths)
        theme_path = sounds.sound_paths["theme"]
        self.assertTrue(os.path.exists(theme_path))
        self.assertGreater(os.path.getsize(theme_path), 50000)

    # --------------------------------------------------------------------------
    # NUWE TOETSE VIR INKREMENT 3 (OPSIE D: POWs, KRATTE, HOËTELLINGS, VLAK 3)
    # --------------------------------------------------------------------------

    def test_hostage_rescue_by_eliminating_guard(self):
        """Toets dat 'n gyselaar (POW) bevry word wanneer sy wag doodgemaak word."""
        guard = Enemy(x=150, y=800, kind=EnemyType.SOLDIER)
        self.game.enemies.append(guard)
        hostage = Hostage(x=140, y=800, guard=guard)
        self.game.hostages.append(hostage)

        initial_score = self.player.score
        # Skiet die wag
        guard.is_alive = False
        self.game.update()

        self.assertTrue(hostage.is_rescued)
        # Speler kry +1000 punte vir bevryding
        self.assertEqual(self.player.score, initial_score + 1000)

    def test_hostage_friendly_fire(self):
        """Toets dat 'n gyselaar wat per abuis getref word nie punte gee nie en sterf."""
        hostage = Hostage(x=160, y=700)
        self.game.hostages.append(hostage)
        initial_score = self.player.score

        # Spelerkoeël tref die gyselaar
        bullet = Bullet(x=160, y=705, direction=Direction.UP, is_player=True)
        self.game.bullets.append(bullet)
        self.game.update()

        self.assertFalse(hostage.is_alive)
        self.assertFalse(hostage.is_rescued)
        self.assertEqual(self.player.score, initial_score)

    def test_supply_crate_pickup(self):
        """Toets dat Super Joe 'n granaatkrat optel en +3 granate kry."""
        crate = SupplyCrate(x=self.player.x, y=self.player.y - 10)
        self.game.supply_crates.append(crate)
        initial_grenades = self.player.grenades
        initial_score = self.player.score

        # Speler beweeg oor die krat
        self.player.set_input(up=True)
        self.game.update()

        self.assertFalse(crate.is_alive)
        self.assertEqual(self.player.grenades, initial_grenades + 3)
        self.assertGreater(self.player.score, initial_score)

    def test_high_score_manager(self):
        """Toets dat die hoëtellingstelsel laai, stoor en nuwe tellings rangskik."""
        test_file = "/tmp/test_commando_highscores.json"
        if os.path.exists(test_file):
            os.remove(test_file)

        mgr = HighScoreManager(filepath=test_file)
        scores = mgr.get_scores()
        self.assertEqual(len(scores), 5)
        # Hoogste moet Butler wees
        self.assertEqual(scores[0]["name"], "BUTLER")

        # Voeg 'n nuwe rekord-telling by
        rank = mgr.add_score("SUPERJOE", 99990)
        self.assertEqual(rank, 1)
        self.assertEqual(mgr.get_scores()[0]["name"], "SUPERJOE")
        self.assertEqual(mgr.get_scores()[0]["score"], 99990)

        # Kontroleer dat lêer op skyf geskryf is
        self.assertTrue(os.path.exists(test_file))

    def test_stage_3_and_victory(self):
        """Toets oorgang na Vlak 3 (Woestynvesting) en finale oorwinning."""
        # Laai vlak 2 en voltooi dit
        self.game.load_stage(2)
        self.game.gate_open = True
        self.player.y = 50
        self.game.update()

        # Moet nou in Vlak 3 wees
        self.assertEqual(self.game.current_stage, 3)
        self.assertEqual(self.game.stage_banner_text, "AREA 3: DESERT FORTRESS")

        # Maak Vlak 3 se hekwagte dood en breek deur Hek 3
        for e in self.game.enemies:
            if e.kind == EnemyType.GATE_GUARD:
                e.is_alive = False
        self.game.update()
        self.assertTrue(self.game.gate_open)

        # Stap deur die finale vestinghek
        self.player.y = 50
        self.game.update()

        # Die speletjie is finaal gewen!
        self.assertTrue(self.game.game_won)
        self.assertGreaterEqual(self.player.score, 35000)

    # --------------------------------------------------------------------------
    # NUWE TOETSE VIR INTROSKERM, DEMO-MODUS, CRT SCANLINES & CONFIG JSON
    # --------------------------------------------------------------------------

    def test_config_manager_load_and_save(self):
        """Toets dat ConfigManager instellings na config.json skryf en laai."""
        cfg_file = "/tmp/test_commando_config.json"
        if os.path.exists(cfg_file):
            os.remove(cfg_file)

        cfg = ConfigManager(filepath=cfg_file)
        self.assertTrue(cfg.get("scanlines", True))

        # Verander instelling en stoor
        cfg.set("scanlines", False)
        cfg.set("sound_volume", 0.8)

        # Laai nuwe instansie vanaf dieselfde lêer
        cfg2 = ConfigManager(filepath=cfg_file)
        self.assertFalse(cfg2.get("scanlines"))
        self.assertEqual(cfg2.get("sound_volume"), 0.8)

    def test_game_mode_title_and_demo_transition(self):
        """Toets dat die speletjie in TITLE modus begin en na DEMO oorskakel."""
        game = GameState(width=320, height=200, world_height=1200, start_mode=GameMode.TITLE)
        self.assertEqual(game.mode, GameMode.TITLE)

        # Laat tyd verloop tot die demo afskop (bv. 10 ticks in toetsmodus)
        game.demo_timer = 1
        game.update_title()
        self.assertEqual(game.mode, GameMode.DEMO)

        # Begin die spelronde as speler 'n sleutel druk
        game.start_game()
        self.assertEqual(game.mode, GameMode.PLAYING)
        self.assertFalse(game.is_demo)

    def test_demo_ai_controller(self):
        """Toets dat DemoAI Super Joe outomaties beheer sonder foute."""
        game = GameState(width=320, height=200, world_height=1200, start_mode=GameMode.DEMO)
        ai = DemoAI()
        initial_y = game.player.y

        # Laat AI 'n paar ticks hardloop
        for _ in range(15):
            ai.update(game)
            game.update()

        # Joe moet vorentoe beweeg het
        self.assertLess(game.player.y, initial_y)

    def test_high_score_name_entry(self):
        """Toets dat naam-invoer werk en rekord korrek opgeslaan word."""
        test_file = "/tmp/test_commando_name_entry.json"
        if os.path.exists(test_file):
            os.remove(test_file)
        game = GameState(width=320, height=200, world_height=1200)
        game.high_score_mgr = HighScoreManager(filepath=test_file)
        game.player.score = 50000
        game.mode = GameMode.NAME_ENTRY
        game.name_entry_buffer = ""

        # Tik 'MIC' in
        game.handle_text_input("M")
        game.handle_text_input("I")
        game.handle_text_input("C")
        self.assertEqual(game.name_entry_buffer, "MIC")

        # Druk Backspace
        game.handle_backspace()
        self.assertEqual(game.name_entry_buffer, "MI")

        # Tik 'CH' en druk Enter
        game.handle_text_input("C")
        game.handle_text_input("H")
        game.confirm_name_entry()

        self.assertEqual(game.mode, GameMode.HALL_OF_FAME)
        scores = game.high_score_mgr.get_scores()
        self.assertEqual(scores[0]["name"], "MICH")
        self.assertEqual(scores[0]["score"], 50000)

    def test_rob_hubbard_highscore_synthesized(self):
        """Toets dat Rob Hubbard se High Score wysie gesintetiseer is."""
        self.assertIn("highscore", sounds.sound_paths)
        hs_path = sounds.sound_paths["highscore"]
        self.assertTrue(os.path.exists(hs_path))
        self.assertGreater(os.path.getsize(hs_path), 50000)

if __name__ == "__main__":
    unittest.main()
