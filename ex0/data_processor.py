#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_processor.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/02 13:20:32 by jkrishna            #+#    #+#            #
#   Updated: 2026/07/02 15:44:03 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import abc
from typing import Any
from abc import ABC


class DataProcessor(ABC):

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    @staticmethod
    def output(self) -> tuple[int, str]:
        pass


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        try:
            data == int | float | list[int | float]
        except Exception:
            return False
        return True
        self.validate_check = 1

    def ingest(self, data: Any, type: Any, extract_num: int = 1) -> None:
        try:
            type == data
        except Exception:
            print("Got exception: Improper numeric data")
            return
        print(f"Processing data: {data}")
        print(f"Extracting {extract_num} values...")
        for i in range(0, extract_num):
            if i <= len(data):
                print(f"Numeric value {i}: {data[i]}")
            else:
                return

    def output(self) -> tuple[int, str]:
        pass


# class TestProcessor(DataProcessor):

#     def validate(self, data: Any) -> bool:
#         pass

#     def ingest(self, data: Any) -> None:
#         pass

#     def output(self) -> tuple[int, str]:
#         pass


# class LogProcessor(DataProcessor):

#     def validate(self, data: Any) -> bool:
#         pass

#     def ingest(self, data: Any) -> None:
#         pass

#     def output(self) -> tuple[int, str]:
#         pass


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    print("Trying to validate input '42': " + NumericProcessor.validate(42))
    print("Trying to validate input 'Hello': " +
          NumericProcessor.validate('Hello'))
    print("Test invalid ingestion of string 'foo' without prior validation:")
    NumericProcessor.ingest('foo', int)


if __name__ == "__main__":
    main()
