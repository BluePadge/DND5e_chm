import os
import codecs

def convert_to_utf8(path, file_types=['.txt']):
    """
    将指定路径下的所有文本文件（包括子文件夹和子文件夹的子文件夹下的）转换为utf8格式。
    自动判断原来的格式是什么，而本身就是utf8格式的文件不转换。
    输出被转换的文件列表，格式为文件路径-文件名-原格式-新格式。

    参数：
    path：要转换的文件夹路径。
    file_types：要转换的文件类型列表，默认为['.txt']。

    返回：
    包含被转换的文件信息的列表，每个元素都是一个包含文件路径、文件名、原格式和新格式的四元组。
    """
    converted_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if not any([file.endswith(file_type) for file_type in file_types]):
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                try:
                    # Try to decode file with utf-8
                    raw_data.decode('utf-8')
                    file_encoding = 'utf-8'
                except UnicodeDecodeError:
                    # If decoding with utf-8 fails, try with other encodings
                    possible_encodings = ['gbk', 'big5', 'utf-16', 'utf-8-sig']
                    for encoding in possible_encodings:
                        try:
                            raw_data.decode(encoding)
                            file_encoding = encoding
                            break
                        except UnicodeDecodeError:
                            continue
                    else:
                        # If all encodings fail, skip the file
                        continue

            # If the file is not already utf-8, convert it to utf-8
            if file_encoding != 'utf-8':
                with codecs.open(file_path, 'w', encoding='utf-8') as f:
                    f.write(raw_data.decode(file_encoding))
                converted_files.append((root, file, file_encoding, 'utf-8'))
            else:
                converted_files.append((root, file, 'utf-8', 'utf-8'))

    # Print the list of converted files
    for file_info in converted_files:
        print('{}-{}-{}-{}'.format(*file_info))
        
    return converted_files


if __name__ == '__main__':
    folder_path = input('请输入要转换的文件夹路径：')
    file_types = input('请输入要转换的文件类型（用空格分隔多个类型，如 .txt .csv）：').split()
    converted_files = convert_to_utf8(folder_path, file_types)
    print('转换完成，以下文件已被转换为utf-8格式：')
    for file_info in converted_files:
        print('{}-{}-{}-{}'.format(*file_info))