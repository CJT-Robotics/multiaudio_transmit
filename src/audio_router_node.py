#!/usr/bin/env python3

import rospy
from audio_common_msgs.msg import AudioData
from std_msgs.msg import Bool

class AudioRouter:
    def __init__(self):
        rospy.init_node('audio_router_node')

        self.publish_mic = True
        self.play_speaker = True

        rospy.Subscriber('operator/config/publish_mic', Bool, self.cb_mic_cfg)
        rospy.Subscriber('operator/config/play_speaker', Bool, self.cb_speaker_cfg)

        self.pub_to_robot = rospy.Publisher('robot/audio_in', AudioData, queue_size=10)
        self.pub_to_operator_speaker = rospy.Publisher('operator/audio_in', AudioData, queue_size=10)

        rospy.Subscriber('robot/audio_out', AudioData, self.cb_robot_audio)
        rospy.Subscriber('operator/audio_out_raw', AudioData, self.cb_operator_audio)

    def cb_mic_cfg(self, msg):
        self.publish_mic = msg.data

    def cb_speaker_cfg(self, msg):
        self.play_speaker = msg.data

    def cb_robot_audio(self, msg):
        if self.play_speaker:
            self.pub_to_operator_speaker.publish(msg)

    def cb_operator_audio(self, msg):
        if self.publish_mic:
            self.pub_to_robot.publish(msg)

if __name__ == '__main__':
    try:
        router = AudioRouter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass