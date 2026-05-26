from extronlib import Platform,Version
import devices as dev
import ui.tlp as tlp
from extronlib.system import Wait
from extronlib import event
import variables as vars
import control.av as av
import modules.project.thingsboard_power as thingsboard_power
import modules.project.thingsboard_sensor as thingsboard_sensor
import modules.project.thingsboard_LED as thingsboard_LED
import modules.project.thingsboard_TV as thingsboard_TV 
import modules.project.martix as martix
import time
# Global variables
current_language = 'zh'
sensor_connected = False
matrixInputState = 'PC' 
sensor_rx_buffer = b''   
sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "co2": 0,
    "tvoc": 0,
    "ch2o": 0,
    "pm2_5": 0,
    "pm10": 0,
    "pm1_0": 0
}
def sensor_start_poll():
    global sensor_connected
    try:
        if not sensor_connected:
            dev.sensor.Connect()
            sensor_connected = True
        dev.sensor.Send(vars.ENVIRONMENTAL_SENSOR_READ)
    except Exception as e:
        print('Abnormal sensor polling:', e)
        sensor_connected = False
    Wait(5, sensor_start_poll)
@event(dev.sensor, 'Connected')
def OnSensorConnected(interface, state):
    global sensor_connected
    sensor_connected = True
    print('Sensor connected')
@event(dev.sensor, 'Disconnected')
def OnSensorDisconnected(interface, state):
    global sensor_connected
    sensor_connected = False
    print('Sensor disconnected, preparing to reconnect...')
    try:
        dev.sensor.Connect()
    except:
        pass
@event(dev.sensor, 'ReceiveData')
def OnSensorData(interface, data):
    global sensor_rx_buffer, sensor_data
    sensor_rx_buffer += data
    while len(sensor_rx_buffer) >= 21:
        # Find frame header 01 03
        head = sensor_rx_buffer.find(b'\x01\x03')
        if head == -1:
            # Frame header not found, clear dirty data
            sensor_rx_buffer = b''
            return
        if head > 0:
            # Remove leading dirty data, start from frame header
            sensor_rx_buffer = sensor_rx_buffer[head:]
        if len(sensor_rx_buffer) < 21:
            return
        # Extract one frame
        frame = sensor_rx_buffer[:21]
        sensor_rx_buffer = sensor_rx_buffer[21:]
        try:
            co2     = frame[3] * 256 + frame[4]
            tvoc    = frame[5] * 256 + frame[6]
            ch2o    = frame[7] * 256 + frame[8]
            pm25    = frame[9] * 256 + frame[10]
            humi    = (frame[11] * 256 + frame[12]) / 100.0
            temp_raw= frame[13] * 256 + frame[14]
            pm10    = frame[15] * 256 + frame[16]
            pm1_0   = frame[17] * 256 + frame[18]
            if temp_raw > 32767:
                temp_raw -= 65536
            temp = temp_raw / 100.0
            sensor_data["co2"] = co2
            sensor_data["tvoc"] = tvoc
            sensor_data["ch2o"] = ch2o
            sensor_data["pm2_5"] = pm25
            sensor_data["humidity"] = round(humi, 2)
            sensor_data["temperature"] = round(temp, 2)
            sensor_data["pm10"] = pm10
            sensor_data["pm1_0"] = pm1_0
            # print("=== Sensor Data ===")
            # print("Temperature: %.2f \u2103" % sensor_data["temperature"])
            # print("Humidity: %.2f %%RH" % sensor_data["humidity"])
            # print("CO2: %d ppm" % sensor_data["co2"])
            # print("TVOC: %d ppb" % sensor_data["tvoc"])
            # print("CH2O: %d µg/m³" % sensor_data["ch2o"])
            # print("PM2.5: %d µg/m³" % sensor_data["pm2_5"])
            # print("PM10: %d µg/m³" % sensor_data["pm10"])
            # print("PM1.0: %d µg/m³" % sensor_data["pm1_0"])
            thingsboard_sensor.send_telemetry(sensor_data)
        except:
            pass
#================= Bilingual Button Sync Helper =================
def _sync_button_state(btn, state):
    """Sync button state to the other language's corresponding button and MESet"""
    if btn in tlp.BUTTON_ZH_TO_EN:
        target_btn = tlp.BUTTON_ZH_TO_EN[btn]
        target_meset = None
        for zh_me, en_me in tlp.MESET_ZH_TO_EN.items():
            if btn in zh_me.Objects:
                target_meset = en_me
                break
        if target_btn:
            target_btn.SetState(state)
        if target_meset:
            target_meset.SetCurrent(target_btn)
    elif btn in tlp.BUTTON_EN_TO_ZH:
        target_btn = tlp.BUTTON_EN_TO_ZH[btn]
        target_meset = None
        for en_me, zh_me in tlp.MESET_EN_TO_ZH.items():
            if btn in en_me.Objects:
                target_meset = zh_me
                break
        if target_btn:
            target_btn.SetState(state)
        if target_meset:
            target_meset.SetCurrent(target_btn)
