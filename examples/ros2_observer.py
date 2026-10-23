#!/usr/bin/env python3
"""Optional read-only ROS 2 odometry subscriber. Requires rclpy and nav_msgs."""
import argparse
from datetime import datetime, timezone
import json
import math
import time
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", default="/odom")
    args, ros_args = parser.parse_known_args()
    try:
        import rclpy
        from rclpy.node import Node
        from rclpy.qos import qos_profile_sensor_data
        from nav_msgs.msg import Odometry
    except ImportError:
        parser.error("Source a supported ROS 2 environment with rclpy and nav_msgs first. See day 9.")
    run_id = str(uuid.uuid4())

    class Observer(Node):
        def __init__(self):
            super().__init__("physical_ai_field_observer")
            self.subscription = self.create_subscription(Odometry, args.topic, self.on_sample, qos_profile_sensor_data)
            self.sequence = 0

        def on_sample(self, message):
            self.sequence += 1
            position = message.pose.pose.position
            orientation = message.pose.pose.orientation
            velocity = message.twist.twist.linear
            event = {"schema_version": 1, "synthetic": False, "run_id": run_id,
                     "sequence": self.sequence, "source": args.topic,
                     "source_time_ns": message.header.stamp.sec * 1_000_000_000 + message.header.stamp.nanosec,
                     "source_clock_domain": "publisher-defined-check-configuration",
                     "received_at": datetime.now(timezone.utc).isoformat(),
                     "received_monotonic_ns": time.monotonic_ns(),
                     "frame_id": message.header.frame_id, "child_frame_id": message.child_frame_id,
                     "position_m": [position.x, position.y, position.z],
                     "orientation_xyzw": [orientation.x, orientation.y, orientation.z, orientation.w],
                     "linear_speed_m_s": math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2),
                     "pose_covariance": list(message.pose.covariance),
                     "meaning": "reported-odometry-not-independent-physical-truth"}
            try:
                print(json.dumps(event, allow_nan=False), flush=True)
            except ValueError:
                self.get_logger().warning("Non-finite odometry sample omitted")

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
