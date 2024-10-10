import sys
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtBluetooth import QBluetoothSocket
from .start_sim_fixture import start_sim_process
from .bluetooth_socket_fixture import bluetooth_socket as socket
from . import vesc_state_msg_requester
import struct
import pytest
import time


def packetize(data: bytearray) -> bytes:
    packet = bytearray(256)
    i = 0
    packet[i] = 2
    i += 1
    packet[i] = len(data)
    i += 1
    packet[i : i + len(data)] = data
    i += len(data)
    # Sim doesn't check crc. So any value can be used.
    crcValue = 1111
    packet[i] = (crcValue >> 8) & 0xFF
    i += 1
    packet[i] = crcValue & 0xFF
    i += 1
    packet[i] = 3
    i += 1
    packet[i] = 0
    return bytes(packet)


@pytest.mark.skip(reason="This test is currently disabled.")
def test_set_erpm_command(start_sim_process, socket):
    app = QCoreApplication(sys.argv)
    while socket.state() != QBluetoothSocket.SocketState.ConnectedState:
        app.processEvents()
    commanded_erpm: int = 99999
    command = bytearray([8]) + bytearray(commanded_erpm.to_bytes(4, "big"))
    socket.write(packetize(command))
    app.processEvents()
    time.sleep(5)
    vsmr = vesc_state_msg_requester.VescStateMsgRequester(socket)
    vsmr.send_state_msg_request()
    count = 0
    while count < 30:
        while vsmr.state_msg_received == False:
            app.processEvents()
        vsmr.send_state_msg_request()
        count += 1
    assert len(vsmr.state_msg_buffer) > 0
    erpms = []
    currents = []
    for timestamp, byte_array in vsmr.state_msg_buffer:
        current = (struct.unpack(">I", byte_array[12:16])[0]) / 100.0
        currents.append(current)
        erpms.append(struct.unpack(">I", byte_array[30:34])[0])
    e = erpms[-5:]
    assert all(erpm == e[0] for erpm in e)
    c = currents[-7:]
    assert all(current == c[0] for current in c)
    socket.disconnectFromService()
    app.processEvents()
    socket.close()
    app.quit()