#================= Language Switch =================
@event([tlp.BTN_START_LANGUAGE, tlp.BTN_START_LANGUAGE_E, tlp.BTN_HOME_LANGUAGE, tlp.BTN_HOME_LANGUAGE_E], 'Pressed')
def OnLanguageSwitch(btn, state):
    global current_language
    if current_language == 'zh':
        current_language = 'en'
        # Currently on Chinese page, switch to English version
        if btn == tlp.BTN_START_LANGUAGE:
            dev.TLP1025M.ShowPage(tlp.PAGE_START_E)
        elif btn == tlp.BTN_HOME_LANGUAGE:
            dev.TLP1025M.ShowPage(tlp.PAGE_MAIN_E)
        print('Language switched to English')
    else:
        current_language = 'zh'
        # Currently on English page, switch to Chinese version
        if btn == tlp.BTN_START_LANGUAGE_E:
            dev.TLP1025M.ShowPage(tlp.PAGE_START)
        elif btn == tlp.BTN_HOME_LANGUAGE_E:
            dev.TLP1025M.ShowPage(tlp.PAGE_MAIN)
        print('Language switched to Chinese')
#===================== Chinese Version ===================#
@event(tlp.BTN_START_HELP, 'Pressed')
def OnStartHelpPressed(btn,state):
    """Start / Help Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_HELP)
@event(tlp.BTN_HOME_HELP, 'Pressed')
def OnHomeHelpPressed(btn,state):
    """Main / Help Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_HELP)
@event(tlp.BTN_HELP_CLOSE, 'Pressed')
def OnHelpClosePressed(btn,state):
    """Main / Hide Help Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_HELP)
#=============================================#
@event(tlp.BTN_START_OPEN, 'Pressed')
def OnStartOpenPressed(btn,state):
    """Start / Power On Confirmation Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_CONFIRM_POWER_ON)
@event(tlp.BTN_POWER_ON, 'Pressed')
def OnPowerOnPressed(btn,state):
    dev.power_sequencer.Send(vars.POWER_SEQUENCER_ON)
    dev.relay_led.SetState(1)
    dev.TLP1025M.ShowPopup(tlp.POPUP_STARTING_UP)
    time.sleep(12)
    time.sleep(1)
    time.sleep(1)
    dev.tv_1.Send(vars.TV_POWER_ON)
    time.sleep(1)
    dev.tv_2.Send(vars.TV_POWER_ON)
    time.sleep(1)
    dev.tv_3.Send(vars.TV_POWER_ON)
    dev.TLP1025M.HideAllPopups()
    dev.TLP1025M.ShowPage(tlp.PAGE_MAIN)
    dev.tracking_camera.Set('Power','On')
    thingsboard_power.send_event({"Power Status": "On"})
    thingsboard_LED.send_event({"LED Screen Status":"On"})
    thingsboard_TV.send_event({"TV Status":"On"})
    
    print('audio initializing')
    av.audio.recall_preset(1)
    time.sleep(4)

    tlp.SLD_ARRAY_LOCAL.SetFill(-10)
    tlp.SLD_ARRAY_LOCAL_E.SetFill(-10)

    tlp.SLD_ARRAY_REMOTE.SetFill(-8)
    tlp.SLD_ARRAY_REMOTE_E.SetFill(-8)

    tlp.SLD_HANDHELD.SetFill(0)
    tlp.SLD_HANDHELD_E.SetFill(0)

    tlp.SLD_HANDHELD2.SetFill(0)
    tlp.SLD_HANDHELD2_E.SetFill(0)
    
    tlp.SLD_STEREO.SetFill(4.5)
    tlp.SLD_STEREO_E.SetFill(4.5)

    tlp.SLD_WEBEX.SetFill(-3)
    tlp.SLD_WEBEX_E.SetFill(-3)

    tlp.SLD_RECORD.SetFill(-4.5)
    tlp.SLD_RECORD_E.SetFill(-4.5)

    time.sleep(1.6)
    time.sleep(8)
    dev.recording_system.Set('Record','Start')
    dev.recording_system.Set('RTMPStream','Enable', {'Stream': 'Archive B'})
@event(tlp.BTN_POWER_OFF_OK, 'Pressed')
def OnPowerOffOkPressed(btn,state):
    """Start / Hide Power On Confirmation Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_CONFIRM_POWER_ON)
#=============================================#
@event(tlp.BTN_HOME_CLOSE,'Pressed')
def OnHomeClosePressed(btn,state):
    """Main / Power Off Confirmation Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_CONFIRM_POWER_OFF)
@event(tlp.BTN_POWER_OFF,'Pressed')
def OnPowerOffPressed(btn,state):
    dev.relay_led.SetState(0)
    time.sleep(1)
    dev.tv_1.Send(vars.TV_POWER_OFF)
    time.sleep(1)
    dev.tv_2.Send(vars.TV_POWER_OFF)
    time.sleep(1)
    dev.tv_3.Send(vars.TV_POWER_OFF)
    dev.recording_system.Set('Record','Stop')
    dev.recording_system.Set('RTMPStream','Disable', {'Stream': 'Archive B'})
    dev.power_sequencer.Send(vars.POWER_SEQUENCER_OFF)
    dev.TLP1025M.ShowPopup(tlp.POPUP_POWERING_DOWN)
    time.sleep(15)
    dev.TLP1025M.HideAllPopups()
    dev.TLP1025M.ShowPage(tlp.PAGE_START)
    dev.tracking_camera.Set('Power','Off')
    thingsboard_LED.send_event({"LED Screen Status":"Off"})
    thingsboard_TV.send_event({"TV Status":"Off"})
    thingsboard_power.send_event({"Power Status": "Off"})
