from sim_time_manager import SimTimeManager
import argparse
import re
import threading
from vesc import fw_6_00, fw
import sys
from riding import motor_state


def firmwareRegex(argValue, pattern=re.compile(r"^\d*[.]\d*$")):
    if not pattern.match(argValue):
        raise argparse.ArgumentTypeError(
            "VESC firmware version specified as $MajorVersion.$MinorVersion, e.g 2.18"
        )
    return argValue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--vescFW",
        help="Specifies the VESC firmware version to be used in the simulation.",
        type=firmwareRegex,
    )
    parser.add_argument(
        "--comPort", help="The com port for the attached USB FTDI module."
    )
    args = parser.parse_args()
    com_port = args.comPort
    vesc_fw = args.vescFW
    motor_state = motor_state.MotorState(0.0, 0.0, 0.0)
    motor_state_lock = threading.Lock()
    cmp_thread = None
    if vesc_fw == fw.FirmwareVersion.FW_6_00.value:
        cmp = fw_6_00.FW6_00CMP(com_port, 100, motor_state, motor_state_lock)
        cmp_thread = threading.Thread(target=cmp.handle_command())
        cmp_thread.daemon = True
        cmp_thread.start()
    else:
        print("No VESC firmware specified. Exiting simulation.")
        sys.exit(1)

    cmp_thread.join()

    # stm = SimTimeManager()
    # stm.set_sim_time_step(10)
    # stm.start_sim()
