# ⚙️ Vention Linear Axis Control (ROS 2)

This **ROS 2 package** enables control of a **Vention linear actuator** via a socket interface. The control node listens to a position command topic and sends the desired position to the actuator over TCP/IP.

---

## ✨ Features

- Simple socket-based communication to Vention actuator
- ROS 2 Humble compatible
- Listens to `/vention/axis1_position_cmd` topic
- Accepts float64 position commands (e.g., in mm or encoder counts)
- Lightweight and easy to integrate into larger robotic systems

---

## 🛠️ Usage

1. **Run the control script** by navigating to the `<path_to_src>/src/vention_ros/vention_ros` folder

   ```bash
   python3 vention_socket_control.py


2. Publish on

   ```bash
   ros2 topic pub /vention/axis1_position_cmd std_msgs/Float64 "data: 650.0"
