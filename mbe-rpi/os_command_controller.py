import subprocess

LOW_BOUND_CPU_SPEED = 600
HIGH_BOUND_CPU_SPEED = 2200

def modify_config_file(config_file_path, key, value):
    with open(config_file_path, 'r') as f:
        lines = f.readlines()

    with open(config_file_path, 'w') as f:
        for line in lines:
            if line.startswith(key):
                line = f"{key}={value}\n"
            f.write(line)

def reboot():
    command = "sudo reboot"
    subprocess.run(command, shell=True)

def set_cpu_speed(speed):
    if speed < LOW_BOUND_CPU_SPEED or speed > HIGH_BOUND_CPU_SPEED:
        print("LOG: CPU speed out of bounds")
        return
    config_file_path = '/boot/config.txt'
    # Specify the desired CPU clock speed in MHz
    # Modify the config.txt file
    modify_config_file(config_file_path, 'arm_freq', str(speed))

    print("LOG: CPU speed set to " + str(speed))    
    