@event(tlp.BTN_POWER_ON_OK,'Pressed')
def OnPowerOffOkPressed(btn,state):
    """Main / Hide Power Off Confirmation Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_CONFIRM_POWER_OFF)
#=============================================#
@event(tlp.mesLEDPowerButtons.Objects,'Pressed')
def OnLEDPowerPressed(btn, state):
    for b in tlp.mesLEDPowerButtons.Objects:
        b.SetState(0)
    """LED Power Button"""
    if btn == tlp.BTN_LED_ON:
        btn.SetState(1)
        dev.relay_led.SetState(1)
        thingsboard_LED.send_event({"LED Screen Status":"On"})
        pass
    elif btn == tlp.BTN_LED_OFF:
        btn.SetState(1)
        dev.relay_led.SetState(0)
        thingsboard_LED.send_event({"LED Screen Status":"Off"})
        pass
    """Set Current Button as Active in MESet"""
    tlp.mesLEDPowerButtons.SetCurrent(btn)
    _sync_button_state(btn, 1)
#=============================================#
@event(tlp.mesTVPowerButtons.Objects, 'Pressed')
def OnTVPowerPressed(btn, state):
    for b in tlp.mesTVPowerButtons.Objects:
        b.SetState(0)
    """TV Power Button"""
    if btn == tlp.BTN_TV_ON:
        btn.SetState(1)
        time.sleep(1)
        dev.tv_1.Send(vars.TV_POWER_ON)
        time.sleep(1)
        dev.tv_2.Send(vars.TV_POWER_ON)
        time.sleep(1)
        dev.tv_3.Send(vars.TV_POWER_ON)
        thingsboard_TV.send_event({"TV Status":"On"})
    elif btn == tlp.BTN_TV_OFF:
        btn.SetState(1)
        time.sleep(1)
        dev.tv_1.Send(vars.TV_POWER_OFF)
        time.sleep(1)
        dev.tv_2.Send(vars.TV_POWER_OFF)
        time.sleep(1)
        dev.tv_3.Send(vars.TV_POWER_OFF)
        thingsboard_TV.send_event({"TV Status":"Off"})
    tlp.mesTVPowerButtons.SetCurrent(btn)
    _sync_button_state(btn, 1)
#=============================================#
@event(tlp.BTN_HOME,'Pressed')
def OnHomePressed(btn,state):
     """Return to Main Page"""
     dev.TLP1025M.HideAllPopups()
#=============================================#
@event(tlp.mesSourceButtons.Objects, 'Pressed')
def OnSourcePressed(btn, state):
    for b in tlp.mesSourceButtons.Objects:
        b.SetState(0)
    """Source Switching Logic"""
    if btn == tlp.BTN_PC:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_RECORDER)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_CAPTURE)
        martix.send_event({"Current Input Source":"Desktop Signal"})
        pass
    elif btn == tlp.BTN_BYOD:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_RECORDER)
        martix.send_event({"Current Input Source":"Wireless Screen Casting"})
        pass
    elif btn == tlp.BTN_DOC_CAM:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_RECORDER)
        martix.send_event({"Current Input Source":"Document Camera"})
        pass
    elif btn == tlp.BTN_CAMERA:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_CAPTURE)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_RECORDER)
        martix.send_event({"Current Input Source":"Monitor Signal"})
        pass
    tlp.mesSourceButtons.SetCurrent(btn)
    _sync_button_state(btn, 1)
#=============================================#
@event(tlp.BTN_VIDEO_SET,'Pressed')
def OnVideoSetPressed(btn, state):
    """Open Video Settings Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_VIDEO_SETTINGS)
@event(tlp.BTN_VIDEO_CLOSE,'Pressed')
def OnVideoClosePressed(btn,state):
    """Close Video Settings Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_VIDEO_SETTINGS)
@event(tlp.BTN_AUDIO_SET,'Pressed')
def OnAudioSetPressed(btn,state):
    """Open Audio Settings Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_AUDIO_SETTINGS)
