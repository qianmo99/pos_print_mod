import serial
import time
import win32print

# 定义虚拟串口和实际打印机串口
virtual_printer_port = 'COM3'
#actual_printer_port = 'USB001'

def send_escpos_command(command):
    # 获取默认打印机
    #printer_name = win32print.GetDefaultPrinter()
    printer_name = 'GP-5830Series'
    # 打开打印机
    printer_handle = win32print.OpenPrinter(printer_name)

    # 开始打印任务
    win32print.StartDocPrinter(printer_handle, 1, ("ESC/POS Document", None, "RAW"))
    win32print.StartPagePrinter(printer_handle)

    # 发送ESC/POS命令
    win32print.WritePrinter(printer_handle, command.encode())

    # 结束打印任务
    win32print.EndPagePrinter(printer_handle)
    win32print.EndDocPrinter(printer_handle)

    # 关闭打印机
    win32print.ClosePrinter(printer_handle)

# 打印数据处理函数
def process_print_data(data):
    # 这里可以添加修改数据的逻辑
    #template = b'========================================\n'
    headline1 = b'\x1b@\x1b!\x10               TROBAR-SE                \n\x1b@\x1b!\x00\n'
    headline2 = b'    CIF: B12345678 TEL: 123 456 789     \n'
    headline3 = b'         CARRER DE FELIP II, 71         \n'
    headline4 = b'            08027 BARCELONA             \n\n'
    modified_data = headline1 + headline2 + headline3 + headline4 + data

    #print(modified_data.decode('latin1'))  # 使用 latin1 解码以避免因非 UTF-8 字符引起的错误 
    return modified_data

# 删除原始的店面信息
def del_original_title(raw_data):
    separator = b'========================================'
    separator_index = raw_data.find(separator)

    # 确保找到了分隔符，然后截取从该行开始的内容
    if separator_index != -1:
        processed_data = raw_data[separator_index:]
    else:
        processed_data = raw_data  # 如果找不到分隔符，则不做处理
    # 打印处理后的数据
    #print(processed_data.decode('latin1'))  # 使用 latin1 解码以避免因非 UTF-8 字符引起的错误 
    return processed_data

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

                # 处理和修改打印数据
                #processed_data = process_print_data(raw_data.decode('utf-8'))
                #print(f"Processed data: {processed_data}")

                # 发送修改后的数据到实际的POS58打印机
                #actual_printer.write(processed_data.encode('utf-8'))
                #actual_printer.write(raw_data)
               # print("Data sent to actual printer")
                processed_data = del_original_title(raw_data)
                processed_data = process_print_data(processed_data)
                
                print(processed_data.decode('utf-8'))
                send_escpos_command(processed_data.decode('utf-8'))
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        virtual_printer.close()
        #actual_printer.close()

if __name__ == "__main__":
    main()
