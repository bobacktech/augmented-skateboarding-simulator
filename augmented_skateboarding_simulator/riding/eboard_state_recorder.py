from datetime import datetime
from .eboard_kinematic_state import EboardKinematicState
from threading import Lock, Thread
import time
import struct


class EboardStateRecorder:

    def __init__(self, eks_lock: Lock, eks: EboardKinematicState, recording_period_ms: int):
        self.__eks: EboardKinematicState = eks
        self.__eks_lock: Lock = eks_lock
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.__record_file_name = f"skateboard_sim_data_recording_{timestamp}.bin"
        self.__recording_period_s: float = recording_period_ms / 1000.0
        self.__recording_thread = Thread(target=self.record, daemon=True)
        self.__stop_recording = False

    def start_recording(self) -> None:
        self.__start_time = time.time()
        self.__recording_thread.start()

    @property.setter
    def stop_recording(self, value: bool):
        self.__stop_recording = value

    def record(self) -> None:
        f = open(self.__record_file_name, "wb")
        while True:
            eks_bytes = None
            with self.__eks_lock:
                timestamp = time.time() - self.__start_time
                eks_bytes = struct.pack(
                    "d f f f f f f f i f",
                    timestamp,
                    self.__eks.velocity,
                    self.__eks.acceleration_x,
                    self.__eks.acceleration_y,
                    self.__eks.acceleration_z,
                    self.__eks.pitch,
                    self.__eks.roll,
                    self.__eks.yaw,
                    self.__eks.erpm,
                    self.__eks.input_current,
                )
            f.write(eks_bytes)
            if self.__stop_recording:
                f.close()
                break
            time.sleep(self.__recording_period_s)