@event(tlp.BTN_AUDIO_CLOSE,'Pressed')
def OnAudioClosePressed(btn,state):
    """Close Audio Settings Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_AUDIO_SETTINGS)
#================ Matrix Routing Select Input Source =============#
@event(tlp.mesMatrixInputButtons.Objects, 'Pressed')
def OnInputSourcePressed(btn, state):
    for b in tlp.mesMatrixInputButtons.Objects:
        b.SetState(0)
    global matrixInputState  
    """Update Input Source State by Button"""
    if btn == tlp.BTN_IN_PC:
        btn.SetState(1)
        matrixInputState = 'PC'
    elif btn == tlp.BTN_IN_BYOD:
        btn.SetState(1)
        matrixInputState = 'BYOD'
    elif btn == tlp.BTN_IN_DOC:
        btn.SetState(1)
        matrixInputState = 'DOC'
    elif btn == tlp.BTN_IN_CAMERA:
        btn.SetState(1)
        matrixInputState = 'CAMERA'
    elif btn == tlp.BTN_IN_FLOOR:
        btn.SetState(1)
        matrixInputState = 'FLOOR'
    """Set Current Button as Active in MESet"""
    tlp.mesMatrixInputButtons.SetCurrent(btn)
    _sync_button_state(btn, 1)
#================ Matrix Routing Select Output Source =============#
@event(tlp.mesMatrixOutputButtons.Objects, 'Pressed')
def OnOutputTargetPressed(btn, state):
    for b in tlp.mesMatrixOutputButtons.Objects:
        b.SetState(0)
    input_var = None
    if matrixInputState == 'PC':
        input_var = vars.MATRIX_INPUT_DESKTOP
    elif matrixInputState == 'BYOD':
        input_var = vars.MATRIX_INPUT_BYOD
    elif matrixInputState == 'DOC':
        input_var = vars.MATRIX_INPUT_DOC
    elif matrixInputState == 'CAMERA':
        input_var = vars.MATRIX_INPUT_CAMERA
    elif matrixInputState == 'FLOOR':
        input_var = vars.MATRIX_INPUT_FLOOR
    """Execute Matrix Tie by Button"""
    if input_var is not None:
        if btn == tlp.BTN_OUT_LED:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_LED)
            pass
        elif btn == tlp.BTN_OUT_RETURN_TV:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_RETURN_TV)
            pass
        elif btn == tlp.BTN_OUT_LEFT_TV:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_LEFT_TV)
            pass
        elif btn == tlp.BTN_OUT_RIGHT_TV:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_RIGHT_TV)
            pass
        elif btn == tlp.BTN_OUT_CAPTURE:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_CAPTURE)
            pass
    """Set Current Button as Active in MESet"""
    tlp.mesMatrixOutputButtons.SetCurrent(btn)
    _sync_button_state(btn, 1)
#================ Mute =============#
@event(tlp.BTN_MUTE_ALL,'Pressed')
def mute(btn,state):
    current_mute = av.audio.get_output_mute(1)  
    new_state = 'Off' if current_mute == 'On' else 'On'
    av.audio.set_output_mute(1, new_state)
    av.audio.set_output_mute(2, new_state)
    av.audio.set_output_mute(3, new_state)
    av.audio.set_output_mute(4, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
#===================== Array Mic Local (Channel 1) =====================
tlp.SLD_ARRAY_LOCAL.SetRange(-36.0,-8.0,0.1)  
@event(tlp.SLD_ARRAY_LOCAL, 'Changed')
def sld_array_local_change(slider, state, val):
    slider.SetFill(val)  # Show fill
    av.audio.set_input_volume(1, val)
@event(tlp.BTN_ARRAY_LOCAL_MUTE, 'Pressed')
def btn_array_local_mute_press(btn, state):
    current = av.audio.get_input_mute(1)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(1, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_ARRAY_LOCAL, 'Released')
def sld_array_local_mute_release(slider, state, val):
    av.audio.set_input_mute(1, 'Off')
    slider.SetFill(val)
#===================== Array Mic Remote (Channel 2) =====================
tlp.SLD_ARRAY_REMOTE.SetRange(-36.0,-10.0,0.1)
@event(tlp.SLD_ARRAY_REMOTE, 'Changed')
def sld_array_remote_change(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(2, val)
@event(tlp.BTN_ARRAY_REMOTE_MUTE, 'Pressed')
def btn_array_remote_mute_press(btn, state):
    current = av.audio.get_input_mute(2)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(2, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_ARRAY_REMOTE, 'Released')
def sld_array_remote_mute_release(slider, state, val):
    av.audio.set_input_mute(2, 'Off')
    slider.SetFill(val)
#===================== Handheld Mic (Channel 4) =====================
tlp.SLD_HANDHELD.SetRange(-36.0,0.0,0.1)
@event(tlp.SLD_HANDHELD, 'Changed')
def sld_handheld_change(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(4, val)
@event(tlp.BTN_HANDHELD_MUTE, 'Pressed')
def btn_handheld_mute_press(btn, state):
    current = av.audio.get_input_mute(4)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(4, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_HANDHELD, 'Released')
def sld_handheld_mute_release(slider, state, val):
    av.audio.set_input_mute(4, 'Off')
    slider.SetFill(val)
#===================== Handheld Mic 2 (Channel 5) =====================
tlp.SLD_HANDHELD2.SetRange(-36.0,0.0,0.1)
@event(tlp.SLD_HANDHELD2, 'Changed')
def sld_handheld2_change(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(5, val)
@event(tlp.BTN_HANDHELD_MUTE2, 'Pressed')
def btn_handheld_mute2_press(btn, state):
    current = av.audio.get_input_mute(5)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(5, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_HANDHELD2, 'Released')
def sld_handheld_mute2_release(slider, state, val):
    av.audio.set_input_mute(5, 'Off')
    slider.SetFill(val)
#===================== Stereo (Channel 6+7 Linked) =====================
tlp.SLD_STEREO.SetRange(-36.0,6.0,0.1)
@event(tlp.SLD_STEREO, 'Changed')
def sld_stereo_change(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(6, val)
    av.audio.set_input_volume(7, val)
@event(tlp.BTN_STEREO_MUTE, 'Pressed')
def btn_stereo_mute_press(btn, state):
    current = av.audio.get_input_mute(6)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(6, new_state)
    av.audio.set_input_mute(7, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_STEREO, 'Released')
def sld_stereo_mute_release(slider, state, val):
    av.audio.set_input_mute(6, 'Off')
    av.audio.set_input_mute(7, 'Off')
    slider.SetFill(val)
#===================== Webex Output (Channel 7) =====================
tlp.SLD_WEBEX.SetRange(-36.0,6.0,0.1)
@event(tlp.SLD_WEBEX, 'Changed')
def sld_webex_change(slider, state, val):
    slider.SetFill(val)
    av.audio.set_output_volume(7, val)
@event(tlp.BTN_WEBEX_MUTE, 'Pressed')
def btn_webex_mute_press(btn, state):
    current = av.audio.get_output_mute(7)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_output_mute(7, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_WEBEX, 'Released')
def sld_webex_mute_release(slider, state, val):
    av.audio.set_output_mute(7, 'Off')
    slider.SetFill(val)
#==================== Recording Output (Channel 8) =====================
tlp.SLD_RECORD.SetRange(-36.0,6.0,0.1)
@event(tlp.SLD_RECORD, 'Changed')
def sld_record_change(slider, state, val):
    slider.SetFill(val)
    av.audio.set_output_volume(8, val)
@event(tlp.BTN_RECORD_MUTE, 'Pressed')
def btn_record_mute_press(btn, state):
    current = av.audio.get_output_mute(8)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_output_mute(8, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_RECORD, 'Released')
def sld_record_mute_release(slider, state, val):
    av.audio.set_output_mute(8, 'Off')
    slider.SetFill(val)
#===================== English Version ===================#
@event(tlp.BTN_START_HELP_E, 'Pressed')
def OnStartHelpPressed_EN(btn,state):
    """Start / Help Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_HELP_E)
