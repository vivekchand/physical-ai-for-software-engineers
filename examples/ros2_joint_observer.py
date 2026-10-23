#!/usr/bin/env python3
"""Optional read-only JointState observer. Requires a sourced ROS 2 environment."""
import argparse
from datetime import datetime, timezone
import json
import time
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", default="/joint_states")
    args, ros_args = parser.parse_known_args()
    try:
        import rclpy
        from rclpy.node import Node
        from rclpy.qos import qos_profile_sensor_data
        from sensor_msgs.msg import JointState
    except ImportError:
        parser.error("Source ROS 2 with rclpy and sensor_msgs first. See day 9.")
    run_id = str(uuid.uuid4())

    class Observer(Node):
        def __init__(self):
            super().__init__("physical_ai_joint_observer")
            self.subscription = self.create_subscription(JointState, args.topic, self.on_sample, qos_profile_sensor_data)
            self.sequence = 0

        def on_sample(self, message):
            self.sequence += 1
            event = {"schema_version": 1, "synthetic": False, "run_id": run_id,
                     "sequence": self.sequence, "source": args.topic,
                     "source_time_ns": message.header.stamp.sec * 1_000_000_000 + message.header.stamp.nanosec,
                     "source_clock_domain": "publisher-defined-check-configuration",
                     "received_at": datetime.now(timezone.utc).isoformat(),
                     "received_monotonic_ns": time.monotonic_ns(),
                     "frame_id": message.header.frame_id, "joint_names": list(message.name),
                     "position": list(message.position), "velocity": list(message.velocity),
                     "effort": list(message.effort),
                     "units": "JointState conventions: rotational rad/Nm; prismatic m/N; inspect robot model",
                     "meaning": "reported-joint-state-not-proof-of-grasp-or-placement"}
            try:
                print(json.dumps(event, allow_nan=False), flush=True)
            except ValueError:
                self.get_logger().warning("Non-finite joint-state sample omitted")

    rclpy.init(args=ros_args)
    node = Observer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
