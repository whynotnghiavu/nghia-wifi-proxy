import subprocess
import os


def set_proxy(proxy_address, proxy_port):
    try:
        # Thiết lập proxy cho hệ thống
        os.system(f"gsettings set org.gnome.system.proxy mode 'manual'")
        os.system(f"gsettings set org.gnome.system.proxy.http host '{proxy_address}'")
        os.system(f"gsettings set org.gnome.system.proxy.http port {proxy_port}")
        os.system(f"gsettings set org.gnome.system.proxy.https host '{proxy_address}'")
        os.system(f"gsettings set org.gnome.system.proxy.https port {proxy_port}")

        # Thiết lập proxy cho APT
        with open('/etc/apt/apt.conf', 'w') as apt_conf:
            apt_conf.write(f'Acquire::http::Proxy "http://{proxy_address}:{proxy_port}";\n')
            apt_conf.write(f'Acquire::https::Proxy "http://{proxy_address}:{proxy_port}";\n')

        print("Proxy đã được thiết lập thành công.")
    except Exception as e:
        print("Đã xảy ra lỗi:", e)


def disable_proxy():
    try:
        # Tắt proxy cho hệ thống
        os.system("gsettings set org.gnome.system.proxy mode 'none'")

        # Tắt proxy trong tệp apt.conf
        with open('/etc/apt/apt.conf', 'w') as apt_conf:
            apt_conf.write(f'')
            # apt_conf.write(f'Acquire::http::Proxy "http://{proxy_address}:{proxy_port}";\n')
            # apt_conf.write(f'Acquire::https::Proxy "http://{proxy_address}:{proxy_port}";\n')

        # if os.path.exists('/etc/apt/apt.conf'):
        #     os.remove('/etc/apt/apt.conf')

        print("Proxy đã được tắt thành công.")
    except Exception as e:
        print("Đã xảy ra lỗi khi tắt proxy:", e)


try:
    # Kiểm tra kết nối mạng

    # Run the nmcli command to get the active Wi-Fi connections
    wifi_output = subprocess.check_output(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'])

    # Decode the output from bytes to string
    data_infor = wifi_output.decode('utf-8')

    # Process the output
    active_connections = []
    for line in data_infor.splitlines():
        active, ssid = line.split(':')
        if active == 'yes':
            active_connections.append(ssid)
            break

    # Print the active connections
    print("Active Wi-Fi connections:", active_connections)

    name_vvn20206205 = active_connections[0]

    if name_vvn20206205 == "vvn20206205":
        print(f"🚀 Có kết nối vvn20206205")
    else:
        print(f"🚀 Không kết nối vvn20206205")
        disable_proxy()
        exit()
except Exception as e:
    print(f"Đã xảy ra lỗi khi kiểm tra kết nối: {e}")
    disable_proxy()
    exit()

try:
    # Lấy thông tin địa chỉ IP và Gateway
    ip_info = subprocess.check_output(['ip', '-4', 'route', 'show', 'default']).decode('utf-8').split()
    proxy_address = ip_info[ip_info.index('via') + 1]
    proxy_port = "10809"

    print(f"🚀 {proxy_address}")
    print(f"🚀 {proxy_port}")
    set_proxy(proxy_address, proxy_port)
except Exception as e:
    print(f"Đã xảy ra lỗi khi lấy thông tin mạng: {e}")
    disable_proxy()
    exit()
