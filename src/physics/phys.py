from src.physics.cloth import Cloth

class Phys:

    def cloth(self, w : int, h : int):
        return Cloth(w, h)

    def update(self, dt : float | int):
        pass