import rclpy
from rclpy.node import Node
import socket
import time


class VentionSocketControl(Node):
    def __init__(self):
        super().__init__('vention_socket_control_node')

        # --- Setup your IP and port here ---
        self.controller_ip = "192.168.7.2"
        self.controller_port = 9999

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2.0)

        try:
            self.sock.connect((self.controller_ip, self.controller_port))
            self.get_logger().info(f"Connected to MachineMotion controller at {self.controller_ip}:{self.controller_port}")
        except socket.error as e:
            self.get_logger().error(f"Socket connection failed: {e}")
            return

        # --- Main sequence ---
        if self.wait_until_ready():
            self.move_axis_abs(1, 100.0)
            self.move_axis_abs(1, 0.0)
        else:
            self.get_logger().warn("Controller not ready. Skipping move.")

        self.sock.close()

    def send_command(self, cmd: str) -> str:
        try:
            if not cmd.endswith(";"):
                cmd += ";"
            self.sock.sendall(cmd.encode() + b"\n")
            response = self.sock.recv(1024).decode().strip()
            self.get_logger().info(f"Sent: {cmd} | Received: {response}")
            return response
        except socket.error as e:
            self.get_logger().error(f"Socket error during command '{cmd}': {e}")
            return ""

    def is_ready(self) -> bool:
        response = self.send_command("isReady;")
        return "Ready = true" in response

    def is_busy(self) -> bool:
        response = self.send_command("isBusy;")
        return "Busy = true" in response


    def wait_until_ready(self, timeout_sec=10) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout_sec:
            if self.is_ready() and not self.is_busy():
                return True
            time.sleep(0.5)
        self.get_logger().warn("Timeout waiting for controller to be ready.")
        return False

    def move_axis_abs(self, axis: int, position_mm: float):
        cmd = f"SET im_move_abs_{axis}/{position_mm}/"
        self.send_command(cmd)
        time.sleep(1.0)

        while self.is_busy():
            self.get_logger().info(f"Axis {axis} is moving to {position_mm} mm...")
            time.sleep(0.5)
        self.get_logger().info(f"Axis {axis} motion to {position_mm} mm complete.")


def main(args=None):
    rclpy.init(args=args)
    node = VentionSocketControl()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
