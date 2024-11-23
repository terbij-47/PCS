import os.path
from PIL import Image

class FileReader:
    """
    Класс, отвечающий за чтение данных из файлов
    """
    current_path = ''

    def __init__(self, path : str) -> None:
        """
        Инициализация экземпляра класса.
        Аргументы:
            - имя директории, из которой нужно будет читать файлы:
                (str) path;
        """
        self.current_path = path

    def check_path(self, file_name : str) -> str | None:
        """
        Проверка существования файла.
        Аргументы:
            - имя файла:
                (str) file_name;
        Выходные данные:
            - (None) если файла не существует;
            - (str) полный путь к файлу от корневой директории;
        """
        full_path = self.current_path + file_name
        if not os.path.exists(full_path):
            print(f'No such file or directory: {full_path}')
            return None
        return full_path

    def read_file(self,  file_name : str) -> str | None:
        """
        Чтение текстового файла.
        Аргументы:
            - имя файла (без имени директории):
                (str) file_name;
        Выходные данные:
            - (None) если не удалось открыть или прочитать файл;
            - (str) содержание файла;

        """
        full_path = self.check_path(file_name)
        if not full_path:
            return None
        with open(full_path) as file:
            content = file.read()
            return content
        print(f'Cannot open "{full_path}" file')
        return None

    def read_image(self, file_name : str) -> tuple[tuple[int, int], bytes] | tuple[None, None]:
        """
        Чтение изображения.
        Аргументы:
            - имя файла (без имени директории):
                (str) file_name;
        Выходные данные:
            - ((None, None)) если не удалось открыть или прочитать файл;
            - (((int, int), bytes)) размер изображения по x и y в пикселях, данные изображения в формате RGBA;
        """
        full_path = self.check_path(file_name)
        if not full_path:
            return None, None
        with Image.open(full_path) as image:
            return image.size, image.convert("RGBA").tobytes()
        print(f'Cannot open "{full_path}" file')
        return None, None



