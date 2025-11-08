import usb.core
import usb.util


# with pure PyUSB
#for dev in usb.core.find(find_all=True):
#    print(dev)

#VID_0416&PID_5011
# 找到USB设备
dev = usb.core.find(idVendor=0x0416, idProduct=0x5011)  # 替换为你的打印机的厂商ID和产品ID

if dev is None:
    raise ValueError('Device not found')

# 打印设备信息
print(dev)



