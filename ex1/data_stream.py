#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_stream.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/03 11:12:34 by jkrishna            #+#    #+#            #
#   Updated: 2026/07/03 13:50:34 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import typing
import abc
from typing import Any
from abc import ABC


class DataProcessor(ABC):

    name: str = "Data Processor"

    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0
        self._total: int = 0

    def _store(self, value: str) -> None:
        self._storage.append(value)
        self._total += 1

    def get_stats(self) -> str:
        return (f"{self.name}: total {self._total} items processed, "
                f"remaining {len(self._storage)} on processor")

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data available")

        value = self._storage.pop(0)
        rank = self._rank
        self._rank += 1
        return (rank, value)


class DataStream():

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for item in stream:
            for p in self._processors:
                if p.validate(item):
                    p.ingest(item)
                    break
            else:
                print(
                    "DataStream error - Can't process"
                    f"element in stream: {item}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for p in self._processors:
            print(p.get_stats())


class NumericProcessor(DataProcessor):

    name: str = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Improper numeric data")
        except Exception:
            print(" Got exception: Improper numeric data")
            return

        if isinstance(data, (int, float)):
            self._store(str(data))

        if isinstance(data, list):
            for value in data:
                self._store(str(value))


class TextProcessor(DataProcessor):

    name: str = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)

        return False

    def ingest(self, data: Any) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Improper text data")
        except Exception:
            print("Got exception: Improper text data")
            return

        if isinstance(data, str):
            self._store(data)

        if isinstance(data, list):
            for value in data:
                self._store(value)


class LogProcessor(DataProcessor):

    name: str = "Log Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and
                "log_level" in item and
                "log_message" in item and
                isinstance(item["log_level"], str) and
                isinstance(item["log_message"], str)
                for item in data
            )
        return False

    def ingest(self, data: Any) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Improper log data")
        except Exception:
            print("Got exception: Improper log data")
            return

        for item in data:
            formatted = f"{item['log_level']}: {item['log_message']}"
            self._store(formatted)


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    nprocessor = NumericProcessor()
    tprocessor = TextProcessor()
    lprocessor = LogProcessor()

    print("\nRegistering Numeric Processors\n")
    ds.register_processor(nprocessor)

    stream = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO',
             'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]
    print(f"Send first batch of data on stream: {stream}")
    ds.process_stream(stream)
    ds.print_processors_stats()

    print("\nRegistering other data processors")
    ds.register_processor(tprocessor)
    ds.register_processor(lprocessor)
    print("Send the same batch again")
    ds.process_stream(stream)
    ds.print_processors_stats()

    print(
        "\nConsume some elements from the data processors:"
        "Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        nprocessor.output()
    for _ in range(2):
        tprocessor.output()
    for _ in range(1):
        lprocessor.output()
    ds.print_processors_stats()


if __name__ == "__main__":
    main()