@event(tlp.BTN_HOME_HELP_E, 'Pressed')
def OnHomeHelpPressed_EN(btn,state):
    """Main / Help Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_HELP_E)
@event(tlp.BTN_HELP_CLOSE_E, 'Pressed')
def OnHelpClosePressed_EN(btn,state):
    """Main / Hide Help Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_HELP_E)
#=============================================#
@event(tlp.BTN_START_OPEN_E, 'Pressed')
def OnStartOpenPressed_EN(btn,state):
    """Start / Power On Confirmation Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_CONFIRM_POWER_ON_E)
@event(tlp.BTN_POWER_ON_E, 'Pressed')
def OnPowerOnPressed_EN(btn,state):
    dev.power_sequencer.Send(vars.POWER_SEQUENCER_ON)
    dev.relay_led.SetState(1)
    dev.TLP1025M.ShowPopup(tlp.POPUP_STARTING_UP_E)
    time.sleep(12)
    time.sleep(1)
    time.sleep(1)
    dev.tv_1.Send(vars.TV_POWER_ON)
    time.sleep(1)
    dev.tv_2.Send(vars.TV_POWER_ON)
    time.sleep(1)
    dev.tv_3.Send(vars.TV_POWER_ON)    
    dev.TLP1025M.HideAllPopups()
    dev.TLP1025M.ShowPage(tlp.PAGE_MAIN_E)
    dev.tracking_camera.Set('Power','On')
    thingsboard_power.send_event({"Power Status": "On"})
    thingsboard_LED.send_event({"LED Screen Status":"On"})
    thingsboard_TV.send_event({"TV Status":"On"})

    print('audio initializing')
    av.audio.recall_preset(1)
    time.sleep(4)

    tlp.SLD_ARRAY_LOCAL.SetFill(-10)
    tlp.SLD_ARRAY_LOCAL_E.SetFill(-10)

    tlp.SLD_ARRAY_REMOTE.SetFill(-8)
    tlp.SLD_ARRAY_REMOTE_E.SetFill(-8)

    tlp.SLD_HANDHELD.SetFill(0)
    tlp.SLD_HANDHELD_E.SetFill(0)

    tlp.SLD_HANDHELD2.SetFill(0)
    tlp.SLD_HANDHELD2_E.SetFill(0)
    
    tlp.SLD_STEREO.SetFill(4.5)
    tlp.SLD_STEREO_E.SetFill(4.5)

    tlp.SLD_WEBEX.SetFill(-3)
    tlp.SLD_WEBEX_E.SetFill(-3)

    tlp.SLD_RECORD.SetFill(-4.5)
    tlp.SLD_RECORD_E.SetFill(-4.5)

    time.sleep(1.6)
    time.sleep(8)
    dev.recording_system.Set('Record','Start')
    dev.recording_system.Set('RTMPStream','Enable', {'Stream': 'Archive B'})
@event(tlp.BTN_POWER_OFF_OK_E, 'Pressed')
def OnPowerOffOkPressed_EN(btn,state):
    """Start / Hide Power On Confirmation Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_CONFIRM_POWER_ON_E)
