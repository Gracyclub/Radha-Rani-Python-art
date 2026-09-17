import cv2
import pygame
import numpy as np
import random
import sys

image_path = "radhaashtami.jpg"
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not load '{image_path}'. Make sure it's in the same folder.")
    sys.exit()

# Reel / Desktop Display Size
target_h = 840
h, w = img.shape[:2]
target_w = int(w * (target_h / h))

img_resized = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

pygame.init()
screen = pygame.display.set_mode((target_w, target_h))
pygame.display.set_caption("Shri Radha Rani - Grand Divine Reveal")
clock = pygame.time.Clock()

# Full HD Surface
full_surface = pygame.surfarray.make_surface(np.transpose(img_rgb, (1, 0, 2)))

# Scan Parameters
scan_y = float(target_h)
scan_speed = 5.2  # Smooth pacing (~5 seconds complete reveal for high watch-time)

# Persistent Background & Beam Sparkles
ambient_sparkles = [
    {
        'x': random.uniform(0, target_w),
        'y': random.uniform(0, target_h),
        'speed_y': random.uniform(-1.2, -0.4),
        'radius': random.uniform(1.2, 3.2),
        'alpha': random.randint(120, 255),
        'color': random.choice([(255, 235, 170), (255, 215, 120), (255, 255, 255)])
    }
    for _ in range(90)
]

beam_sparkles = []

running = True
finished = False
freeze_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Deep Divine Canvas Base
    screen.fill((8, 6, 12))

    # 1. Image reveal section from bottom up
    if scan_y < target_h:
        reveal_height = target_h - int(scan_y)
        reveal_rect = pygame.Rect(0, int(scan_y), target_w, reveal_height)
        screen.blit(full_surface, (0, int(scan_y)), reveal_rect)

    # 2. Grand Broad Golden Glow Beam (Full Width)
    if not finished:
        glow_height = 64  # Broad glowing beam
        beam_surf = pygame.Surface((target_w, glow_height), pygame.SRCALPHA)
        
        half_h = glow_height / 2
        for i in range(glow_height):
            dist_from_center = abs(i - half_h)
            intensity = max(0.0, 1.0 - (dist_from_center / half_h))
            alpha = int(240 * (intensity ** 1.6))
            
            # Rich golden yellow gradient
            color = (255, int(210 + 40 * intensity), int(100 + 80 * intensity), alpha)
            pygame.draw.line(beam_surf, color, (0, i), (target_w, i))

        screen.blit(beam_surf, (0, int(scan_y) - glow_height // 2))

        # Spawn rich burst of sparkles continuously along the broad beam
        for _ in range(12):
            beam_sparkles.append({
                'x': random.uniform(0, target_w),
                'y': scan_y + random.uniform(-20, 20),
                'vx': random.uniform(-1.8, 1.8),
                'vy': random.uniform(-1.5, 3.0),
                'life': random.randint(25, 45),
                'max_life': 45,
                'size': random.uniform(1.5, 4.0),
                'color': random.choice([(255, 245, 190), (255, 220, 120), (255, 190, 80)])
            })

        scan_y -= scan_speed
        if scan_y <= 0:
            scan_y = 0
            finished = True

    # 3. Render Beam Sparkles
    for sp in beam_sparkles[:]:
        sp['x'] += sp['vx']
        sp['y'] += sp['vy']
        sp['life'] -= 1
        
        if sp['life'] <= 0:
            beam_sparkles.remove(sp)
        else:
            alpha_ratio = sp['life'] / sp['max_life']
            radius = max(1, int(sp['size'] * alpha_ratio))
            pygame.draw.circle(screen, sp['color'], (int(sp['x']), int(sp['y'])), radius)

    # 4. Render Ambient Full-Screen Sparkles (always active)
    for asp in ambient_sparkles:
        asp['y'] += asp['speed_y']
        if asp['y'] < 0:
            asp['y'] = target_h
            asp['x'] = random.uniform(0, target_w)
        pygame.draw.circle(screen, asp['color'], (int(asp['x']), int(asp['y'])), int(asp['radius']))

    pygame.display.flip()
    clock.tick(60)

    # Post-reveal freeze buffer for screen recording
    if finished:
        freeze_counter += 1
        if freeze_counter > 160:  # ~2.7 seconds pause on full clear picture
            break

pygame.quit()