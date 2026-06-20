#!/usr/bin/env python3

import rospy
from rqt_gui_py.plugin import Plugin
from python_qt_binding.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel
from python_qt_binding.QtGui import QIcon
import os
import rospkg
from std_msgs.msg import Bool

class OperatorAudioPlugin(Plugin):
    def __init__(self, context):
        super(OperatorAudioPlugin, self).__init__(context)
        self.setObjectName('OperatorAudioPlugin')

        self.pub_mic_enable = rospy.Publisher('operator/config/publish_mic', Bool, queue_size=1, latch=True)
        self.pub_speaker_enable = rospy.Publisher('operator/config/play_speaker', Bool, queue_size=1, latch=True)

        self.current_mode = "Duplex"
        self._setup_ui(context)
        
        self.pub_mic_enable.publish(True)
        self.pub_speaker_enable.publish(True)

    def _setup_ui(self, context):
        self._widget = QWidget()

        try:
            rp = rospkg.RosPack()
            package_path = rp.get_path('multiaudio_transmit') 
            icon_path = os.path.join(package_path, 'res', 'favicon.png')
            self._widget.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            rospy.logwarn(e)
        
        layout = QVBoxLayout(self._widget)

        self._widget.setWindowTitle('Multiaudio Control Panel')

        mode_layout = QHBoxLayout()
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["Duplex", "PTT"])
        self.combo_mode.currentIndexChanged.connect(self._mode_changed)
        mode_layout.addWidget(QLabel("Modus:"))
        mode_layout.addWidget(self.combo_mode)
        layout.addLayout(mode_layout)

        self.btn_ptt = QPushButton("PUSH TO TALK")
        self.btn_ptt.setStyleSheet("background-color: #7f8c8d; color: white; font-weight: bold; font-size: 16px; padding: 30px;")
        self.btn_ptt.setEnabled(False)
        self.btn_ptt.pressed.connect(self._ptt_pressed)
        self.btn_ptt.released.connect(self._ptt_released)
        layout.addWidget(self.btn_ptt)

        context.add_widget(self._widget)

    def _mode_changed(self):
        if self.combo_mode.currentIndex() == 0:
            self.current_mode = "Duplex"
            self.btn_ptt.setEnabled(False)
            self.btn_ptt.setStyleSheet("background-color: #7f8c8d; color: white; font-weight: bold; font-size: 16px; padding: 30px;")
            self.pub_mic_enable.publish(True)
            self.pub_speaker_enable.publish(True)
        else:
            self.current_mode = "PTT"
            self.btn_ptt.setEnabled(True)
            self.btn_ptt.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; font-size: 16px; padding: 30px;")
            self.pub_mic_enable.publish(False)
            self.pub_speaker_enable.publish(True)

    def _ptt_pressed(self):
        if self.current_mode == "PTT":
            self.btn_ptt.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; font-size: 16px; padding: 30px;")
            self.pub_mic_enable.publish(True)
            self.pub_speaker_enable.publish(False)

    def _ptt_released(self):
        if self.current_mode == "PTT":
            self.btn_ptt.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; font-size: 16px; padding: 30px;")
            self.pub_mic_enable.publish(False)
            self.pub_speaker_enable.publish(True)

    def shutdown_plugin(self):
        try:
            self.pub_mic_enable.unregister()
            self.pub_speaker_enable.unregister()
        except:
            pass