import win32print

def send_escpos_command(command):
    # 获取默认打印机
     #printer_name = win32print.GetDefaultPrinter()
    printer_name = 'POS-58'
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

def process_print_data(data):
    # 这里可以添加修改数据的逻辑
    #template = b'========================================\n'
    headline1 = b'\x1b@\x1b!\x10           TROBAR-SE            \n\x1b@\x1b!\x00\n'
    headline2 = b'CIF: B12345678 TEL: 123 456 789 \n'
    headline3 = b'     CARRER DE FELIP II, 71     \n'
    headline4 = b'        08027 BARCELONA         \n\n'
    modified_data = headline1 + headline2 + headline3 + headline4 + data

    #print(modified_data.decode('latin1'))  # 使用 latin1 解码以避免因非 UTF-8 字符引起的错误 
    return modified_data
# 示例ESC/POS命令，这里是打印一行文本
escpos_command = b'\x1b@\x1b!\x10Hello, ESC/POS!\n\x1b@\x1b!\x00'
raw_data = b'\x1b=\x01\x1b@\x1bt\x00\x1bR\x00\x1ba\x01\x1b!\x10\x1c!\x08\x1b!\x10\x1c!\x08           BOHAO IMP-EXP S.A.           \n                          \n\x1b!\x00\x1c!\x00                                        \n            C/.GRAN VIA, 88             \n            08088 BARCELONA             \n             NIF:A-88888888             \n\x1b!\x00\x1c!\x00                                        \n\x1b!\x10\x1c!\x08========================================\n\x1b!\x00\x1c!\x00\x1b!\x10\x1c!\x08MESA:  11                     FACTURA: 9\n\x1b!\x00\x1c!\x0023-06-2024                              \n----------------------------------------\nCAN.  DESCRIPCION           PRE.    SUMA\n----------------------------------------\n 1 SOPA DE MISO             3,50    3,50\n----------------------------------------\n\x1b!\x10\x1c!\x08              Total:        3,50  Euro  \n\x1b!\x00\x1c!\x00                                        \n              IVA INCLUIDO              \n         GRACIAS POR SU VISITA          \n\x1b!\x00\x1c!\x00                                        \n----------------------------------------\n   Imponible   IVA%       IVA           \n----------------------------------------\n        3,18    10%      0,32           \n----------------------------------------\n                                        \n\x1bd\x01\x1dVB\x00'

# 调用函数发送ESC/POS命令
raw_data = process_print_data(b'')
send_escpos_command(raw_data.decode('utf-8'))
#send_escpos_command(raw_data.decode('utf-8'))
