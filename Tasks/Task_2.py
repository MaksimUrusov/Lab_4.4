#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import pathlib
import logging
from datetime import datetime

# Настройка логгирования с добавлением времени выполнения до миллисекунд
logging.basicConfig(filename='planes.log', level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def add_plane(staff, destination, num, typ):
    staff.append({"destination": destination, "num": num, "typ": typ})
    logging.info(f"Добавлен самолет: пункт назначения {destination}, номер {num}, тип {typ}")
    return staff


def display_planes(staff):
    if staff:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format('-' * 4, '-' * 30, '-' * 20, '-' * 15)
        print(line)
        print('| {:^4} | {:^30} | {:^20} | {:^15} |'.format("No", "Пункт назначения", "Номер рейса", "Тип самолета"))
        print(line)
        for idx, plane in enumerate(staff, 1):
            print('| {:>4} | {:<30} | {:<20} | {:>15} |'.format(idx, plane.get('destination', ''), plane.get('num', ''),
                                                                plane.get('typ', '')))
            print(line)
    else:
        print("Список самолетов пуст")
        logging.info("Попытка отобразить пустой список самолетов")


def select_planes(staff, jet):
    result = [plane for plane in staff if jet == plane.get('typ', '')]
    if not result:
        logging.info(f"Самолеты типа {jet} не найдены")
    return result


def save_planes(file_name, staff):
    try:
        with open(file_name, "w", encoding="utf-8") as fout:
            json.dump(staff, fout, ensure_ascii=False, indent=4)
            logging.info(f"Данные успешно сохранены в файл {file_name}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных: {e}")


def load_planes(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)
    except FileNotFoundError:
        logging.warning(f"Файл {file_name} не найден. Будет создан новый файл.")
        return []
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {e}")
        return []


def main(command_line=None):
    start_time = datetime.now()

    parser = argparse.ArgumentParser("planes")
    subparsers = parser.add_subparsers(dest="command")

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("filename", action="store", help="The data file name")

    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new plane")
    add.add_argument("-d", "--destination", action="store", required=True, help="The plane's destination")
    add.add_argument("-n", "--num", action="store", type=int, required=True, help="The plane's number")
    add.add_argument("-t", "--typ", action="store", required=True, help="The plane's type")

    _ = subparsers.add_parser("display", parents=[file_parser], help="Display all planes")

    select = subparsers.add_parser("select", parents=[file_parser], help="Select the planes")
    select.add_argument("-T", "--type", action="store", required=True, help="The required type")

    args = parser.parse_args(command_line)
    is_dirty = False
    args.filename = pathlib.Path.home().joinpath(args.filename)
    if os.path.exists(args.filename):
        planes = load_planes(args.filename)
    else:
        planes = []

    if args.command == "add":
        planes = add_plane(planes, args.destination, args.num, args.typ)
        is_dirty = True
    elif args.command == "display":
        display_planes(planes)
    elif args.command == "select":
        selected = select_planes(planes, args.type)
        display_planes(selected)

    if is_dirty:
        save_planes(args.filename, planes)

    end_time = datetime.now()
    logging.info(f"Выполнение команды завершено. Время выполнения: {end_time - start_time}")


if __name__ == '__main__':
    main()