# Matrix Input
MATRIX_INPUT_BYOD = 'BYOD'              
MATRIX_INPUT_DOC = 'DOC'                
MATRIX_INPUT_CAMERA = 'Camera'         
MATRIX_INPUT_FLOOR = 'Floor Socket'             
MATRIX_INPUT_DESKTOP = 'Desktop'           
# Matrix Output 
MATRIX_OUTPUT_LED = 'LED'                   
MATRIX_OUTPUT_RECORDER = 'luobo'        
MATRIX_OUTPUT_RETURN_TV = 'Mirroring TV'    
MATRIX_OUTPUT_LEFT_TV = 'Left TV'           
MATRIX_OUTPUT_RIGHT_TV = 'Right TV'          
MATRIX_OUTPUT_CAPTURE = 'CAIji'              
# Power Sequencer Switch Commands
POWER_SEQUENCER_ON = b'\x48\x1A\x00\x01\x02\x00\x00\x4D'    
POWER_SEQUENCER_OFF = b'\x48\x1A\x00\x01\x01\x00\x00\x4D'  
# Philips TV Switch Commands 
TV_POWER_ON = b'\x06\x01\x00\x18\x02\x1D'     
TV_POWER_OFF = b'\x06\x01\x00\x18\x01\x1E'    
# Environmental Sensor Read Command
ENVIRONMENTAL_SENSOR_READ = b'\x01\x03\x00\x00\x00\x08\x44\x0C'     
 
