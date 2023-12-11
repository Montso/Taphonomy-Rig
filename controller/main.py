from configuration_manager import ConfigurationManager
from multi_uart_controller import MultiUARTController
import serial_assistance as sa
import time

if __name__ == "__main__":

    config_man = ConfigurationManager("configuration/")
    config = config_man.read_config_file()

    selected_port = sa.get_port_by_name(config.get('port_by_name'))
    if(selected_port):
        mc_control = MultiUARTController(selected_port)
        mc_control.set_power_to_all_channels(state = 0)
        #while(1):
        for device in range(config.get('num_devices')):
            mc_control.set_power_to_channel(channel = device,state = 1)
            mc_control.set_communication_channel(channel = device,baud = 0)
            message = f"D:{device} ["
            for packet in range(config.get('bytes_received')):
                    if(config.get('verbose_messages')):
                        short_message = f"Packet: {packet}\t data: {mc_control.read_byte()}\n"
                        message += short_message
                        print(short_message)
                    else:
                        message += f"{mc_control.read_byte()}"
                        if(packet != config.get('bytes_received')-1):
                            message += ','
                        else:
                            message += ']\n'
            print(message)
            mc_control.set_power_to_channel(channel = device,state = 0)
            with open(f"{config.get('data_directory')}{config.get('desiccation_filename')}", 'a') as f:
                f.write(f"epoch:{time.time()}, {message}")
        #time.sleep(config.get('sleep_period_seconds'))    
    else:
        print("No device found, confirm configuration settings and device -> exiting")