#=============================================#
@event(tlp.BTN_HOME_CLOSE_E,'Pressed')
def OnHomeClosePressed_EN(btn,state):
    """Main / Power Off Confirmation Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_CONFIRM_POWER_OFF_E)
@event(tlp.BTN_POWER_OFF_E,'Pressed')
def OnPowerOffPressed_EN(btn,state):
    dev.relay_led.SetState(0)
    time.sleep(1)
    dev.tv_1.Send(vars.TV_POWER_OFF)
    time.sleep(1)
    dev.tv_2.Send(vars.TV_POWER_OFF)
    time.sleep(1)
    dev.tv_3.Send(vars.TV_POWER_OFF)
    dev.recording_system.Set('Record','Stop')
    dev.recording_system.Set('RTMPStream','Disable', {'Stream': 'Archive B'})
    dev.power_sequencer.Send(vars.POWER_SEQUENCER_OFF)
    dev.TLP1025M.ShowPopup(tlp.POPUP_POWERING_DOWN_E)
    time.sleep(15)
    dev.tracking_camera.Set('Power','Off')
    dev.TLP1025M.HideAllPopups()
    dev.TLP1025M.ShowPage(tlp.PAGE_START)
    thingsboard_LED.send_event({"LED Screen Status":"Off"})
    thingsboard_TV.send_event({"TV Status":"Off"})
    thingsboard_power.send_event({"Power Status": "Off"})
@event(tlp.BTN_POWER_ON_OK_E,'Pressed')
def OnPowerOffOkPressed_EN(btn,state):
    """Main / Hide Power Off Confirmation Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_CONFIRM_POWER_OFF_E)
#=============================================#
@event(tlp.mesLEDPowerButtons_E.Objects,'Pressed')
def OnLEDPowerPressed_EN(btn, state):
    for b in tlp.mesLEDPowerButtons_E.Objects:
        b.SetState(0)
    """LED Power Button"""
    if btn == tlp.BTN_LED_ON_E:
        btn.SetState(1)
        dev.relay_led.SetState(1)
        thingsboard_LED.send_event({"LED Screen Status":"On"})
        pass
    elif btn == tlp.BTN_LED_OFF_E:
        btn.SetState(1)
        dev.relay_led.SetState(0)
        thingsboard_LED.send_event({"LED Screen Status":"Off"})
        pass
    """Set Current Button as Active in MESet"""
    tlp.mesLEDPowerButtons_E.SetCurrent(btn)
    _sync_button_state(btn, 1)
#=============================================#
@event(tlp.mesTVPowerButtons_E.Objects, 'Pressed')
def OnTVPowerPressed_EN(btn, state):
    for b in tlp.mesTVPowerButtons_E.Objects:
        b.SetState(0)
    """TV Power Button"""
    if btn == tlp.BTN_TV_ON_E:
        btn.SetState(1)
        time.sleep(1)
        dev.tv_1.Send(vars.TV_POWER_ON)
        time.sleep(1)
        dev.tv_2.Send(vars.TV_POWER_ON)
        time.sleep(1)
        dev.tv_3.Send(vars.TV_POWER_ON)
        thingsboard_TV.send_event({"TV Status":"On"})
    elif btn == tlp.BTN_TV_OFF_E:
        btn.SetState(1)
        time.sleep(1)
        dev.tv_1.Send(vars.TV_POWER_OFF)
        time.sleep(1)
        dev.tv_2.Send(vars.TV_POWER_OFF)
        time.sleep(1)
        dev.tv_3.Send(vars.TV_POWER_OFF)
        thingsboard_TV.send_event({"TV Status":"Off"})
    tlp.mesTVPowerButtons_E.SetCurrent(btn)
    _sync_button_state(btn, 1)
#=============================================#
@event(tlp.BTN_HOME_E,'Pressed')
def OnHomePressed_EN(btn,state):
     """Return to Main Page"""
     dev.TLP1025M.HideAllPopups()
#=============================================#
@event(tlp.mesSourceButtons_E.Objects, 'Pressed')
def OnSourcePressed_EN(btn, state):
    for b in tlp.mesSourceButtons_E.Objects:
        b.SetState(0)
    """Source Switching Logic"""
    if btn == tlp.BTN_PC_E:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_RECORDER)
        av.matrix_tie(vars.MATRIX_INPUT_DESKTOP, vars.MATRIX_OUTPUT_CAPTURE)
        martix.send_event({"Current Input Source":"Desktop Signal"})
        pass
    elif btn == tlp.BTN_BYOD_E:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_BYOD, vars.MATRIX_OUTPUT_RECORDER)
        martix.send_event({"Current Input Source":"Wireless Screen Casting"})
        pass
    elif btn == tlp.BTN_DOC_CAM_E:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_DOC, vars.MATRIX_OUTPUT_RECORDER)
        martix.send_event({"Current Input Source":"Document Camera"})
        pass
    elif btn == tlp.BTN_CAMERA_E:
        btn.SetState(1)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_CAPTURE)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_LED)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_RETURN_TV)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_LEFT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_RIGHT_TV)
        av.matrix_tie(vars.MATRIX_INPUT_CAMERA, vars.MATRIX_OUTPUT_RECORDER)
        martix.send_event({"Current Input Source":"Monitor Signal"})
        pass
    tlp.mesSourceButtons_E.SetCurrent(btn)
    _sync_button_state(btn, 1)
#=============================================#
@event(tlp.BTN_VIDEO_SET_E,'Pressed')
def OnVideoSetPressed_EN(btn, state):
    """Open Video Settings Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_VIDEO_SETTINGS_E)
@event(tlp.BTN_VIDEO_CLOSE_E,'Pressed')
def OnVideoClosePressed_EN(btn,state):
    """Close Video Settings Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_VIDEO_SETTINGS_E)
