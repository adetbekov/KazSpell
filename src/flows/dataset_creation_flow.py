from metaflow import FlowSpec, step, Parameter, IncludeFile
import os
import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

class DatasetCreationFlow(FlowSpec):
    input_dir = Parameter('input_dir', default='data/raw', help="Путь к директории с EPUB файлами")
    output_dir = Parameter('output_dir', default='data/processed', help="Путь для сохранения обработанных данных")
    max_chunk_size = Parameter('max_chunk_size', default=200, help="Максимальный размер чанка в словах")

    @step
    def start(self):
        """
        Начальный шаг, подготавливающий директории для хранения данных.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        nltk.download('punkt')
        nltk.download('punkt_tab')
        self.next(self.extract_texts)

    @step
    def extract_texts(self):
        """
        Извлекает тексты из EPUB файлов.
        """
        self.text_data = {}
        for file_name in os.listdir(self.input_dir):
            if file_name.endswith('.epub'):
                file_path = os.path.join(self.input_dir, file_name)
                text = self.extract_text_from_epub(file_path)
                book_title = os.path.splitext(file_name)[0]
                self.text_data[book_title] = text
        self.next(self.split_and_save_chunks)

    def extract_text_from_epub(self, file_path):
        """
        Извлекает текст из EPUB файла.
        """
        book = epub.read_epub(file_path)
        text = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                text += soup.get_text(separator=" ")
        return text

    @step
    def split_and_save_chunks(self):
        """
        Разделяет текст на чанки и сохраняет их в .txt файлы.
        """
        for book_title, text in self.text_data.items():
            chunks = self.split_text_into_chunks(text)
            self.save_book_chunks_to_txt(chunks, book_title)  # Сохранение в формате .txt
        self.next(self.end)


    def split_text_into_chunks(self, text):
        """
        Разделяет текст на чанки с учетом максимального размера.
        """
        sentences = sent_tokenize(text)
        chunks = []
        chunk = []

        for sentence in sentences:
            if sentence[0].isupper() and sentence[-1] in ".!?":
                words = word_tokenize(sentence)
                if len(chunk) + len(words) <= self.max_chunk_size:
                    chunk.extend(words)
                else:
                    chunks.append(" ".join(chunk))
                    chunk = words

        if chunk:
            chunks.append(" ".join(chunk))
        
        return chunks

    def save_book_chunks_to_txt(self, chunks, book_title):
        """
        Сохраняет все чанки книги в один .txt файл, предварительно очищая их от лишних пробелов.
        
        :param chunks: Список чанков текста.
        :param book_title: Название книги для имени файла.
        """
        file_name = f"{book_title}.txt"
        file_path = os.path.join(self.output_dir, file_name)
        
        with open(file_path, mode='w', encoding='utf-8') as file:
            for chunk in chunks:
                cleaned_chunk = clean_text_with_proper_quotes(chunk)  # Очистка текста перед сохранением
                file.write(cleaned_chunk + "\n")  # Отделяем каждый чанк пустой строкой

    @step
    def end(self):
        """
        Завершение пайплайна.
        """
        print("Датасет успешно создан и сохранен в папке", self.output_dir)


def clean_text_with_proper_quotes(text):
    """
    Форматирует текст с правильным открытием и закрытием кавычек для каждой строки,
    убирает лишние пробелы после открывающей и перед закрывающей кавычкой, а также вокруг знаков препинания.
    """
    # Разделить текст на строки
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        # Сброс состояния открытых кавычек для новой строки
        cleaned_line = ""
        inside_quotes = False

        # Удалить пробелы перед знаками препинания
        line = re.sub(r'\s+([,.!?;:])', r'\1', line)
        # Удалить лишние пробелы внутри строки
        line = re.sub(r'\s+', ' ', line)
        # Заменить двойные одинарные кавычки на стандартные двойные кавычки
        line = line.replace("``", '"').replace("''", '"')

        # Проход по символам строки
        for i, char in enumerate(line):
            # Обработка открывающей кавычки
            if char == '"' and not inside_quotes:
                cleaned_line += '"'
                inside_quotes = True
                # Пропуск пробела сразу после открывающей кавычки, если он есть
                if i + 1 < len(line) and line[i + 1] == ' ':
                    continue

            # Обработка закрывающей кавычки
            elif char == '"' and inside_quotes:
                # Удаление пробела перед закрывающей кавычкой, если он есть
                if cleaned_line and cleaned_line[-1] == ' ':
                    cleaned_line = cleaned_line[:-1]
                cleaned_line += '"'
                inside_quotes = False

            # Добавление остальных символов
            else:
                cleaned_line += char

        # Добавление пробела после закрывающей кавычки, если за ней сразу идет слово
        cleaned_line = re.sub(r'"\s*([^\s,.!?;:])', r'" \1', cleaned_line)

        # Добавление очищенной строки в список
        cleaned_lines.append(cleaned_line.strip())

    # Объединить строки обратно в текст
    return '\n'.join(cleaned_lines)


if __name__ == "__main__":
    DatasetCreationFlow()
