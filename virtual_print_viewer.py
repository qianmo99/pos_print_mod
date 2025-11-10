import serial
import time
import re
#from escpos.printer import Usb


# 定义虚拟串口和实际打印机串口
virtual_printer_port = 'COM3'
#actual_printer_port = 'COM7'


# 打印数据处理函数
def process_print_data(data):
    # 这里可以添加修改数据的逻辑
    modified_data = data.replace('Original Text', 'Modified Text')
    return modified_data

def decode_receipt_data(data):
    # 过滤掉不可见字符
    cleaned_data = re.sub(rb'[\x00-\x1F\x7F]', b'', data)
     # 解码为字符串
    decoded_string = cleaned_data.decode('utf-8', errors='ignore')
    return decoded_string

# 主程序
def main():
    # 打开虚拟串口用于读取数据
    virtual_printer = serial.Serial(virtual_printer_port, 9600, timeout=1)
    # 打开实际打印机串口用于发送数据
    #actual_printer = serial.Serial(actual_printer_port, 9600, timeout=1)



    try:
        while True:
            # 从虚拟串口读取数据
            if virtual_printer.in_waiting > 0:
                raw_data = virtual_printer.read(virtual_printer.in_waiting)
                print(f"Received raw data: {raw_data}")
                #print(decode_receipt_data(raw_data))
                # 处理和修改打印数据
                #processed_data = process_print_data(raw_data.decode('utf-8'))
                #print(f"Processed data: {processed_data}")

                # 发送修改后的数据到实际的POS58打印机
                #actual_printer.write(processed_data.encode('utf-8'))
                #print("Data sent to actual printer")

               

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        virtual_printer.close()
        #actual_printer.close()

if __name__ == "__main__":
    main()
