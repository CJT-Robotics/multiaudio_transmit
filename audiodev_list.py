#!/usr/bin/env python3
import subprocess
import re

def get_devices(cmd):
    devices = []
    try:
        out = subprocess.check_output([cmd, "-l"], stderr=subprocess.DEVNULL).decode('utf-8')
        for line in out.splitlines():
            if ("card" in line or "Karte" in line) and ("device" in line or "Gerät" in line):
                c_id = re.search(r'(?:card|Karte)\s+(\d+):', line).group(1)
                d_id = re.search(r'(?:device|Gerät)\s+(\d+):', line).group(1)
                if "[" in line and "]" in line:
                    name = line.split("[")[1].split("]")[0].strip()
                else:
                    name_match = re.search(r'(?:card|Karte)\s+\d+:\s*([^,:]+)', line)
                    name = name_match.group(1).strip() if name_match else "Unknown"
                
                devices.append({'id': f"plughw:{c_id},{d_id}", 'name': name})
    except:
        pass
    return devices

def select(devices, label):
    if not devices:
        print(f"No {label} devices found.")
        return ""
    print(f"\n{label} Devices:")
    for i, d in enumerate(devices):
        print(f" [{i}] {d['name']} ({d['id']})")
    while True:
        try:
            val = input(f"Select {label} [0]: ").strip()
            return devices[int(val) if val else 0]['id']
        except:
            print("Invalid selection.")

def main():
    ins, outs = get_devices("arecord"), get_devices("aplay")
    chosen_in = select(ins, "INPUT")
    chosen_out = select(outs, "OUTPUT")
    
    print(f"""\n<launch>
    <node name="robot_audio_capture" pkg="audio_capture" type="audio_capture" output="screen">
        <param name="bitrate" value="128"/>
        <param name="device" value="{chosen_in}"/> 
        <param name="channels" value="2"/>
        <param name="sample_rate" value="44100"/>
        <param name="format" value="mp3"/>
        <remap from="audio" to="robot/audio_out" />
    </node>

    <node name="robot_audio_play" pkg="audio_play" type="audio_play" output="screen">
        <param name="device" value="{chosen_out}"/> 
        <param name="format" value="mp3"/>
        <remap from="audio" to="robot/audio_in" />
    </node>
</launch>""")

if __name__ == "__main__":
    main()