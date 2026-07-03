#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_processor.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/02 13:20:32 by jkrishna            #+#    #+#            #
#   Updated: 2026/07/03 11:09:13 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import abc
from typing import Any
from abc import ABC


class DataProcessor(ABC):

    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0

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


class NumericProcessor(DataProcessor):

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
            self._storage.append(str(data))

        if isinstance(data, list):
            for value in data:
                self._storage.append(str(value))


class TestProcessor(DataProcessor):

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
            self._storage.append(data)

        if isinstance(data, list):
            for value in data:
                self._storage.append(value)


class LogProcessor(DataProcessor):

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
            self._storage.append(formatted)


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    nprocessor = NumericProcessor()
    print(f" Trying to validate input '42': {nprocessor.validate(42)}")
    print(f" Trying to validate input 'Hello': {nprocessor.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    nprocessor.ingest("foo")  # type: ignore
    nprocessor.ingest([1, 2, 3, 4, 5])
    print(" Extracting 3 values...")
    for _ in range(3):
        result = nprocessor.output()
        print(f" Numeric value {result[0]}: {result[1]}")

    print("\nTesting Text Processor...")
    tprocessor = TestProcessor()
    print(f" Trying to validate input '42': {tprocessor.validate(42)}")
    tprocessor.ingest(['Hello', 'Nexus', 'World'])
    print(" Extracting 1 values...")
    result1 = tprocessor.output()
    print(f" Text value {result1[0]}: {result1[1]}")

    print("\nTesting Log Processor...")
    lprocessor = LogProcessor()
    print(f" Trying to validate input 'Hello': {lprocessor.validate('Hello')}")
    lprocessor.ingest(
        [{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
         {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}])
    print(" Extracting 2 values...")
    for _ in range(2):
        result2 = lprocessor.output()
        print(f" Log entry {result2[0]}: {result2[1]}")


if __name__ == "__main__":
    main()
