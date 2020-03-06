# -*- coding: utf-8 -*-
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="this is a checker")
    parser.add_argument('-u', "--url", help="please input full url with http or https")
    parser.add_argument('-t', "--thread", nargs="?", const=1, default=1, type=int, help="run with 1 thread defalut")
    parser.add_argument('-o', "--output", nargs="?", const=1, default="links.txt", help="output file path")
    args = parser.parse_args()
    return args
