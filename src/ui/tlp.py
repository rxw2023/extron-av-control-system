from extronlib.ui import Button, Slider
from extronlib.system import MESet
from devices import TLP1025M
# Pages
PAGE_START = 'Start_1'
PAGE_MAIN = 'Main Multi-Window_1'
PAGE_START_E = 'Start'
PAGE_MAIN_E = 'Main Multi-Window'
# Popups
POPUP_AUDIO_SETTINGS = 'Audio Settings_1'
POPUP_VIDEO_SETTINGS = 'Video Settings_1'
POPUP_HELP = 'Help_1'
POPUP_CONFIRM_POWER_OFF = 'Confirmation_1'
POPUP_CONFIRM_POWER_ON = 'Confirmation Power On_1'
POPUP_STARTING_UP = 'Starting Up_1'
POPUP_POWERING_DOWN = 'Powering Down_1'
POPUP_CAMERA = 'Camera Settings_1'
POPUP_AUDIO_SETTINGS_E = 'Audio Settings'
POPUP_VIDEO_SETTINGS_E = 'Video Settings'
POPUP_HELP_E = 'Help'
POPUP_CONFIRM_POWER_OFF_E = 'Confirmation'
POPUP_CONFIRM_POWER_ON_E = 'Confirmation Power On'
POPUP_STARTING_UP_E = 'Starting Up'
POPUP_POWERING_DOWN_E = 'Powering Down'
POPUP_CAMERA_E = 'Camera Settings'
#===== Start Page =====
BTN_START_LANGUAGE = Button(TLP1025M,153)   # Start language switch
BTN_START_LANGUAGE_E = Button(TLP1025M,8119)
BTN_START_OPEN = Button(TLP1025M,154)        # Show power on popup
BTN_START_OPEN_E = Button(TLP1025M,24)
#===== Main Page =====
BTN_HOME_LANGUAGE = Button(TLP1025M,114)      # Main page language switch
BTN_HOME_LANGUAGE_E = Button(TLP1025M,28)
BTN_HOME_CLOSE = Button(TLP1025M,115)        # Main page close popup
BTN_HOME_CLOSE_E = Button(TLP1025M,8022)
#===== Help =====
BTN_START_HELP = Button(TLP1025M,155)        # Show help on start
BTN_START_HELP_E = Button(TLP1025M,8117)
BTN_HOME_HELP = Button(TLP1025M,125)         # Show help on main page
BTN_HOME_HELP_E = Button(TLP1025M,8117)
BTN_HELP_CLOSE = Button(TLP1025M,362)        # Close help popup
BTN_HELP_CLOSE_E = Button(TLP1025M,9057)
#===== Power Control =====
BTN_POWER_ON = Button(TLP1025M,358)      # Power on confirm
BTN_POWER_ON_E = Button(TLP1025M,26)
BTN_POWER_OFF_OK = Button(TLP1025M,359)  # Close power on confirm popup
BTN_POWER_OFF_OK_E = Button(TLP1025M,27)
BTN_POWER_OFF = Button(TLP1025M,355)     # Power off confirm 
BTN_POWER_OFF_E = Button(TLP1025M,9028)
BTN_POWER_ON_OK = Button(TLP1025M,356)   # Close power off confirm popup
BTN_POWER_ON_OK_E = Button(TLP1025M,9029)
#===== LED Screen Control =====
BTN_LED_ON=Button(TLP1025M,19)    # LED on
BTN_LED_ON_E=Button(TLP1025M,8109)
BTN_LED_OFF=Button(TLP1025M,23)   # LED off
BTN_LED_OFF_E=Button(TLP1025M,1) 
#===== TV Control =====
BTN_TV_ON = Button(TLP1025M,173)    # TV on
BTN_TV_ON_E = Button(TLP1025M,167)
BTN_TV_OFF = Button(TLP1025M,174)   # TV off
BTN_TV_OFF_E = Button(TLP1025M,168)
#===== Input Source =====
BTN_PC = Button(TLP1025M,8)         # PC signal
BTN_BYOD = Button(TLP1025M,144)     # BYOD
BTN_DOC_CAM = Button(TLP1025M,96)   # Document Camera
BTN_CAMERA = Button(TLP1025M,10)    # Camera
BTN_HOME = Button(TLP1025M,7)       # Home
BTN_PC_E = Button(TLP1025M,8052)         
BTN_BYOD_E = Button(TLP1025M,2)     
BTN_DOC_CAM_E = Button(TLP1025M,8059)   
BTN_CAMERA_E = Button(TLP1025M,98)    
BTN_HOME_E = Button(TLP1025M,94)       
#===== Audio Control =====
BTN_MUTE_ALL = Button(TLP1025M,148)          # Mute all (Output Mute Ch1-4)
BTN_MUTE_ALL_E = Button(TLP1025M,110)
BTN_AUDIO_SET = Button(TLP1025M,150)         # Open audio settings popup
BTN_AUDIO_SET_E = Button(TLP1025M,112)
BTN_AUDIO_CLOSE = Button(TLP1025M,326)       # Close audio settings popup
BTN_AUDIO_CLOSE_E = Button(TLP1025M,9027)
#===== Audio Mute Buttons (Using Slider) =====
BTN_ARRAY_LOCAL_MUTE = Button(TLP1025M,120)   # Array Mic Local (Channel 1)
SLD_ARRAY_LOCAL = Slider(TLP1025M,122)        # Array Mic Local Volume Slider
BTN_ARRAY_REMOTE_MUTE = Button(TLP1025M,184)  # Array Mic Remote (Channel 2)
SLD_ARRAY_REMOTE = Slider(TLP1025M,185)       # Array Mic Remote Volume Slider
BTN_HANDHELD_MUTE = Button( TLP1025M,188)      # Handheld Mic 1 (Channel 4)
SLD_HANDHELD = Slider(TLP1025M,189)           # Handheld Mic Volume Slider 1
BTN_HANDHELD_MUTE2 = Button( TLP1025M,58)      # Handheld Mic 2 (Channel 5)
SLD_HANDHELD2 = Slider(TLP1025M,59)           # Handheld Mic Volume Slider 2
BTN_STEREO_MUTE = Button(TLP1025M,124)        # Stereo (Channel 6,7)
SLD_STEREO = Slider(TLP1025M,126)             # Stereo Volume Slider
BTN_WEBEX_MUTE = Button(TLP1025M,128)         # Webex Output (Channel 7)
SLD_WEBEX = Slider(TLP1025M,129)              # Webex Volume Slider
BTN_RECORD_MUTE = Button(TLP1025M,131)        # Recording Output (Channel 8)
SLD_RECORD = Slider(TLP1025M,132)             # Recording Volume Slider
BTN_ARRAY_LOCAL_MUTE_E = Button(TLP1025M,9017)   # Array Mic Local (Channel 1)
SLD_ARRAY_LOCAL_E = Slider(TLP1025M,9018)        # Array Mic Local Volume Slider
BTN_ARRAY_REMOTE_MUTE_E = Button(TLP1025M,191)  # Array Mic Remote (Channel 2)
SLD_ARRAY_REMOTE_E = Slider(TLP1025M,192)       # Array Mic Remote Volume Slider
BTN_HANDHELD_MUTE_E = Button( TLP1025M,194)      # Handheld Mic (Channel 4)
SLD_HANDHELD_E = Slider(TLP1025M,195)           # Handheld Mic Volume Slider
BTN_HANDHELD_MUTE2_E = Button( TLP1025M,77)      # Handheld Mic 2 (Channel 5)
SLD_HANDHELD2_E = Slider(TLP1025M,78)           # Handheld Mic Volume Slider 2
BTN_STEREO_MUTE_E = Button(TLP1025M,118)        # Stereo (Channel 6,7)
SLD_STEREO_E = Slider(TLP1025M,119)             # Stereo Volume Slider
BTN_WEBEX_MUTE_E = Button(TLP1025M,134)         # Webex Output (Channel 7)
SLD_WEBEX_E = Slider(TLP1025M,135)              # Webex Volume Slider
BTN_RECORD_MUTE_E = Button(TLP1025M,137)        # Recording Output (Channel 8)
SLD_RECORD_E = Slider(TLP1025M,138)             # Recording Volume Slider
#===== Video Settings =====
BTN_VIDEO_SET = Button(TLP1025M,87)          # Open video settings popup
BTN_VIDEO_CLOSE = Button(TLP1025M,63)        # Close video settings popup
BTN_VIDEO_SET_E = Button(TLP1025M,116)          # Open video settings popup
BTN_VIDEO_CLOSE_E = Button(TLP1025M,60)        # Close video settings popup
# Matrix Output Selection
BTN_OUT_LED = Button(TLP1025M,92)            # Output to LED
BTN_OUT_RETURN_TV = Button(TLP1025M,176)     # Output to Mirroring TV
BTN_OUT_LEFT_TV = Button(TLP1025M,177)       # Output to Left TV
BTN_OUT_RIGHT_TV = Button(TLP1025M,175)      # Output to Right TV
BTN_OUT_CAPTURE = Button(TLP1025M,86)        # Output to Capture Card
BTN_OUT_LED_E = Button(TLP1025M,43)            # Output to LED
BTN_OUT_RETURN_TV_E = Button(TLP1025M,178)     # Output to Mirroring TV
BTN_OUT_LEFT_TV_E = Button(TLP1025M,146)       # Output to Left TV
BTN_OUT_RIGHT_TV_E = Button(TLP1025M,141)      # Output to Right TV
BTN_OUT_CAPTURE_E = Button(TLP1025M,88)        # Output to Capture Card
# Matrix Input Selection
BTN_IN_DOC = Button(TLP1025M,143)            # Input from Document Camera
BTN_IN_BYOD = Button(TLP1025M,197)           # Input from BYOD
BTN_IN_PC = Button(TLP1025M,89)              # Input from PC
BTN_IN_FLOOR = Button(TLP1025M,151)          # Input from Floor Socket
BTN_IN_CAMERA = Button(TLP1025M,91)          # Input from Camera-1
BTN_IN_DOC_E = Button(TLP1025M,140)            # Input from Document Camera
BTN_IN_BYOD_E = Button(TLP1025M,196)           # Input from BYOD
BTN_IN_PC_E = Button(TLP1025M,152)              # Input from PC
BTN_IN_FLOOR_E = Button(TLP1025M,121)          # Input from Floor Socket
BTN_IN_CAMERA_E = Button(TLP1025M,142)          # Input from Camera-1
# Source selection mutual exclusion group 
mesSourceButtons = MESet([
    BTN_PC,BTN_BYOD, BTN_CAMERA, BTN_DOC_CAM
])
# LED power mutual exclusion group
mesLEDPowerButtons = MESet([BTN_LED_ON, BTN_LED_OFF])
# TV power mutual exclusion group
mesTVPowerButtons = MESet([BTN_TV_ON, BTN_TV_OFF])
# Matrix input mutual exclusion group (select 1 of 5)
mesMatrixInputButtons = MESet([
    BTN_IN_PC, BTN_IN_BYOD, BTN_IN_DOC, BTN_IN_CAMERA, BTN_IN_FLOOR
])
# Matrix output mutual exclusion group (select 1 of 5)
mesMatrixOutputButtons = MESet([
    BTN_OUT_LED, BTN_OUT_RETURN_TV, BTN_OUT_LEFT_TV, BTN_OUT_RIGHT_TV, BTN_OUT_CAPTURE
])
# Source selection mutual exclusion group 
mesSourceButtons_E= MESet([
    BTN_PC_E,BTN_BYOD_E, BTN_CAMERA_E, BTN_DOC_CAM_E
])
# LED power mutual exclusion group
mesLEDPowerButtons_E = MESet([BTN_LED_ON_E, BTN_LED_OFF_E])
# TV power mutual exclusion group
mesTVPowerButtons_E = MESet([BTN_TV_ON_E, BTN_TV_OFF_E])
# Matrix input mutual exclusion group (select 1 of 5)
mesMatrixInputButtons_E = MESet([
    BTN_IN_PC_E, BTN_IN_BYOD_E, BTN_IN_DOC_E, BTN_IN_CAMERA_E, BTN_IN_FLOOR_E
])
# Matrix output mutual exclusion group (select 1 of 5)
mesMatrixOutputButtons_E = MESet([
    BTN_OUT_LED_E, BTN_OUT_RETURN_TV_E, BTN_OUT_LEFT_TV_E, BTN_OUT_RIGHT_TV_E, BTN_OUT_CAPTURE_E
])

