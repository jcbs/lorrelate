#!/bin/python3

import sys
import os
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finding log entries of events ocurring at the same time')
    parser.add_argument('--primarylogfile', metavar='log1', help='log file for which matching events should be found', nargs=1, type=str)
    parser.add_argument('--secondarylogfile', metavar='log2', help='log file for which matching events should be found', nargs="+", type=str)
    args = parser.parse_args()