@event(tlp.BTN_AUDIO_SET_E,'Pressed')
def OnAudioSetPressed_EN(btn,state):
    """Open Audio Settings Popup"""
    dev.TLP1025M.ShowPopup(tlp.POPUP_AUDIO_SETTINGS_E)
@event(tlp.BTN_AUDIO_CLOSE_E,'Pressed')
def OnAudioClosePressed_EN(btn,state):
    """Close Audio Settings Popup"""
    dev.TLP1025M.HidePopup(tlp.POPUP_AUDIO_SETTINGS_E)
#================ Matrix Routing Select Input Source =============#
@event(tlp.mesMatrixInputButtons_E.Objects, 'Pressed')
def OnInputSourcePressed_EN(btn, state):
    for b in tlp.mesMatrixInputButtons_E.Objects:
        b.SetState(0)
    global matrixInputState  
    """Update Input Source State by Button"""
    if btn == tlp.BTN_IN_PC_E:
        btn.SetState(1)
        matrixInputState = 'PC'
    elif btn == tlp.BTN_IN_BYOD_E:
        btn.SetState(1)
        matrixInputState = 'BYOD'
    elif btn == tlp.BTN_IN_DOC_E:
        btn.SetState(1)
        matrixInputState = 'DOC'
    elif btn == tlp.BTN_IN_CAMERA_E:
        btn.SetState(1)
        matrixInputState = 'CAMERA'
    elif btn == tlp.BTN_IN_FLOOR_E:
        btn.SetState(1)
        matrixInputState = 'FLOOR'
    """Set Current Button as Active in MESet"""
    tlp.mesMatrixInputButtons_E.SetCurrent(btn)
    _sync_button_state(btn, 1)
#================ Matrix Routing Select Output Source =============#
@event(tlp.mesMatrixOutputButtons_E.Objects, 'Pressed')
def OnOutputTargetPressed_EN(btn, state):
    for b in tlp.mesMatrixOutputButtons_E.Objects:
        b.SetState(0)
    input_var = None
    if matrixInputState == 'PC':
        input_var = vars.MATRIX_INPUT_DESKTOP
    elif matrixInputState == 'BYOD':
        input_var = vars.MATRIX_INPUT_BYOD
    elif matrixInputState == 'DOC':
        input_var = vars.MATRIX_INPUT_DOC
    elif matrixInputState == 'CAMERA':
        input_var = vars.MATRIX_INPUT_CAMERA
    elif matrixInputState == 'FLOOR':
        input_var = vars.MATRIX_INPUT_FLOOR
    """Execute Matrix Tie by Button"""
    if input_var is not None:
        if btn == tlp.BTN_OUT_LED_E:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_LED)
            pass
        elif btn == tlp.BTN_OUT_RETURN_TV_E:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_RETURN_TV)
            pass
        elif btn == tlp.BTN_OUT_LEFT_TV_E:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_LEFT_TV)
            pass
        elif btn == tlp.BTN_OUT_RIGHT_TV_E:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_RIGHT_TV)
            pass
        elif btn == tlp.BTN_OUT_CAPTURE_E:
            btn.SetState(1)
            av.matrix_tie(input_var, vars.MATRIX_OUTPUT_CAPTURE)
            pass
    """Set Current Button as Active in MESet"""
    tlp.mesMatrixOutputButtons_E.SetCurrent(btn)
    _sync_button_state(btn, 1)
