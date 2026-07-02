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

    def output(self) -> tuple[int, str]:
        pass


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)

        return False

    def ingest(self, data: int | float | list[int, float]) -> None:
        try:
            if not self.validate(data):
                raise TypeError("Improper numeric data")
        except Exception:
            print("Got exception: Improper numeric data")
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
#          print(f"Processing data: {data}")
#        print(f"Extracting {extract_num} values...")
#       for i in range(0, extract_num):
#           if i <= len(data):
#              print(f"Numeric value {i}: {data[i]}")
#          else:
#              return


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    nprocessor = NumericProcessor()
    print(f"Trying to validate input '42': {nprocessor.validate(42)}")
    print(f"Trying to validate input 'Hello': {nprocessor.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    nprocessor.ingest("foo")


if __name__ == "__main__":
    main()
