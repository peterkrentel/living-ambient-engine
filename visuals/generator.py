"""
Hypnotic visual generator using psychological triggers.
Creates procedural animations designed to capture attention and induce trance states.
Features fractal zooms, color cycling, and psychedelic effects.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import cv2
from pathlib import Path
from typing import Dict, Tuple, List
import math
from numba import jit
import colorsys


# JIT-compiled fractal functions for speed
@jit(nopython=True, cache=True)
def mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iter):
    """Generate Mandelbrot set with escape time algorithm."""
    result = np.zeros((height, width), dtype=np.float64)

    for py in range(height):
        for px in range(width):
            x0 = x_min + (px / width) * (x_max - x_min)
            y0 = y_min + (py / height) * (y_max - y_min)

            x, y = 0.0, 0.0
            iteration = 0

            while x*x + y*y <= 4.0 and iteration < max_iter:
                x_new = x*x - y*y + x0
                y = 2*x*y + y0
                x = x_new
                iteration += 1

            # Smooth coloring
            if iteration < max_iter:
                log_zn = math.log(x*x + y*y) / 2
                nu = math.log(log_zn / math.log(2)) / math.log(2)
                iteration = iteration + 1 - nu

            result[py, px] = iteration

    return result


@jit(nopython=True, cache=True)
def julia_set(width, height, x_min, x_max, y_min, y_max, c_real, c_imag, max_iter):
    """Generate Julia set."""
    result = np.zeros((height, width), dtype=np.float64)

    for py in range(height):
        for px in range(width):
            x = x_min + (px / width) * (x_max - x_min)
            y = y_min + (py / height) * (y_max - y_min)

            iteration = 0

            while x*x + y*y <= 4.0 and iteration < max_iter:
                x_new = x*x - y*y + c_real
                y = 2*x*y + c_imag
                x = x_new
                iteration += 1

            if iteration < max_iter:
                log_zn = math.log(x*x + y*y) / 2
                nu = math.log(log_zn / math.log(2)) / math.log(2)
                iteration = iteration + 1 - nu

            result[py, px] = iteration

    return result


class VisualGenerator:
    """Generate hypnotic procedural visuals."""
    
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
    
    def __init__(self, config: Dict, width: int = 1920, height: int = 1080, fps: int = 30):
        self.config = config
        self.width = width
        self.height = height
        self.fps = fps
        self.center = (width // 2, height // 2)
        
    def generate(self, duration: int, output_path: str) -> str:
        """Generate visual video file."""
        pattern_type = self.config.get('pattern', 'fibonacci_spiral')
        
        # Route to appropriate generator
        generators = {
            'fibonacci_spiral': self._generate_fibonacci_spiral,
            'sacred_geometry': self._generate_sacred_geometry,
            'slow_waves': self._generate_slow_waves,
            'organic_flow': self._generate_organic_flow,
            'platonic_solids': self._generate_platonic_solids,
            'mandelbrot': self._generate_mandelbrot,
            'julia': self._generate_julia,
            'flowing_waves': self._generate_flowing_waves,
            'particle_flow': self._generate_particle_flow,
            'geometric_morph': self._generate_geometric_morph,
            'fractal_zoom': self._generate_fractal_zoom,
        }
        
        generator = generators.get(pattern_type, self._generate_sacred_geometry)
        return generator(duration, output_path)
    
    def _get_color_at_time(self, t: float, total_frames: int) -> Tuple[int, int, int]:
        """Interpolate colors over time with smooth transitions."""
        progress = t / total_frames
        primary = np.array(self.config['colors']['primary'])
        secondary = np.array(self.config['colors']['secondary'])
        accent = np.array(self.config['colors']['accent'])
        
        # Smooth color cycling
        if progress < 0.33:
            ratio = progress / 0.33
            color = primary * (1 - ratio) + secondary * ratio
        elif progress < 0.66:
            ratio = (progress - 0.33) / 0.33
            color = secondary * (1 - ratio) + accent * ratio
        else:
            ratio = (progress - 0.66) / 0.34
            color = accent * (1 - ratio) + primary * ratio
            
        # Add pulse effect
        pulse_freq = self.config.get('pulse_frequency', 0.1)
        pulse = math.sin(t * pulse_freq * 2 * math.pi / self.fps) * 0.2 + 0.8
        color = color * pulse
        
        return tuple(np.clip(color, 0, 255).astype(int))
    
    def _generate_fibonacci_spiral(self, duration: int, output_path: str) -> str:
        """Generate Fibonacci spiral with golden ratio - highly hypnotic."""
        total_frames = duration * self.fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        speed = self.config.get('speed', 0.3)
        complexity = self.config.get('complexity', 0.7)

        for frame in range(total_frames):
            # Create gradient background
            img = self._create_gradient_background(frame, total_frames)
            draw = ImageDraw.Draw(img)

            color = self._get_color_at_time(frame, total_frames)
            accent = tuple(self.config['colors']['accent'])
            rotation = frame * speed * 0.02

            # Draw multiple layers of spirals
            num_spirals = int(8 * complexity)
            for i in range(num_spirals):
                angle_offset = (i / num_spirals) * 2 * math.pi
                layer_color = self._blend_colors(color, accent, i / num_spirals)
                self._draw_spiral(draw, rotation + angle_offset, layer_color, 0.5 + 0.5 * (i / num_spirals))

            # Draw center glow
            self._draw_center_glow(img, color, frame, total_frames)

            # Apply blur for dreamy effect
            img = img.filter(ImageFilter.GaussianBlur(radius=2))

            # Convert to OpenCV format
            frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

        out.release()
        return output_path

    def _create_gradient_background(self, frame: int, total_frames: int) -> Image.Image:
        """Create animated gradient background using vectorized operations."""
        primary = np.array(self.config['colors']['primary'], dtype=np.float32)
        secondary = np.array(self.config['colors']['secondary'], dtype=np.float32)

        # Create coordinate grids
        y_coords = np.arange(self.height).reshape(-1, 1)
        x_coords = np.arange(self.width).reshape(1, -1)

        center_x, center_y = self.width // 2, self.height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)

        # Calculate distances vectorized
        dist = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)

        pulse = 0.7 + 0.3 * math.sin(frame * 0.05)
        ratio = np.clip((dist / max_dist) * pulse, 0, 1)

        # Blend colors
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for c in range(3):
            img[:, :, c] = np.clip((primary[c] * (1 - ratio) + secondary[c] * ratio) * 0.4, 0, 255).astype(np.uint8)

        return Image.fromarray(img)

    def _blend_colors(self, c1: Tuple[int, int, int], c2: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
        """Blend two colors."""
        return tuple(int(c1[i] * (1 - ratio) + c2[i] * ratio) for i in range(3))

    def _draw_center_glow(self, img: Image.Image, color: Tuple[int, int, int], frame: int, total_frames: int):
        """Draw pulsing center glow."""
        draw = ImageDraw.Draw(img)
        pulse = 0.5 + 0.5 * math.sin(frame * 0.1)

        for r in range(100, 10, -10):
            alpha = (100 - r) / 100 * pulse
            glow_color = tuple(int(c * alpha) for c in color)
            draw.ellipse([
                self.center[0] - r, self.center[1] - r,
                self.center[0] + r, self.center[1] + r
            ], fill=glow_color)

    def _draw_spiral(self, draw, rotation: float, color: Tuple[int, int, int], alpha: float):
        """Draw a single Fibonacci spiral with thickness."""
        points = []
        max_radius = min(self.width, self.height) * 0.45

        for i in range(300):
            # Fibonacci spiral equation
            theta = i * 0.08 + rotation
            r = 20 + (max_radius - 20) * (1 - math.exp(-theta / 10))

            if r > max_radius:
                break

            x = self.center[0] + r * math.cos(theta)
            y = self.center[1] + r * math.sin(theta)
            points.append((x, y))

        if len(points) > 1:
            # Draw with varying thickness
            brightness = 0.4 + 0.6 * alpha
            final_color = tuple(int(c * brightness) for c in color)
            draw.line(points, fill=final_color, width=4)

    def _generate_sacred_geometry(self, duration: int, output_path: str) -> str:
        """Generate sacred geometry patterns - Flower of Life, Metatron's Cube."""
        total_frames = duration * self.fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        speed = self.config.get('speed', 0.3)
        symmetry = self.config.get('symmetry', 6)

        for frame in range(total_frames):
            # Create gradient background
            img = self._create_gradient_background(frame, total_frames)
            draw = ImageDraw.Draw(img)

            color = self._get_color_at_time(frame, total_frames)
            accent = tuple(self.config['colors']['accent'])
            rotation = frame * speed * 0.015
            pulse = 0.8 + 0.2 * math.sin(frame * 0.08)

            # Draw multiple rings of sacred geometry (Flower of Life pattern)
            base_radius = min(self.width, self.height) * 0.12 * pulse

            # Center circle with glow
            self._draw_center_glow(img, color, frame, total_frames)

            # Inner ring
            for i in range(symmetry):
                angle = (i / symmetry) * 2 * math.pi + rotation
                x = self.center[0] + base_radius * 1.8 * math.cos(angle)
                y = self.center[1] + base_radius * 1.8 * math.sin(angle)
                draw.ellipse([x - base_radius, y - base_radius, x + base_radius, y + base_radius],
                           outline=color, width=3)

            # Outer ring
            for i in range(symmetry * 2):
                angle = (i / (symmetry * 2)) * 2 * math.pi - rotation * 0.5
                x = self.center[0] + base_radius * 3.5 * math.cos(angle)
                y = self.center[1] + base_radius * 3.5 * math.sin(angle)
                draw.ellipse([x - base_radius * 0.8, y - base_radius * 0.8,
                            x + base_radius * 0.8, y + base_radius * 0.8],
                           outline=accent, width=2)

            # Connecting lines (Metatron's cube style)
            for i in range(symmetry):
                angle1 = (i / symmetry) * 2 * math.pi + rotation
                angle2 = ((i + 2) / symmetry) * 2 * math.pi + rotation
                x1 = self.center[0] + base_radius * 1.8 * math.cos(angle1)
                y1 = self.center[1] + base_radius * 1.8 * math.sin(angle1)
                x2 = self.center[0] + base_radius * 1.8 * math.cos(angle2)
                y2 = self.center[1] + base_radius * 1.8 * math.sin(angle2)
                line_color = self._blend_colors(color, accent, 0.5)
                draw.line([(x1, y1), (x2, y2)], fill=line_color, width=2)

            # Center circle
            draw.ellipse([self.center[0] - base_radius, self.center[1] - base_radius,
                         self.center[0] + base_radius, self.center[1] + base_radius],
                        outline=color, width=4)

            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

        out.release()
        return output_path

    def _generate_slow_waves(self, duration: int, output_path: str) -> str:
        """Generate slow, hypnotic wave patterns."""
        total_frames = duration * self.fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        speed = self.config.get('speed', 0.1)

        for frame in range(total_frames):
            img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            color = self._get_color_at_time(frame, total_frames)

            # Create wave pattern
            for y in range(self.height):
                for x in range(self.width):
                    # Multiple sine waves for complexity
                    wave1 = math.sin((x * 0.01 + frame * speed * 0.1))
                    wave2 = math.sin((y * 0.01 + frame * speed * 0.15))
                    wave3 = math.sin((x * 0.005 + y * 0.005 + frame * speed * 0.05))

                    intensity = (wave1 + wave2 + wave3) / 3
                    intensity = (intensity + 1) / 2  # Normalize to 0-1

                    img[y, x] = [int(c * intensity) for c in color]

            # Smooth it out
            img = cv2.GaussianBlur(img, (5, 5), 0)
            out.write(img)

        out.release()
        return output_path

    def _generate_organic_flow(self, duration: int, output_path: str) -> str:
        """Generate organic flowing particle patterns."""
        return self._generate_particle_flow(duration, output_path)

    def _generate_particle_flow(self, duration: int, output_path: str) -> str:
        """Generate flowing particle system."""
        total_frames = duration * self.fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        speed = self.config.get('speed', 0.4)
        complexity = self.config.get('complexity', 0.5)
        num_particles = int(100 * complexity)

        # Initialize particles
        particles = []
        for _ in range(num_particles):
            particles.append({
                'x': np.random.rand() * self.width,
                'y': np.random.rand() * self.height,
                'vx': (np.random.rand() - 0.5) * speed,
                'vy': (np.random.rand() - 0.5) * speed,
                'size': np.random.rand() * 5 + 2
            })

        for frame in range(total_frames):
            img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(img)

            color = self._get_color_at_time(frame, total_frames)

            # Update and draw particles
            for p in particles:
                # Flow field influence
                flow_x = math.sin(p['y'] * 0.01 + frame * 0.01) * speed
                flow_y = math.cos(p['x'] * 0.01 + frame * 0.01) * speed

                p['vx'] += flow_x * 0.1
                p['vy'] += flow_y * 0.1

                # Update position
                p['x'] += p['vx']
                p['y'] += p['vy']

                # Wrap around
                p['x'] = p['x'] % self.width
                p['y'] = p['y'] % self.height

                # Draw particle
                size = p['size']
                draw.ellipse([p['x'] - size, p['y'] - size,
                            p['x'] + size, p['y'] + size],
                           fill=color)

            img = img.filter(ImageFilter.GaussianBlur(radius=2))
            frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

        out.release()
        return output_path

    def _generate_platonic_solids(self, duration: int, output_path: str) -> str:
        """Generate rotating platonic solids projection."""
        total_frames = duration * self.fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        speed = self.config.get('speed', 0.35)

        for frame in range(total_frames):
            img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(img)

            color = self._get_color_at_time(frame, total_frames)
            rotation = frame * speed * 0.02

            # Draw cube projection
            size = min(self.width, self.height) * 0.2
            vertices = self._get_cube_vertices(size, rotation)

            # Draw edges
            edges = [(0,1), (1,2), (2,3), (3,0),  # Front face
                    (4,5), (5,6), (6,7), (7,4),   # Back face
                    (0,4), (1,5), (2,6), (3,7)]   # Connecting edges

            for edge in edges:
                p1 = vertices[edge[0]]
                p2 = vertices[edge[1]]
                draw.line([p1, p2], fill=color, width=3)

            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

        out.release()
        return output_path

    def _get_cube_vertices(self, size: float, rotation: float) -> List[Tuple[float, float]]:
        """Get 2D projection of rotating cube vertices."""
        vertices_3d = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]

        vertices_2d = []
        for v in vertices_3d:
            # Rotate around Y and X axes
            x, y, z = v

            # Y rotation
            x_rot = x * math.cos(rotation) - z * math.sin(rotation)
            z_rot = x * math.sin(rotation) + z * math.cos(rotation)

            # X rotation
            y_rot = y * math.cos(rotation * 0.7) - z_rot * math.sin(rotation * 0.7)
            z_final = y * math.sin(rotation * 0.7) + z_rot * math.cos(rotation * 0.7)

            # Project to 2D
            scale = size / (3 + z_final)
            x_2d = self.center[0] + x_rot * scale
            y_2d = self.center[1] + y_rot * scale

            vertices_2d.append((x_2d, y_2d))

        return vertices_2d

    def _generate_mandelbrot(self, duration: int, output_path: str) -> str:
        """Generate zooming Mandelbrot fractal."""
        return self._generate_fractal_zoom(duration, output_path, fractal_type='mandelbrot')

    def _generate_julia(self, duration: int, output_path: str) -> str:
        """Generate animated Julia set fractal."""
        return self._generate_fractal_zoom(duration, output_path, fractal_type='julia')

    def _generate_fractal_zoom(self, duration: int, output_path: str, fractal_type: str = 'mandelbrot') -> str:
        """Generate zooming fractal animation with psychedelic color cycling."""
        total_frames = duration * self.fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        speed = self.config.get('speed', 0.6)

        # Interesting zoom targets for Mandelbrot
        zoom_targets = [
            (-0.743643887037151, 0.131825904205330),  # Seahorse valley
            (-0.74529, 0.113075),                      # Spiral
            (-1.25066, 0.02012),                       # Lightning
            (-0.1015, 0.633),                          # Mini mandelbrot
        ]
        target_x, target_y = zoom_targets[0]

        # Use lower resolution for speed, then upscale
        render_width = self.width // 2
        render_height = self.height // 2

        for frame in range(total_frames):
            # Exponential zoom for smooth infinite zoom effect
            zoom = math.exp(frame * speed * 0.02)

            # Render fractal
            if fractal_type == 'julia':
                # Animate Julia set c parameter
                t = frame / total_frames
                c_real = -0.7 + 0.1 * math.sin(t * 2 * math.pi)
                c_imag = 0.27015 + 0.1 * math.cos(t * 2 * math.pi)
                img = self._render_julia_fast(zoom, frame, c_real, c_imag, render_width, render_height)
            else:
                img = self._render_mandelbrot_fast(zoom, frame, target_x, target_y, render_width, render_height)

            # Upscale to full resolution
            img = img.resize((self.width, self.height), Image.LANCZOS)

            # Add glow effect
            img = self._add_bloom(img)

            frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

        out.release()
        return output_path

    def _render_mandelbrot_fast(self, zoom: float, frame: int, center_x: float, center_y: float,
                                 width: int, height: int) -> Image.Image:
        """Render Mandelbrot using JIT-compiled function with color cycling."""
        # Calculate view bounds
        width_range = 3.5 / zoom
        height_range = width_range * height / width

        x_min = center_x - width_range / 2
        x_max = center_x + width_range / 2
        y_min = center_y - height_range / 2
        y_max = center_y + height_range / 2

        # More iterations for deeper zooms
        max_iter = min(100 + int(math.log(zoom + 1) * 50), 500)

        # Use JIT-compiled function
        fractal_data = mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iter)

        # Apply psychedelic color cycling
        img = self._apply_color_cycling(fractal_data, frame, max_iter)

        return Image.fromarray(img)

    def _render_julia_fast(self, zoom: float, frame: int, c_real: float, c_imag: float,
                           width: int, height: int) -> Image.Image:
        """Render Julia set using JIT-compiled function."""
        width_range = 3.5 / zoom
        height_range = width_range * height / width

        x_min, x_max = -width_range / 2, width_range / 2
        y_min, y_max = -height_range / 2, height_range / 2

        max_iter = min(100 + int(math.log(zoom + 1) * 50), 500)

        fractal_data = julia_set(width, height, x_min, x_max, y_min, y_max, c_real, c_imag, max_iter)

        img = self._apply_color_cycling(fractal_data, frame, max_iter)

        return Image.fromarray(img)

    def _apply_color_cycling(self, fractal_data: np.ndarray, frame: int, max_iter: int) -> np.ndarray:
        """Apply psychedelic color cycling to fractal data (vectorized for speed)."""
        height, width = fractal_data.shape

        # Color cycle offset based on frame
        color_offset = frame * 0.02

        # Normalize fractal data
        normalized = fractal_data / max_iter

        # Create mask for inside the set (black)
        inside_mask = normalized >= 1.0

        # Psychedelic color cycling using HSV (vectorized)
        hue = (normalized * 3 + color_offset) % 1.0
        sat = 0.8 + 0.2 * np.sin(normalized * 10)
        val = 0.5 + 0.5 * normalized

        # Convert HSV to RGB (vectorized)
        # Using simplified HSV to RGB conversion
        c = val * sat
        x = c * (1 - np.abs((hue * 6) % 2 - 1))
        m = val - c

        # Determine RGB based on hue sector
        h_sector = (hue * 6).astype(int) % 6

        r = np.zeros_like(hue)
        g = np.zeros_like(hue)
        b = np.zeros_like(hue)

        # Sector 0: R=C, G=X, B=0
        mask = h_sector == 0
        r[mask], g[mask], b[mask] = c[mask], x[mask], 0
        # Sector 1: R=X, G=C, B=0
        mask = h_sector == 1
        r[mask], g[mask], b[mask] = x[mask], c[mask], 0
        # Sector 2: R=0, G=C, B=X
        mask = h_sector == 2
        r[mask], g[mask], b[mask] = 0, c[mask], x[mask]
        # Sector 3: R=0, G=X, B=C
        mask = h_sector == 3
        r[mask], g[mask], b[mask] = 0, x[mask], c[mask]
        # Sector 4: R=X, G=0, B=C
        mask = h_sector == 4
        r[mask], g[mask], b[mask] = x[mask], 0, c[mask]
        # Sector 5: R=C, G=0, B=X
        mask = h_sector == 5
        r[mask], g[mask], b[mask] = c[mask], 0, x[mask]

        r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255

        # Stack into image
        img = np.stack([r, g, b], axis=-1).astype(np.uint8)

        # Set inside points to black
        img[inside_mask] = [0, 0, 0]

        return img

    def _add_bloom(self, img: Image.Image) -> Image.Image:
        """Add bloom/glow effect to bright areas."""
        # Create a blurred version
        blurred = img.filter(ImageFilter.GaussianBlur(radius=10))

        # Enhance brightness of blurred
        enhancer = ImageEnhance.Brightness(blurred)
        blurred = enhancer.enhance(1.3)

        # Blend original with bloom
        return Image.blend(img, blurred, 0.3)

    def _generate_flowing_waves(self, duration: int, output_path: str) -> str:
        """Generate flowing wave patterns (alias for slow_waves)."""
        return self._generate_slow_waves(duration, output_path)

    def _generate_geometric_morph(self, duration: int, output_path: str) -> str:
        """Generate morphing geometric shapes."""
        total_frames = duration * self.fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        speed = self.config.get('speed', 0.35)
        symmetry = self.config.get('symmetry', 4)

        for frame in range(total_frames):
            img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(img)

            color = self._get_color_at_time(frame, total_frames)

            # Morph between different polygon shapes
            num_sides = symmetry + int(math.sin(frame * speed * 0.01) * 2)
            num_sides = max(3, num_sides)

            radius = min(self.width, self.height) * 0.3
            points = []

            for i in range(num_sides):
                angle = (i / num_sides) * 2 * math.pi + frame * speed * 0.01
                x = self.center[0] + radius * math.cos(angle)
                y = self.center[1] + radius * math.sin(angle)
                points.append((x, y))

            if len(points) > 2:
                draw.polygon(points, outline=color, width=3)

            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_cv)

        out.release()
        return output_path

