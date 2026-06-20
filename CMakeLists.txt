cmake_minimum_required(VERSION 3.0.2)
project(multiaudio_transmit)

find_package(catkin REQUIRED COMPONENTS
  rospy
  rqt_gui
  rqt_gui_py
  std_msgs
  audio_common_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  src/audio_router_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)