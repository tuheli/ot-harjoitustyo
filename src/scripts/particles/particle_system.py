import random

from scripts.particles.particle import Particle



class ParticleSystem:
    def __init__(self, velocity_range=(0, 0), size_range=(2, 5), lifetime_range=(0.5, 1.5)):
        self.particles: list[Particle] = []
        self.velocity_range = velocity_range
        self.size_range = size_range
        self.lifetime_range = lifetime_range

    def emit(self, position, num_particles):
        for _ in range(num_particles):
            velocity = [random.uniform(*self.velocity_range), random.uniform(*self.velocity_range)]
            size = random.randint(*self.size_range)
            color = (255, 255, 255)
            lifetime = random.uniform(*self.lifetime_range)
            particle = Particle(position, velocity, size, color, lifetime)
            self.particles.append(particle)

    def update(self, delta_time):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update(delta_time)

    def render(self, surface, camera_offset):
        for particle in self.particles:
            particle.render(surface, camera_offset)