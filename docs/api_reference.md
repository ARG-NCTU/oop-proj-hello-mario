# API Reference and Usage Guide

This document describes every publicly accessible module, class, function, and helper contained in the repository. It also includes guidance on how to run each module and short code examples that illustrate typical usage.

## Prerequisites

- Python 3.10+ with `pygame`, `pandas`, `seaborn`, `matplotlib`, and `numpy` installed.
- All assets under `img/` and `sound/` must be present because most sprites and sounds are loaded at import time.
- To run any of the interactive demos, execute the modules directly with `python <module>.py` from the workspace root so the relative asset paths resolve.

---

## Module: `main.py`

`main.py` hosts the primary side-scrolling Mario-style game, including score tracking, analytics, sprite classes, and level management. Running `python main.py` launches the full experience.

### Scoreboard & Analytics Helpers

| API | Description |
| --- | --- |
| `read_leaderboard() -> list[int]` | Loads `leaderboard.json` (if present) and returns the stored scores. |
| `write_leaderboard(leaderboard: list[int]) -> None` | Persists the top scores list back to disk. |
| `update_leaderboard(new_score: int) -> list[int]` | Appends a score, keeps the top 5 entries, rewrites the file, and returns the truncated list. |
| `create_dataframe(scores: list[int]) -> pandas.DataFrame` | Converts raw score numbers into a DataFrame with synthetic player names. |
| `picture() -> None` | Renders a bar chart of leaderboard standings with mean and standard deviation annotations using Seaborn/Matplotlib. |

**Usage example**

```python
from main import read_leaderboard, update_leaderboard, picture

scores = read_leaderboard()
print("Previous top scores:", scores)

scores = update_leaderboard(new_score=250)
print("Updated top 5:", scores)

# Launch analytics view (blocks until the Matplotlib window closes)
picture()
```

### Text & Screen Utilities

- `draw_text(surf, text, size, x, y)` renders centered text to any surface.
- `draw_init()` displays the start screen and blocks until a key press.
- `darken_screen()` runs a fade-to-black transition that is reused for level intro/outro sequences.
- `show_leaderboard(leaderboard)` blits a formatted leaderboard overlay for 5 seconds.
- `show_game_over()` handles the lose-state: plays audio, fades out, records the score, and shows the leaderboard.
- `show_level(level_index)` flashes the current level indicator.

**Usage example**

```python
import pygame
from main import draw_text, darken_screen, show_level

pygame.init()
screen = pygame.display.set_mode((800, 600))
draw_text(screen, "Custom Overlay", 48, 400, 100)
pygame.display.flip()
darken_screen()
show_level(2)
```

### Sprite Classes

Each sprite inherits from `pygame.sprite.Sprite` and is meant to be managed through sprite groups.

#### `Coin(type: int, coin_num: int, coin_start: int)`

- Creates collectible coins either on the ground (`type == 1`) or elevated platforms.
- Automatically removes itself when moving outside the horizontal bounds.

```python
coin = Coin(type=1, coin_num=3, coin_start=500)
coins.add(coin)
all_sprites.add(coin)
```

#### `Player()`

Represents the controllable Mario character with gravity, jumping, shooting, scoring, and collision handling (`collide_with_bricks`, `collide_with_skystage`, `eat_coin`, `shoot`). Public attributes include `score`, `bullet_num`, `direction`, and `rect`.

```python
player = Player()
all_sprites.add(player)

# Within the main loop:
all_sprites.update()
if user_input_shoots:
    player.shoot()
```

#### `Enemy()`, `FlyingTurtle(x: int)`

Ground-based enemies patrol between random bounds, while flying turtles oscillate horizontally at elevated positions. Both flip their sprite depending on direction and can be destroyed by bullets.

```python
enemy = Enemy()
turtle = FlyingTurtle(1800)
enemies.add(enemy, turtle)
all_sprites.add(enemy, turtle)
```

#### `Bullet(x: int, y: int, direction: int)`

Projectiles spawned by the player. They auto-move horizontally, self-destruct off-screen, and remove the first enemy they collide with.

```python
bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
bullets.add(bullet)
all_sprites.add(bullet)
```

#### `Flag(x: int)`, `Cloud()`, `GoldBrick(x, y)`

Scenery and interactive objects that the level loader positions to mark objectives, provide parallax, or enable head-bump coin spawns.

#### Terrain Helpers: `Object`, `Block`, `get_block`

`Object` provides a rectangular surface baseline. `Block` composes textured tiles via `get_block`, which rescales `img/brick_with_grass_resized.png`. These classes underpin the ground/floating platforms.

### Procedural Generation Functions

- `create_coin(existing_end_positions: list[int]) -> int`: Spawns a horizontal coin strip and returns the last x-position to avoid overlap.
- `create_floating_block(x: int) -> None`: Places a random cluster of sky blocks near `x`.

### Level Management

- `levels`: a list where each entry declares `flying_turtles`, `gold_bricks`, and `flag` placements.
- `load_level(level_index, pre_score, pre_bullet_num)` wipes all sprite groups, rebuilds terrain, reinstates the player with preserved stats, offers a coin-for-bullet exchange, and returns `(current_level, score, bullets)`.
- `load_next_level(pre_score, pre_bullet_num)` increments `current_level`, calls `load_level`, and returns the updated tuple or `(None, score, bullets)` when the campaign ends.

**Usage example**

