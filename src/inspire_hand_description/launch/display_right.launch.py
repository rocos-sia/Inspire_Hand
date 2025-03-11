import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro


def generate_launch_description():
    package_name = 'inspire_hand_description'
    # urdf_name = "diana_v2.urdf"
    ld = LaunchDescription()
    pkg_share = FindPackageShare(package=package_name).find(package_name)

    rviz_file = os.path.join(pkg_share, 'rviz/right_hand.rviz')

    diana_xacro_path = os.path.join(pkg_share, 'urdf/inspire_hand_right_mimic.urdf')
    diana7_description = xacro.process_file(diana_xacro_path).toprettyxml(indent="  ")

    # urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{"robot_description": diana7_description}],
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        # arguments=[diana7_description],
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=["--display-config", rviz_file]
    )
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz2_node)
    return ld
