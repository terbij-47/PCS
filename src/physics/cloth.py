from src.mth.vec3 import Vec3

class _Part:
    def __init__(self, x, y, z):
        self.pos = Vec3(x, y, z)
        self.prev_pos = Vec3(x, y, z)
        self.vel = Vec3()

    def update(self, new_pos : Vec3):
        self.prev_pos = self.pos
        self.pos = new_pos

class Cloth:
    G = Vec3(0, -9.81, 0)
    __offsets = ((1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 2**0.5), (1, -1, 2**0.5), (-1, 1, 2**0.5), (-1, -1, 2**0.5))

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.stiffness = 2 # жесткость пружины
        self.d0 = 0.001
        self.grid = []
        self.__tmp_grid = []
        self.m = 0.00001

        for x in range(w):
            tmp = []
            tmp2 = []
            zapas = 0.6
            for y in range(h):
                tmp.append(_Part(x * self.d0 * zapas, 0, y * self.d0 * zapas))
                tmp2.append(Vec3(x * self.d0 * zapas, 0, y * self.d0 * zapas))
            self.grid.append(tmp)
            self.__tmp_grid.append(tmp2)

    def __get_force(self, x, y):
        force = Vec3()

        pos = self.grid[x][y].pos

        for offset in self.__offsets:
            x1 = x + offset[0]
            y1 = y + offset[1]
            if 0 <= x1 < self.w and 0 <= y1 < self.h:
                p = self.grid[x + offset[0]][y + offset[1]].pos - pos
                l = p.len()
                force += (p / l) * self.stiffness * (l - self.d0 * offset[2])

        force -= self.grid[x][y].vel * 0.01
        force *= 1
        force += self.G * self.m
        force_len = force.len()
        # print(force_len)
        return force


    def update(self, dt):
        # print('origin: ', dt)
        dt = min(dt / 1000, 0.0007)

        for x in range(self.w):
            for y in range(self.h):
                force = self.__get_force(x, y)
                # print(force, 'delta time: ', dt)
                # self.__tmp_grid[x][y] = self.grid[x][y].pos * 2 - self.grid[x][y].prev_pos + force * dt * dt / self.m
                acc = force / self.m
                self.grid[x][y].vel += acc * dt
                self.__tmp_grid[x][y] += self.grid[x][y].vel * dt
        self.__tmp_grid[0][0] = Vec3()
        self.__tmp_grid[self.w - 1][0] = Vec3((self.w - 1) * self.d0 * 0.5, 0, 0 * self.d0 * 0.5)
        self.__tmp_grid[0][self.h - 1] = Vec3(0 * self.d0 * 0.5, 0, (self.h - 1) * self.d0 * 0.5)
        self.__tmp_grid[self.w - 1][self.h - 1] = Vec3((self.w - 1) * self.d0 * 0.5, 0, (self.h - 1) * self.d0 * 0.5)
        for x in range(self.w):
            for y in range(self.h):
                self.grid[x][y].update(self.__tmp_grid[x][y])


