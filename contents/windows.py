import subprocess
# pip install wmi
import wmi
import winreg

import time


def set_proxy_git(proxy_address, proxy_port):
    proxy_url = f"http://{proxy_address}:{proxy_port}"
    try:
        subprocess.run(["git", "config", "--global", "http.proxy", proxy_url], check=True)
        print(f"Proxy set to {proxy_url}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set proxy: {e}")

def disable_proxy_git():
    try:
        subprocess.run(["git", "config", "--global", "--unset", "http.proxy"], check=True)
        print("Proxy has been disabled.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable proxy: {e}")


def set_proxy(proxy_address, proxy_port):
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(
            reg, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE)

        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"{
                          proxy_address}:{proxy_port}")

        winreg.CloseKey(key)

        print("Proxy đã được thiết lập thành công.")
    except Exception as e:
        print("Đã xảy ra lỗi:", e)


def disable_proxy():
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(
            reg, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE)

        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

        winreg.CloseKey(key)

        print("Proxy đã được tắt thành công.")
    except Exception as e:
        print("Đã xảy ra lỗi khi tắt proxy:", e)


wifi_output = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
data_infor = wifi_output.decode('utf-8')

name_vvn20206205 = "vvn20206205"

if name_vvn20206205 in data_infor:
    print(f"🚀 Có kết nối {name_vvn20206205}")
else:
    print(f"🚀 Không kết nối {name_vvn20206205}")
    disable_proxy()
    disable_proxy_git()
    exit()


wmi_obj = wmi.WMI()
wmi_sql = "select IPAddress, DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
wmi_out = wmi_obj.query(wmi_sql)

for dev in wmi_out:
    try:
        # print(f"🚀 {dev}")
        proxy_address = dev.DefaultIPGateway[0]
        break
    except:
        pass

proxy_port = "10809"

print(f"🚀 {proxy_address}")
print(f"🚀 {proxy_port}")
set_proxy(proxy_address, proxy_port)
set_proxy_git(proxy_address, proxy_port)
time.sleep(1)