#================ Mute =============#
@event(tlp.BTN_MUTE_ALL_E,'Pressed')
def mute_EN(btn,state):
    current_mute = av.audio.get_output_mute(1)  
    new_state = 'Off' if current_mute == 'On' else 'On'
    av.audio.set_output_mute(1, new_state)
    av.audio.set_output_mute(2, new_state)
    av.audio.set_output_mute(3, new_state)
    av.audio.set_output_mute(4, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
#===================== Array Mic Local (Channel 1) =====================
tlp.SLD_ARRAY_LOCAL_E.SetRange(-36.0,-8.0,0.1)  
@event(tlp.SLD_ARRAY_LOCAL_E, 'Changed')
def sld_array_local_change_EN(slider, state, val):
    slider.SetFill(val)  # Show fill
    av.audio.set_input_volume(1, val)
@event(tlp.BTN_ARRAY_LOCAL_MUTE_E, 'Pressed')
def btn_array_local_mute_press_EN(btn, state):
    current = av.audio.get_input_mute(1)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(1, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_ARRAY_LOCAL_E, 'Released')
def sld_array_local_mute_release_EN(slider, state, val):
    av.audio.set_input_mute(1, 'Off')
    slider.SetFill(val)
#===================== Array Mic Remote (Channel 2) =====================
tlp.SLD_ARRAY_REMOTE_E.SetRange(-36.0,-10.0,0.1)
@event(tlp.SLD_ARRAY_REMOTE_E, 'Changed')
def sld_array_remote_change_EN(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(2, val)
@event(tlp.BTN_ARRAY_REMOTE_MUTE_E, 'Pressed')
def btn_array_remote_mute_press_EN(btn, state):
    current = av.audio.get_input_mute(2)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(2, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_ARRAY_REMOTE_E, 'Released')
def sld_array_remote_mute_release_EN(slider, state, val):
    av.audio.set_input_mute(2, 'Off')
    slider.SetFill(val)
#===================== Handheld Mic (Channel 4) =====================
tlp.SLD_HANDHELD_E.SetRange(-36.0,0.0,0.1)
@event(tlp.SLD_HANDHELD_E, 'Changed')
def sld_handheld_change_EN(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(4, val)
@event(tlp.BTN_HANDHELD_MUTE_E, 'Pressed')
def btn_handheld_mute_press_EN(btn, state):
    current = av.audio.get_input_mute(4)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(4, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_HANDHELD_E, 'Released')
def sld_handheld_mute_release_EN(slider, state, val):
    av.audio.set_input_mute(4, 'Off')
    slider.SetFill(val)
#===================== Handheld Mic 2 (Channel 5) =====================
tlp.SLD_HANDHELD2_E.SetRange(-36.0,0.0,0.1)
@event(tlp.SLD_HANDHELD2_E, 'Changed')
def sld_handheld2_change_EN(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(5, val)
@event(tlp.BTN_HANDHELD_MUTE2_E, 'Pressed')
def btn_handheld_mute2_press_EN(btn, state):
    current = av.audio.get_input_mute(5)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(5, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_HANDHELD2_E, 'Released')
def sld_handheld_mute2_release_EN(slider, state, val):
    av.audio.set_input_mute(5, 'Off')
    slider.SetFill(val)
#===================== Stereo (Channel 6+7 Linked) =====================
tlp.SLD_STEREO_E.SetRange(-36.0,6.0,0.1)
@event(tlp.SLD_STEREO_E, 'Changed')
def sld_stereo_change_EN(slider, state, val):
    slider.SetFill(val)
    av.audio.set_input_volume(6, val)
    av.audio.set_input_volume(7, val)
@event(tlp.BTN_STEREO_MUTE_E, 'Pressed')
def btn_stereo_mute_press_EN(btn, state):
    current = av.audio.get_input_mute(6)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_input_mute(6, new_state)
    av.audio.set_input_mute(7, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_STEREO_E, 'Released')
def sld_stereo_mute_release_EN(slider, state, val):
    av.audio.set_input_mute(6, 'Off')
    av.audio.set_input_mute(7, 'Off')
    slider.SetFill(val)
#===================== Webex Output (Channel 7) =====================
tlp.SLD_WEBEX_E.SetRange(-36.0,6.0,0.1)
@event(tlp.SLD_WEBEX_E, 'Changed')
def sld_webex_change_EN(slider, state, val):
    slider.SetFill(val)
    av.audio.set_output_volume(7, val)
@event(tlp.BTN_WEBEX_MUTE_E, 'Pressed')
def btn_webex_mute_press_EN(btn, state):
    current = av.audio.get_output_mute(7)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_output_mute(7, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_WEBEX_E, 'Released')
def sld_webex_mute_release_EN(slider, state, val):
    av.audio.set_output_mute(7, 'Off')
    slider.SetFill(val)
#==================== Recording Output (Channel 8) =====================
tlp.SLD_RECORD_E.SetRange(-36.0,6.0,0.1)
@event(tlp.SLD_RECORD_E, 'Changed')
def sld_record_change_EN(slider, state, val):
    slider.SetFill(val)
    av.audio.set_output_volume(8, val)
@event(tlp.BTN_RECORD_MUTE_E, 'Pressed')
def btn_record_mute_press_EN(btn, state):
    current = av.audio.get_output_mute(8)
    new_state = 'On' if current == 'Off' else 'Off'
    av.audio.set_output_mute(8, new_state)
    btn.SetState(1 if new_state == 'On' else 0)
    _sync_button_state(btn, 1 if new_state == 'On' else 0)
@event(tlp.SLD_RECORD_E, 'Released')
def sld_record_mute_release_EN(slider, state, val):
    av.audio.set_output_mute(8, 'Off')
    slider.SetFill(val)
# Initialize
def Initialize():
    print('ControlScript', Platform(), Version())
    print('System Initialized')
    dev.TLP1025M.ShowPage(tlp.PAGE_START)
    dev.sensor.Connect()
    print('seneor polling started')
    sensor_start_poll()
    av.matrix_tie(vars.MATRIX_INPUT_BYOD,vars.MATRIX_OUTPUT_LED)
    av.matrix_tie(vars.MATRIX_INPUT_BYOD,vars.MATRIX_OUTPUT_RETURN_TV)
    av.matrix_tie(vars.MATRIX_INPUT_BYOD,vars.MATRIX_OUTPUT_LEFT_TV)
    av.matrix_tie(vars.MATRIX_INPUT_BYOD,vars.MATRIX_OUTPUT_RIGHT_TV)
    av.matrix_tie(vars.MATRIX_INPUT_BYOD,vars.MATRIX_OUTPUT_RECORDER)
    av.matrix_tie(vars.MATRIX_INPUT_CAMERA,vars.MATRIX_OUTPUT_CAPTURE)
    martix.send_event({"Current Input Source":"Wireless Screen Casting"})
   
  
    