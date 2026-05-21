from devices import video_matrix,audio_processor
import variables as vars
#=================== Video Matrix ===================
class VideoMatrix:
    def __init__(self, serial_interface):
        self.serial = serial_interface
    def _command_builder(self, index, length, body):
        """Build hex command"""
        checksum = (0xF0 + index + length + sum(body)) & 0xFF
        return bytes([0x7B, 0x7B, index, length] + body + [checksum, 0x7D, 0x7D])
    def tie(self, input_num, output_num):
        """Input -> Output"""
        cmd = self._command_builder(0x01, 0x02, [input_num-1, output_num-1])
        self.serial.Send(cmd)
    def tie_all(self, input_num):
        """Input -> All Outputs"""
        cmd = self._command_builder(0x01, 0x02, [input_num-1, 0xFF])
        self.serial.Send(cmd)
# Initialize matrix
matrix = VideoMatrix(video_matrix)
# Matrix input number mapping
MATRIX_INPUT_NUMBERS = {
    vars.MATRIX_INPUT_CAMERA:7,
    vars.MATRIX_INPUT_DESKTOP:9,
    vars.MATRIX_INPUT_DOC:10,
    vars.MATRIX_INPUT_BYOD:11,
    vars.MATRIX_INPUT_FLOOR:12,
}
# Matrix output number mapping
MATRIX_OUTPUT_NUMBERS = {
    vars.MATRIX_OUTPUT_LED:3,
    vars.MATRIX_OUTPUT_RECORDER:4,
    vars.MATRIX_OUTPUT_RETURN_TV:5,
    vars.MATRIX_OUTPUT_LEFT_TV:6,
    vars.MATRIX_OUTPUT_RIGHT_TV:7,
    vars.MATRIX_OUTPUT_CAPTURE:8,
}
def matrix_tie(input_name, output_name):
    """Switch input signal to output"""
    input_num = MATRIX_INPUT_NUMBERS.get(input_name)
    output_num = MATRIX_OUTPUT_NUMBERS.get(output_name)
    if input_num and output_num:
        matrix.tie(input_num, output_num)
        print("Matrix Tie: {} -> {}".format(input_name, output_name))
    else:
        print("Invalid input or output: {}, {}".format(input_name, output_name))
#=================== Audio Processor ===================
class AudioProcessor:
    """TOT TIGER Audio Processor Controller"""
    def __init__(self, serial_interface):
        self.serial = serial_interface
    def calcChkSum(self, cmdString):
        """Calculate checksum"""
        chkSum = sum(cmdString) % 0x100
        return chkSum.to_bytes(1, 'big')
    def _command_builder(self, index, length, body):
        """Build TIGER protocol command"""
        cmdString = bytes([index]) + bytes([length]) + bytes(body)
        return b'\xA5\xAB' + cmdString + self.calcChkSum(cmdString)  
    def set_input_volume(self, channel, value):
        """Set input volume"""
        vol_hex = int(hex((int(round(value, 1) * 100) + (1 << 16)) % (1 << 16)), 16)
        cmd = self._command_builder(0x02, 0x37, [channel, (vol_hex >> 8) & 0xFF, vol_hex & 0xFF])
        self.serial.Send(cmd)
    def set_input_mute(self, channel, state):
        """Set input mute"""
        value = 0x31 if state == 'On' else 0x32
        cmd = self._command_builder(0x02, value, [channel, channel, 0x00])
        self.serial.Send(cmd)
    def get_input_volume(self, channel):
        """Get input volume"""
        cmd = self._command_builder(0x02, 0xB7, [channel, 0x00, 0x00])
        response = self.serial.SendAndWait(cmd, 1000, deliLen=8)
        if response and len(response) >= 8:
            vol_value = int.from_bytes(response[5:7], 'big')
            if vol_value >= 32768:
                vol_value -= 65536
            return vol_value / 100.0
    def get_input_mute(self, channel):
        """Get input mute status"""
        cmd = self._command_builder(0x02, 0xB1, [0x00, 0x00, 0x00])
        response = self.serial.SendAndWait(cmd, 1000, deliLen=8)
        if response and len(response) >= 8:
            bitmask = int.from_bytes(response[5:7], 'big')
            return 'On' if (bitmask & (1 << (channel - 1))) else 'Off'
    def set_output_volume(self, channel, value):
        """Set output volume"""
        vol_hex = int(hex((int(round(value, 1) * 100) + (1 << 16)) % (1 << 16)), 16)
        cmd = self._command_builder(0x03, 0x37, [channel, (vol_hex >> 8) & 0xFF, vol_hex & 0xFF])
        self.serial.Send(cmd)
    def set_output_mute(self, channel, state):
        """Set output mute"""
        value = 0x31 if state == 'On' else 0x32
        cmd = self._command_builder(0x03, value, [channel, channel, 0x00])
        self.serial.Send(cmd)
    def get_output_volume(self, channel):
        """Get output volume"""
        cmd = self._command_builder(0x03, 0xB7, [channel, 0x00, 0x00])
        response = self.serial.SendAndWait(cmd, 1000, deliLen=8)
        if response and len(response) >= 8:
            vol_value = int.from_bytes(response[5:7], 'big')
            if vol_value >= 32768:
                vol_value -= 65536
            return vol_value / 100.0
    def get_output_mute(self, channel):
        """Get output mute status"""
        cmd = self._command_builder(0x03, 0xB1, [0x00, 0x00, 0x00])
        response = self.serial.SendAndWait(cmd, 1000, deliLen=8)
        if response and len(response) >= 8:
            bitmask = int.from_bytes(response[5:7], 'big')
            return 'On' if (bitmask & (1 << (channel - 1))) else 'Off'
    def save_preset(self):
        """Save preset"""
        cmd = self._command_builder(0x01, 0x40, [0x00, 0x00, 0x00])
        self.serial.Send(cmd)
    def recall_preset(self, preset_num):
        """Recall preset"""
        cmd = self._command_builder(0x01, 0x30, [0x01, preset_num, 0x00])
        self.serial.Send(cmd)
# Initialize audio processor
audio = AudioProcessor(audio_processor)