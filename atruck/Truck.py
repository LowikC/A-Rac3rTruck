from Queue import Queue
from CameraStreamer import CameraStreamer
from TruckStatus import TruckStatus


class Truck(object):
    def __init__(self, engine):
        self.camera_images = Queue(maxsize=4)
        self.camera_streamer = CameraStreamer(self.camera_images, device_id=0)
        self.camera_streamer.start()
        self.status = TruckStatus()
        self.engine = engine
        self.current_cmd_id = 0
        self.running_commands = dict()  # cmd_id -> process

    def run(self):
        while not self.status.over:
            im_bgr, timestamp_s = self.camera_images.get(block=True, timeout=1)
            command = self.engine.get_command(im_bgr, timestamp_s, self.status)
            self.add_command(command)

        self.stop_all()

    def add_command(self, command):
        self.stop_conflicts(command)
        command.start()
        self.running_commands[self.current_cmd_id] = command
        self.current_cmd_id += 1

    def stop_conflicts(self, command):
        commands_ids_to_remove = []
        for cmd_id, previous_cmd in self.running_commands.items():
            if not previous_cmd.is_alive():
                commands_ids_to_remove.append(cmd_id)
            if command.conflicts(previous_cmd):
                previous_cmd.stop()

        for cmd_id in commands_ids_to_remove:
            self.running_commands[cmd_id].join()
            self.running_commands.pop(cmd_id)

    def stop_all(self):
        for cmd_id, previous_cmd in self.running_commands.items():
            previous_cmd.stop()

        for cmd_id, previous_cmd in self.running_commands.items():
            previous_cmd.join()

        self.camera_streamer.join()


