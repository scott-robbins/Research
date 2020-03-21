from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import imutils
import time


class Particle:
    x = 0
    y = 0
    mass = 0.01
    force = [0.0, 0.0]  # [Magnitude, Direction (from vertical @ 0.0 deg]

    def __init__(self, initial_position):
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.mass = np.random.randint(1,10000,1)[0]

    def calculate_force(self, pts):
        forces = 0
        attractors = {}
        for ptB in pts:
            r = imutils.get_displacement(self.x, ptB.x, self.y, ptB.y)
            forces += attract_strength*(self.mass*ptB.mass)/r**2 - repel_strength*(self.mass*ptB.mass)/r**3
            attractors[r] = ptB
        return attractors[np.array(attractors.keys()).max()]

    def move_to(self, ptB):
        dx = ptB.x - self.x
        dy = ptB.y - self.y
        if dx > 1:
            self.x += 1
        elif dx < 1:
            self.x -= 1
        if dy > 1:
            self.y += 1
        elif dy < 1:
            self.y -= 1


class Swarm:
    width, height = 0, 0
    n_particles = 0
    time_step = 0
    state = [[]]
    goal = 'none'
    cells = []

    push = 0.0      # Repel strength between points
    pull = 0.0      # Pull strength between points

    def __init__(self, initial_state, pts, r_strength, a_strength):
        self.width = initial_state.shape[0]
        self.height = initial_state.shape[1]
        self.state = initial_state
        self.cells = pts
        self.push = r_strength
        self.pull = a_strength


# Simulation parameters
W = 350
H = 350
N_Steps = 250
N_Particles = 150
frame_rate = 10
pt_size = 1
attract_strength = 1
repel_strength = 1

# Initialize
print '[*] Creating [%d, %d] World' % (W, H)
state, points = imutils.add_random_points(np.zeros((W, H)), N_Particles, size=pt_size)
particles = list()
[particles.append(Particle(cell)) for cell in points]
swarm = Swarm(state,particles,repel_strength,attract_strength)
print '[*] %d Points added to World' % len(particles)

# Run the Simulation
tic = time.time()
f = plt.figure()
simulation = []
# simulation.append([plt.imshow(state, 'gray')])
progress = tqdm(total=N_Steps)
for step in range(N_Steps):
    # TODO: For each time step cycle through each particle onscreen and let them
    #  Feel the force of every other particle, both attractive and repulsive
    # particles, state = swarm.update(particles, state, 1)
    for particle in particles:
        try:
            state[particle.x-pt_size:particle.x+pt_size,
                  particle.y-pt_size:particle.y+pt_size] = 0
        except IndexError:
            pass
        strong_pull = particle.calculate_force(particles)
        particle.move_to(strong_pull)
        try:
            state[particle.x-pt_size:particle.x+pt_size,
                  particle.y-pt_size:particle.y+pt_size] = 1
        except IndexError:
            pass
    progress.update(1)
    simulation.append([plt.imshow(state, 'gray')])
progress.close()

print '[*] Simulation Finished [%ss Elapsed]' % str(time.time()-tic)
a = animation.ArtistAnimation(f, simulation, interval=frame_rate, blit=True, repeat_delay=900)
if raw_input('Do you want to save this: ').upper() == 'Y':
    name = raw_input('Enter Name for Animation: ')
    w = FFMpegWriter(fps=frame_rate,bitrate=1800)
    a.save(name,writer=w)
plt.show()
