from mgba.core import load_vf, load_path
from mgba.gba import GBA
from mgba.image import Image
from mgba._pylib import ffi, lib

KEY_MAP = {
    "up": GBA.KEY_UP,
    "down": GBA.KEY_DOWN,
    "left": GBA.KEY_LEFT,
    "right": GBA.KEY_RIGHT,
    "A": GBA.KEY_A,
    "B": GBA.KEY_B,
    "L": GBA.KEY_L,
    "R": GBA.KEY_R,
    "start": GBA.KEY_START,
    "select": GBA.KEY_SELECT,
}

class PyGBA:
    def __init__(self, rom):
        self.core = load_path(rom)
        self.core.add_frame_callback(self._invalidate_mem_cache)

        if self.core is None:
            raise RuntimeError("Failed to load ROM")

        width, height = self.core.desired_video_dimensions()
        self.video_buffer = Image(width, height)
        self.core.set_video_buffer(self.video_buffer)

        self._mem_cache = {}

    def press_key(self, key):
        if key not in KEY_MAP:
            raise ValueError(f"Invalid key: {key}")
        
        self.core.add_keys(KEY_MAP[key])

    def release_key(self, key):
        if key not in KEY_MAP:
            raise ValueError(f"Invalid key: {key}")
        
        self.core.clear_keys(KEY_MAP[key])

    def _invalidate_mem_cache(self):
        self._mem_cache = {}
    
    def _get_memory_region(self, region_id: int):
        if region_id not in self._mem_cache:
            mem_core = self.core.memory.u8._core
            size = ffi.new("size_t *")
            ptr = ffi.cast("uint8_t *", mem_core.getMemoryBlock(mem_core, region_id, size))
            self._mem_cache[region_id] = ffi.buffer(ptr, size[0])[:]
        return self._mem_cache[region_id]

    def read_memory(self, address: int, size: int = 1):
        region_id = address >> lib.BASE_OFFSET
        mem_region = self._get_memory_region(region_id)
        mask = len(mem_region) - 1
        address &= mask
        return mem_region[address:address + size]

    def read_u8(self, address: int):
        return int.from_bytes(self.read_memory(address, 1), byteorder='little', signed=False)

    def read_u16(self, address: int):
        return int.from_bytes(self.read_memory(address, 2), byteorder='little', signed=False)

    def read_u32(self, address: int):
        return int.from_bytes(self.read_memory(address, 4), byteorder='little', signed=False)
