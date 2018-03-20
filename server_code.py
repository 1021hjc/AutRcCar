import socket
import sys
import picamera
import time
import io
import struct
import gpioController as g

class SendTrainingData(object):
    def __init__(self):
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs.connect(('192.168.1.3',8000))
        self.connection = self.cs.makefile('wb')
        self.con = self.cs.makefile('rb')
        g.ControllerInit()
        g.receive_command()
        send_image()
       
    def send_image(self):
        try:
            with picamera.PiCamera() as cam:
                cam.resolution = (320,240)
                cam.framerate = 10
                time.sleep(2)
                start = time.time()
                stream = io.BytesIO()

                for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
                    receive_command()
                    self.connection.write(struct.pack('<L',stream.tell()))
                    self.connection.flush()
                    stream.seek(0)
                    self.connection.write(stream.read())
                    if time.time() - start > 600:
                        break
                    stream.seek(0)
                    stream.truncate()
            self.connection.write(struct.pack('<L',0))

        finally:
            self.connection.close()
            self.con.close()
            self.cs.close()
if __name__ == '__main__':
    SendTrainingData()