```python
current_level = -1
current_level, score, bullets = load_next_level(pre_score=0, pre_bullet_num=10)
if current_level is None:
    print("No more levels left!")
```

### Game Loop Entry Point

Executing `python main.py` performs the following:

1. Initializes all sprites, enemies, coins, bricks, sky platforms, and audio assets.
2. Starts the background music and waits on `draw_init()`.
3. Runs the 60 FPS loop that updates sprites, handles user input (arrow keys + down for shooting), tracks collisions, transitions levels, and renders the HUD (`Score`/`Bullets` counters).
4. Shows analytics (`picture()`) before closing when the player dies or clears all levels.

To integrate pieces of this module elsewhere, import only the utilities you need; avoid importing `main` at module load time if your environment cannot initialize Pygame (because asset loading runs immediately).

---

## Module: `group5.py`

`group5.py` is a earlier prototype of the Mario gameplay with a simplified ruleset and smaller cast of sprites. The module is self-contained and runs a loop when executed directly.

### Transition & UI Helpers

- `darken_screen()` — same behavior as in `main.py`, used to teleport the player when exiting the right edge.
- `show_game_over()` — displays a blocking “GAME OVER” overlay and plays the corresponding audio cue.

### Sprite Classes

- `Player`: Similar basics to `main.Player` but lacks scoring/bullets. Includes downward movement when pressing `K_DOWN`.
- `Enemy1`, `Enemy2`: Ground patrol enemies with fixed ranges and different speeds. Constructors do not take arguments and set up movement bounds automatically.
- `FlyingTurtle`: Mid-air patrol enemy with a wide movement range.

**Usage example**

```python
from group5 import Player, Enemy1, FlyingTurtle

player = Player()
enemy = Enemy1()
air_enemy = FlyingTurtle()

all_sprites = pygame.sprite.Group(player, enemy, air_enemy)
enemies = pygame.sprite.Group(enemy, air_enemy)
```

### Running the Prototype

```bash
python group5.py
```

The module:

1. Sets up the background, music, player, and three enemy variants.
2. Updates sprites each frame and ends the session if the player collides with any enemy.

---

## Module: `transition.py`

This utility module isolates the `darken_screen()` effect for experimentation.

- Constants: `FPS`, `BLACK`, `WHITE`, and a minimal Pygame surface (`100x100`) for previewing the fade.
- `darken_screen()` duplicates the same logic as the main game but with a shorter delay (`10 ms`).

**Usage example**

```python
from transition import darken_screen

darken_screen()
```

This is useful for testing transition timing without starting the full game.

---

## Module: `Sam/project3.py`

`project3.py` presents an alternative sandbox focusing on camera scrolling, precise collision, and modular terrain blocks.

### Background Helpers

- `get_background(name: str) -> tuple[list[tuple[int, int]], pygame.Surface]` tiles a background image to cover the viewport and returns tile positions plus the surface.
- `draw_background(screen, background, bg_img, player, blocks)` blits the tiled background, renders blocks, and draws the player before flipping the display.

### Player Class

`Player(x, y, width, height)` expands on the main character with:

- Horizontal helpers (`move_left`, `move_right`, `move`)
- Jump physics (`loop`, `landed`, `hit_head`, `fall_time`, `y_vel`)
- Pixel-perfect collision masks via `update`

### Collision & Movement

- `handle_vertical_collision(player, objects, dy)` clamps the player against solid objects and returns the collided list.
- `handle_movement(player, objects)` reads the keyboard, updates `x_vel`, moves horizontally, and calls `handle_vertical_collision`.

### Terrain

- `Object`/`Block` classes (similar to `main.py`), plus `get_block(width, height)` for grabbing the brick tile.

### Entry Point

- `main(screen)` sets up the scene, creates a `Player`, instantiates an infinite floor, and runs the typical Pygame loop until the window closes. The module calls `main(screen)` automatically when executed.

**Usage example**

```python
if __name__ == "__main__":
    from Sam.project3 import main
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((2400, 1000))
    main(screen)
```

---

## Modules: `Sam/movecamera.py` and `Sam/movecamerax.py`

Both scripts demonstrate camera scrolling techniques using a single player sprite and a background image.

### Shared APIs

- `darken_screen()` — identical fade-to-black helper.
- `Player` — arrow-key movement with screen wrapping when exiting the right edge.
- Global objects: `all_sprites`, `player`, `camera_offset`.
- Main loop — updates the player, recalculates `camera_offset`, draws the parallax-scrolling background plus sprites, and updates the display.

### Differences

- `movecamera.py` allows the camera to track both X and Y axes.
- `movecamerax.py` locks the Y offset to `0`, creating a horizontal-only scroll illusion.

**Usage example**

```bash
python Sam/movecamera.py
# or
python Sam/movecamerax.py
```

Integrate the camera concept elsewhere by copying the `camera_offset` logic or importing the module and reusing the `Player` sprite class.

---

## Running Automated Docs Examples

Where applicable, the snippets show how to import a class or function directly. When integrating these APIs into other games or tests:

1. Always call `pygame.init()` (and `pygame.mixer.init()` if you need audio) before instantiating sprites.
2. Load assets relative to the workspace root or adjust the working directory accordingly.
3. Use `pygame.sprite.Group` instances to manage updates/drawing, as every sprite here relies on the group update cycle.

With this reference you can confidently reuse, extend, or embed the provided components in new prototypes.