#===== Button Mapping for Bilingual Sync =====
# Chinese -> English button mapping
BUTTON_ZH_TO_EN = {
    # LED Power
    BTN_LED_ON: BTN_LED_ON_E,
    BTN_LED_OFF: BTN_LED_OFF_E,
    # TV Power
    BTN_TV_ON: BTN_TV_ON_E,
    BTN_TV_OFF: BTN_TV_OFF_E,
    # Source Selection
    BTN_PC: BTN_PC_E,
    BTN_BYOD: BTN_BYOD_E,
    BTN_DOC_CAM: BTN_DOC_CAM_E,
    BTN_CAMERA: BTN_CAMERA_E,
    # Matrix Input
    BTN_IN_PC: BTN_IN_PC_E,
    BTN_IN_BYOD: BTN_IN_BYOD_E,
    BTN_IN_DOC: BTN_IN_DOC_E,
    BTN_IN_CAMERA: BTN_IN_CAMERA_E,
    BTN_IN_FLOOR: BTN_IN_FLOOR_E,
    # Matrix Output
    BTN_OUT_LED: BTN_OUT_LED_E,
    BTN_OUT_RETURN_TV: BTN_OUT_RETURN_TV_E,
    BTN_OUT_LEFT_TV: BTN_OUT_LEFT_TV_E,
    BTN_OUT_RIGHT_TV: BTN_OUT_RIGHT_TV_E,
    BTN_OUT_CAPTURE: BTN_OUT_CAPTURE_E,
    # Mute All
    BTN_MUTE_ALL: BTN_MUTE_ALL_E,
    # Audio Mute Buttons
    BTN_ARRAY_LOCAL_MUTE: BTN_ARRAY_LOCAL_MUTE_E,
    BTN_ARRAY_REMOTE_MUTE: BTN_ARRAY_REMOTE_MUTE_E,
    BTN_HANDHELD_MUTE: BTN_HANDHELD_MUTE_E,
    BTN_HANDHELD_MUTE2: BTN_HANDHELD_MUTE2_E,
    BTN_STEREO_MUTE: BTN_STEREO_MUTE_E,
    BTN_WEBEX_MUTE: BTN_WEBEX_MUTE_E,
    BTN_RECORD_MUTE: BTN_RECORD_MUTE_E,
}
# English -> Chinese button mapping
BUTTON_EN_TO_ZH = {v: k for k, v in BUTTON_ZH_TO_EN.items()}

# MESet pairing for bilingual sync
MESET_ZH_TO_EN = {
    mesLEDPowerButtons: mesLEDPowerButtons_E,
    mesTVPowerButtons: mesTVPowerButtons_E,
    mesSourceButtons: mesSourceButtons_E,
    mesMatrixInputButtons: mesMatrixInputButtons_E,
    mesMatrixOutputButtons: mesMatrixOutputButtons_E,
}
MESET_EN_TO_ZH = {v: k for k, v in MESET_ZH_TO_EN.items()}
