from extronlib.device import ProcessorDevice, UIDevice
from extronlib.interface import SerialInterface,RelayInterface,EthernetClientInterface
import modules.device.vsca_camera_Visca_v1_0_1_2
import modules.device.extr_sm_SMP_300_Series_v1_19_20_0 
# Controller devices
IPCP = ProcessorDevice('IPCP350')
IPL = ProcessorDevice('IPLS3')   
TLP1025M = UIDevice('TLP1025M')        
# IPCP devices
video_matrix = SerialInterface(IPCP,'COM1',9600,8,'None',1,'Off',0,'RS232')
power_sequencer = SerialInterface(IPCP,'COM2',9600,8,'None',1,'Off',0,'RS232')               
recording_system = modules.device.extr_sm_SMP_300_Series_v1_19_20_0.SerialClass(IPCP,'COM3',Model='SMP 351')
byod_switcher = SerialInterface(IPCP,'IRS1',9600,8,'None',1,'Off',0,'RS232')
tv_3 = SerialInterface(IPCP,'IRS2',9600,8,'None',1,'Off',0,'RS232')
relay_led = RelayInterface(IPCP, 'RLY1')
# IPL devices
tv_1 = SerialInterface(IPL,'COM1',9600,8,'None',1,'Off',0,'RS232')
tv_2 = SerialInterface(IPL,'COM2',9600,8,'None',1,'Off',0,'RS232')
audio_processor = SerialInterface(IPL,'COM3',9600,8,'None',1,'Off',0,'RS232')
# Extended serial devices
sensor = EthernetClientInterface("10.109.77.169",8002)
# Camera devices
tracking_camera = modules.device.vsca_camera_Visca_v1_0_1_2.SerialOverEthernetClass("10.109.74.205",1259,'UDP')






