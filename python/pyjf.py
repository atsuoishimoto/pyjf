# -*- coding: ShiftJIS -*-
import re, bisect, unicodedata

UNKNOWN=0
ASCII=1
SJIS=2
EUC=3
JIS=4
UTF8=5
UTF16_LE=6
UTF16_BE=7

CONV_FAILED = "\x22\x2e"

_tbl_jis2mskanji = {
"\x22\x40" : "\x87\x9c",
"\x22\x41" : "\x87\x9b",
"\x22\x4c" : "\xee\xf9",
"\x22\x5c" : "\x87\x97",
"\x22\x5d" : "\x87\x96",
"\x22\x61" : "\x87\x91",
"\x22\x62" : "\x87\x90",
"\x22\x65" : "\x87\x95",
"\x22\x68" : "\x87\x9a",
"\x22\x69" : "\x87\x92",
"\x2d\x35" : "\x87\x54",
"\x2d\x36" : "\x87\x55",
"\x2d\x37" : "\x87\x56",
"\x2d\x38" : "\x87\x57",
"\x2d\x39" : "\x87\x58",
"\x2d\x3a" : "\x87\x59",
"\x2d\x3b" : "\x87\x5a",
"\x2d\x3c" : "\x87\x5b",
"\x2d\x3d" : "\x87\x5c",
"\x2d\x3e" : "\x87\x5d",
"\x2d\x62" : "\x87\x82",
"\x2d\x64" : "\x87\x84",
"\x2d\x6a" : "\x87\x8a",
"\x79\x21" : "\xed\x40",
"\x79\x22" : "\xed\x41",
"\x79\x23" : "\xed\x42",
"\x79\x24" : "\xed\x43",
"\x79\x25" : "\xed\x44",
"\x79\x26" : "\xed\x45",
"\x79\x27" : "\xed\x46",
"\x79\x28" : "\xed\x47",
"\x79\x29" : "\xed\x48",
"\x79\x2a" : "\xed\x49",
"\x79\x2b" : "\xed\x4a",
"\x79\x2c" : "\xed\x4b",
"\x79\x2d" : "\xed\x4c",
"\x79\x2e" : "\xed\x4d",
"\x79\x2f" : "\xed\x4e",
"\x79\x30" : "\xed\x4f",
"\x79\x31" : "\xed\x50",
"\x79\x32" : "\xed\x51",
"\x79\x33" : "\xed\x52",
"\x79\x34" : "\xed\x53",
"\x79\x35" : "\xed\x54",
"\x79\x36" : "\xed\x55",
"\x79\x37" : "\xed\x56",
"\x79\x38" : "\xed\x57",
"\x79\x39" : "\xed\x58",
"\x79\x3a" : "\xed\x59",
"\x79\x3b" : "\xed\x5a",
"\x79\x3c" : "\xed\x5b",
"\x79\x3d" : "\xed\x5c",
"\x79\x3e" : "\xed\x5d",
"\x79\x3f" : "\xed\x5e",
"\x79\x40" : "\xed\x5f",
"\x79\x41" : "\xed\x60",
"\x79\x42" : "\xed\x61",
"\x79\x43" : "\xed\x62",
"\x79\x44" : "\xed\x63",
"\x79\x45" : "\xed\x64",
"\x79\x46" : "\xed\x65",
"\x79\x47" : "\xed\x66",
"\x79\x48" : "\xed\x67",
"\x79\x49" : "\xed\x68",
"\x79\x4a" : "\xed\x69",
"\x79\x4b" : "\xed\x6a",
"\x79\x4c" : "\xed\x6b",
"\x79\x4d" : "\xed\x6c",
"\x79\x4e" : "\xed\x6d",
"\x79\x4f" : "\xed\x6e",
"\x79\x50" : "\xed\x6f",
"\x79\x51" : "\xed\x70",
"\x79\x52" : "\xed\x71",
"\x79\x53" : "\xed\x72",
"\x79\x54" : "\xed\x73",
"\x79\x55" : "\xed\x74",
"\x79\x56" : "\xed\x75",
"\x79\x57" : "\xed\x76",
"\x79\x58" : "\xed\x77",
"\x79\x59" : "\xed\x78",
"\x79\x5a" : "\xed\x79",
"\x79\x5b" : "\xed\x7a",
"\x79\x5c" : "\xed\x7b",
"\x79\x5d" : "\xed\x7c",
"\x79\x5e" : "\xed\x7d",
"\x79\x5f" : "\xed\x7e",
"\x79\x60" : "\xed\x80",
"\x79\x61" : "\xed\x81",
"\x79\x62" : "\xed\x82",
"\x79\x63" : "\xed\x83",
"\x79\x64" : "\xed\x84",
"\x79\x65" : "\xed\x85",
"\x79\x66" : "\xed\x86",
"\x79\x67" : "\xed\x87",
"\x79\x68" : "\xed\x88",
"\x79\x69" : "\xed\x89",
"\x79\x6a" : "\xed\x8a",
"\x79\x6b" : "\xed\x8b",
"\x79\x6c" : "\xed\x8c",
"\x79\x6d" : "\xed\x8d",
"\x79\x6e" : "\xed\x8e",
"\x79\x6f" : "\xed\x8f",
"\x79\x70" : "\xed\x90",
"\x79\x71" : "\xed\x91",
"\x79\x72" : "\xed\x92",
"\x79\x73" : "\xed\x93",
"\x79\x74" : "\xed\x94",
"\x79\x75" : "\xed\x95",
"\x79\x76" : "\xed\x96",
"\x79\x77" : "\xed\x97",
"\x79\x78" : "\xed\x98",
"\x79\x79" : "\xed\x99",
"\x79\x7a" : "\xed\x9a",
"\x79\x7b" : "\xed\x9b",
"\x79\x7c" : "\xed\x9c",
"\x79\x7d" : "\xed\x9d",
"\x79\x7e" : "\xed\x9e",
"\x7a\x21" : "\xed\x9f",
"\x7a\x22" : "\xed\xa0",
"\x7a\x23" : "\xed\xa1",
"\x7a\x24" : "\xed\xa2",
"\x7a\x25" : "\xed\xa3",
"\x7a\x26" : "\xed\xa4",
"\x7a\x27" : "\xed\xa5",
"\x7a\x28" : "\xed\xa6",
"\x7a\x29" : "\xed\xa7",
"\x7a\x2a" : "\xed\xa8",
"\x7a\x2b" : "\xed\xa9",
"\x7a\x2c" : "\xed\xaa",
"\x7a\x2d" : "\xed\xab",
"\x7a\x2e" : "\xed\xac",
"\x7a\x2f" : "\xed\xad",
"\x7a\x30" : "\xed\xae",
"\x7a\x31" : "\xed\xaf",
"\x7a\x32" : "\xed\xb0",
"\x7a\x33" : "\xed\xb1",
"\x7a\x34" : "\xed\xb2",
"\x7a\x35" : "\xed\xb3",
"\x7a\x36" : "\xed\xb4",
"\x7a\x37" : "\xed\xb5",
"\x7a\x38" : "\xed\xb6",
"\x7a\x39" : "\xed\xb7",
"\x7a\x3a" : "\xed\xb8",
"\x7a\x3b" : "\xed\xb9",
"\x7a\x3c" : "\xed\xba",
"\x7a\x3d" : "\xed\xbb",
"\x7a\x3e" : "\xed\xbc",
"\x7a\x3f" : "\xed\xbd",
"\x7a\x40" : "\xed\xbe",
"\x7a\x41" : "\xed\xbf",
"\x7a\x42" : "\xed\xc0",
"\x7a\x43" : "\xed\xc1",
"\x7a\x44" : "\xed\xc2",
"\x7a\x45" : "\xed\xc3",
"\x7a\x46" : "\xed\xc4",
"\x7a\x47" : "\xed\xc5",
"\x7a\x48" : "\xed\xc6",
"\x7a\x49" : "\xed\xc7",
"\x7a\x4a" : "\xed\xc8",
"\x7a\x4b" : "\xed\xc9",
"\x7a\x4c" : "\xed\xca",
"\x7a\x4d" : "\xed\xcb",
"\x7a\x4e" : "\xed\xcc",
"\x7a\x4f" : "\xed\xcd",
"\x7a\x50" : "\xed\xce",
"\x7a\x51" : "\xed\xcf",
"\x7a\x52" : "\xed\xd0",
"\x7a\x53" : "\xed\xd1",
"\x7a\x54" : "\xed\xd2",
"\x7a\x55" : "\xed\xd3",
"\x7a\x56" : "\xed\xd4",
"\x7a\x57" : "\xed\xd5",
"\x7a\x58" : "\xed\xd6",
"\x7a\x59" : "\xed\xd7",
"\x7a\x5a" : "\xed\xd8",
"\x7a\x5b" : "\xed\xd9",
"\x7a\x5c" : "\xed\xda",
"\x7a\x5d" : "\xed\xdb",
"\x7a\x5e" : "\xed\xdc",
"\x7a\x5f" : "\xed\xdd",
"\x7a\x60" : "\xed\xde",
"\x7a\x61" : "\xed\xdf",
"\x7a\x62" : "\xed\xe0",
"\x7a\x63" : "\xed\xe1",
"\x7a\x64" : "\xed\xe2",
"\x7a\x65" : "\xed\xe3",
"\x7a\x66" : "\xed\xe4",
"\x7a\x67" : "\xed\xe5",
"\x7a\x68" : "\xed\xe6",
"\x7a\x69" : "\xed\xe7",
"\x7a\x6a" : "\xed\xe8",
"\x7a\x6b" : "\xed\xe9",
"\x7a\x6c" : "\xed\xea",
"\x7a\x6d" : "\xed\xeb",
"\x7a\x6e" : "\xed\xec",
"\x7a\x6f" : "\xed\xed",
"\x7a\x70" : "\xed\xee",
"\x7a\x71" : "\xed\xef",
"\x7a\x72" : "\xed\xf0",
"\x7a\x73" : "\xed\xf1",
"\x7a\x74" : "\xed\xf2",
"\x7a\x75" : "\xed\xf3",
"\x7a\x76" : "\xed\xf4",
"\x7a\x77" : "\xed\xf5",
"\x7a\x78" : "\xed\xf6",
"\x7a\x79" : "\xed\xf7",
"\x7a\x7a" : "\xed\xf8",
"\x7a\x7b" : "\xed\xf9",
"\x7a\x7c" : "\xed\xfa",
"\x7a\x7d" : "\xed\xfb",
"\x7a\x7e" : "\xed\xfc",
"\x7b\x21" : "\xee\x40",
"\x7b\x22" : "\xee\x41",
"\x7b\x23" : "\xee\x42",
"\x7b\x24" : "\xee\x43",
"\x7b\x25" : "\xee\x44",
"\x7b\x26" : "\xee\x45",
"\x7b\x27" : "\xee\x46",
"\x7b\x28" : "\xee\x47",
"\x7b\x29" : "\xee\x48",
"\x7b\x2a" : "\xee\x49",
"\x7b\x2b" : "\xee\x4a",
"\x7b\x2c" : "\xee\x4b",
"\x7b\x2d" : "\xee\x4c",
"\x7b\x2e" : "\xee\x4d",
"\x7b\x2f" : "\xee\x4e",
"\x7b\x30" : "\xee\x4f",
"\x7b\x31" : "\xee\x50",
"\x7b\x32" : "\xee\x51",
"\x7b\x33" : "\xee\x52",
"\x7b\x34" : "\xee\x53",
"\x7b\x35" : "\xee\x54",
"\x7b\x36" : "\xee\x55",
"\x7b\x37" : "\xee\x56",
"\x7b\x38" : "\xee\x57",
"\x7b\x39" : "\xee\x58",
"\x7b\x3a" : "\xee\x59",
"\x7b\x3b" : "\xee\x5a",
"\x7b\x3c" : "\xee\x5b",
"\x7b\x3d" : "\xee\x5c",
"\x7b\x3e" : "\xee\x5d",
"\x7b\x3f" : "\xee\x5e",
"\x7b\x40" : "\xee\x5f",
"\x7b\x41" : "\xee\x60",
"\x7b\x42" : "\xee\x61",
"\x7b\x43" : "\xee\x62",
"\x7b\x44" : "\xee\x63",
"\x7b\x45" : "\xee\x64",
"\x7b\x46" : "\xee\x65",
"\x7b\x47" : "\xee\x66",
"\x7b\x48" : "\xee\x67",
"\x7b\x49" : "\xee\x68",
"\x7b\x4a" : "\xee\x69",
"\x7b\x4b" : "\xee\x6a",
"\x7b\x4c" : "\xee\x6b",
"\x7b\x4d" : "\xee\x6c",
"\x7b\x4e" : "\xee\x6d",
"\x7b\x4f" : "\xee\x6e",
"\x7b\x50" : "\xee\x6f",
"\x7b\x51" : "\xee\x70",
"\x7b\x52" : "\xee\x71",
"\x7b\x53" : "\xee\x72",
"\x7b\x54" : "\xee\x73",
"\x7b\x55" : "\xee\x74",
"\x7b\x56" : "\xee\x75",
"\x7b\x57" : "\xee\x76",
"\x7b\x58" : "\xee\x77",
"\x7b\x59" : "\xee\x78",
"\x7b\x5a" : "\xee\x79",
"\x7b\x5b" : "\xee\x7a",
"\x7b\x5c" : "\xee\x7b",
"\x7b\x5d" : "\xee\x7c",
"\x7b\x5e" : "\xee\x7d",
"\x7b\x5f" : "\xee\x7e",
"\x7b\x60" : "\xee\x80",
"\x7b\x61" : "\xee\x81",
"\x7b\x62" : "\xee\x82",
"\x7b\x63" : "\xee\x83",
"\x7b\x64" : "\xee\x84",
"\x7b\x65" : "\xee\x85",
"\x7b\x66" : "\xee\x86",
"\x7b\x67" : "\xee\x87",
"\x7b\x68" : "\xee\x88",
"\x7b\x69" : "\xee\x89",
"\x7b\x6a" : "\xee\x8a",
"\x7b\x6b" : "\xee\x8b",
"\x7b\x6c" : "\xee\x8c",
"\x7b\x6d" : "\xee\x8d",
"\x7b\x6e" : "\xee\x8e",
"\x7b\x6f" : "\xee\x8f",
"\x7b\x70" : "\xee\x90",
"\x7b\x71" : "\xee\x91",
"\x7b\x72" : "\xee\x92",
"\x7b\x73" : "\xee\x93",
"\x7b\x74" : "\xee\x94",
"\x7b\x75" : "\xee\x95",
"\x7b\x76" : "\xee\x96",
"\x7b\x77" : "\xee\x97",
"\x7b\x78" : "\xee\x98",
"\x7b\x79" : "\xee\x99",
"\x7b\x7a" : "\xee\x9a",
"\x7b\x7b" : "\xee\x9b",
"\x7b\x7c" : "\xee\x9c",
"\x7b\x7d" : "\xee\x9d",
"\x7b\x7e" : "\xee\x9e",
"\x7c\x21" : "\xee\x9f",
"\x7c\x22" : "\xee\xa0",
"\x7c\x23" : "\xee\xa1",
"\x7c\x24" : "\xee\xa2",
"\x7c\x25" : "\xee\xa3",
"\x7c\x26" : "\xee\xa4",
"\x7c\x27" : "\xee\xa5",
"\x7c\x28" : "\xee\xa6",
"\x7c\x29" : "\xee\xa7",
"\x7c\x2a" : "\xee\xa8",
"\x7c\x2b" : "\xee\xa9",
"\x7c\x2c" : "\xee\xaa",
"\x7c\x2d" : "\xee\xab",
"\x7c\x2e" : "\xee\xac",
"\x7c\x2f" : "\xee\xad",
"\x7c\x30" : "\xee\xae",
"\x7c\x31" : "\xee\xaf",
"\x7c\x32" : "\xee\xb0",
"\x7c\x33" : "\xee\xb1",
"\x7c\x34" : "\xee\xb2",
"\x7c\x35" : "\xee\xb3",
"\x7c\x36" : "\xee\xb4",
"\x7c\x37" : "\xee\xb5",
"\x7c\x38" : "\xee\xb6",
"\x7c\x39" : "\xee\xb7",
"\x7c\x3a" : "\xee\xb8",
"\x7c\x3b" : "\xee\xb9",
"\x7c\x3c" : "\xee\xba",
"\x7c\x3d" : "\xee\xbb",
"\x7c\x3e" : "\xee\xbc",
"\x7c\x3f" : "\xee\xbd",
"\x7c\x40" : "\xee\xbe",
"\x7c\x41" : "\xee\xbf",
"\x7c\x42" : "\xee\xc0",
"\x7c\x43" : "\xee\xc1",
"\x7c\x44" : "\xee\xc2",
"\x7c\x45" : "\xee\xc3",
"\x7c\x46" : "\xee\xc4",
"\x7c\x47" : "\xee\xc5",
"\x7c\x48" : "\xee\xc6",
"\x7c\x49" : "\xee\xc7",
"\x7c\x4a" : "\xee\xc8",
"\x7c\x4b" : "\xee\xc9",
"\x7c\x4c" : "\xee\xca",
"\x7c\x4d" : "\xee\xcb",
"\x7c\x4e" : "\xee\xcc",
"\x7c\x4f" : "\xee\xcd",
"\x7c\x50" : "\xee\xce",
"\x7c\x51" : "\xee\xcf",
"\x7c\x52" : "\xee\xd0",
"\x7c\x53" : "\xee\xd1",
"\x7c\x54" : "\xee\xd2",
"\x7c\x55" : "\xee\xd3",
"\x7c\x56" : "\xee\xd4",
"\x7c\x57" : "\xee\xd5",
"\x7c\x58" : "\xee\xd6",
"\x7c\x59" : "\xee\xd7",
"\x7c\x5a" : "\xee\xd8",
"\x7c\x5b" : "\xee\xd9",
"\x7c\x5c" : "\xee\xda",
"\x7c\x5d" : "\xee\xdb",
"\x7c\x5e" : "\xee\xdc",
"\x7c\x5f" : "\xee\xdd",
"\x7c\x60" : "\xee\xde",
"\x7c\x61" : "\xee\xdf",
"\x7c\x62" : "\xee\xe0",
"\x7c\x63" : "\xee\xe1",
"\x7c\x64" : "\xee\xe2",
"\x7c\x65" : "\xee\xe3",
"\x7c\x66" : "\xee\xe4",
"\x7c\x67" : "\xee\xe5",
"\x7c\x68" : "\xee\xe6",
"\x7c\x69" : "\xee\xe7",
"\x7c\x6a" : "\xee\xe8",
"\x7c\x6b" : "\xee\xe9",
"\x7c\x6c" : "\xee\xea",
"\x7c\x6d" : "\xee\xeb",
"\x7c\x6e" : "\xee\xec",
"\x7c\x71" : "\xee\xef",
"\x7c\x72" : "\xee\xf0",
"\x7c\x73" : "\xee\xf1",
"\x7c\x74" : "\xee\xf2",
"\x7c\x75" : "\xee\xf3",
"\x7c\x76" : "\xee\xf4",
"\x7c\x77" : "\xee\xf5",
"\x7c\x78" : "\xee\xf6",
"\x7c\x79" : "\xee\xf7",
"\x7c\x7a" : "\xee\xf8",
"\x7c\x7c" : "\xee\xfa",
"\x7c\x7d" : "\xee\xfb",
"\x7c\x7e" : "\xee\xfc", }


_tbl_mskanji2jis = {
"\x87\x90" : "\x22\x62",
"\x87\x91" : "\x22\x61",
"\x87\x92" : "\x22\x69",
"\x87\x95" : "\x22\x65",
"\x87\x96" : "\x22\x5d",
"\x87\x97" : "\x22\x5c",
"\x87\x9a" : "\x22\x68",
"\x87\x9b" : "\x22\x41",
"\x87\x9c" : "\x22\x40",
"\xee\xf9" : "\x22\x4c",
"\xfa\x40" : "\x7c\x71",
"\xfa\x41" : "\x7c\x72",
"\xfa\x42" : "\x7c\x73",
"\xfa\x43" : "\x7c\x74",
"\xfa\x44" : "\x7c\x75",
"\xfa\x45" : "\x7c\x76",
"\xfa\x46" : "\x7c\x77",
"\xfa\x47" : "\x7c\x78",
"\xfa\x48" : "\x7c\x79",
"\xfa\x49" : "\x7c\x7a",
"\xfa\x4a" : "\x2d\x35",
"\xfa\x4b" : "\x2d\x36",
"\xfa\x4c" : "\x2d\x37",
"\xfa\x4d" : "\x2d\x38",
"\xfa\x4e" : "\x2d\x39",
"\xfa\x4f" : "\x2d\x3a",
"\xfa\x50" : "\x2d\x3b",
"\xfa\x51" : "\x2d\x3c",
"\xfa\x52" : "\x2d\x3d",
"\xfa\x53" : "\x2d\x3e",
"\xfa\x54" : "\x22\x4c",
"\xfa\x55" : "\x7c\x7c",
"\xfa\x56" : "\x7c\x7d",
"\xfa\x57" : "\x7c\x7e",
"\xfa\x58" : "\x2d\x6a",
"\xfa\x59" : "\x2d\x62",
"\xfa\x5a" : "\x2d\x64",
"\xfa\x5b" : "\x22\x68",
"\xfa\x5c" : "\x79\x21",
"\xfa\x5d" : "\x79\x22",
"\xfa\x5e" : "\x79\x23",
"\xfa\x5f" : "\x79\x24",
"\xfa\x60" : "\x79\x25",
"\xfa\x61" : "\x79\x26",
"\xfa\x62" : "\x79\x27",
"\xfa\x63" : "\x79\x28",
"\xfa\x64" : "\x79\x29",
"\xfa\x65" : "\x79\x2a",
"\xfa\x66" : "\x79\x2b",
"\xfa\x67" : "\x79\x2c",
"\xfa\x68" : "\x79\x2d",
"\xfa\x69" : "\x79\x2e",
"\xfa\x6a" : "\x79\x2f",
"\xfa\x6b" : "\x79\x30",
"\xfa\x6c" : "\x79\x31",
"\xfa\x6d" : "\x79\x32",
"\xfa\x6e" : "\x79\x33",
"\xfa\x6f" : "\x79\x34",
"\xfa\x70" : "\x79\x35",
"\xfa\x71" : "\x79\x36",
"\xfa\x72" : "\x79\x37",
"\xfa\x73" : "\x79\x38",
"\xfa\x74" : "\x79\x39",
"\xfa\x75" : "\x79\x3a",
"\xfa\x76" : "\x79\x3b",
"\xfa\x77" : "\x79\x3c",
"\xfa\x78" : "\x79\x3d",
"\xfa\x79" : "\x79\x3e",
"\xfa\x7a" : "\x79\x3f",
"\xfa\x7b" : "\x79\x40",
"\xfa\x7c" : "\x79\x41",
"\xfa\x7d" : "\x79\x42",
"\xfa\x7e" : "\x79\x43",
"\xfa\x80" : "\x79\x44",
"\xfa\x81" : "\x79\x45",
"\xfa\x82" : "\x79\x46",
"\xfa\x83" : "\x79\x47",
"\xfa\x84" : "\x79\x48",
"\xfa\x85" : "\x79\x49",
"\xfa\x86" : "\x79\x4a",
"\xfa\x87" : "\x79\x4b",
"\xfa\x88" : "\x79\x4c",
"\xfa\x89" : "\x79\x4d",
"\xfa\x8a" : "\x79\x4e",
"\xfa\x8b" : "\x79\x4f",
"\xfa\x8c" : "\x79\x50",
"\xfa\x8d" : "\x79\x51",
"\xfa\x8e" : "\x79\x52",
"\xfa\x8f" : "\x79\x53",
"\xfa\x90" : "\x79\x54",
"\xfa\x91" : "\x79\x55",
"\xfa\x92" : "\x79\x56",
"\xfa\x93" : "\x79\x57",
"\xfa\x94" : "\x79\x58",
"\xfa\x95" : "\x79\x59",
"\xfa\x96" : "\x79\x5a",
"\xfa\x97" : "\x79\x5b",
"\xfa\x98" : "\x79\x5c",
"\xfa\x99" : "\x79\x5d",
"\xfa\x9a" : "\x79\x5e",
"\xfa\x9b" : "\x79\x5f",
"\xfa\x9c" : "\x79\x60",
"\xfa\x9d" : "\x79\x61",
"\xfa\x9e" : "\x79\x62",
"\xfa\x9f" : "\x79\x63",
"\xfa\xa0" : "\x79\x64",
"\xfa\xa1" : "\x79\x65",
"\xfa\xa2" : "\x79\x66",
"\xfa\xa3" : "\x79\x67",
"\xfa\xa4" : "\x79\x68",
"\xfa\xa5" : "\x79\x69",
"\xfa\xa6" : "\x79\x6a",
"\xfa\xa7" : "\x79\x6b",
"\xfa\xa8" : "\x79\x6c",
"\xfa\xa9" : "\x79\x6d",
"\xfa\xaa" : "\x79\x6e",
"\xfa\xab" : "\x79\x6f",
"\xfa\xac" : "\x79\x70",
"\xfa\xad" : "\x79\x71",
"\xfa\xae" : "\x79\x72",
"\xfa\xaf" : "\x79\x73",
"\xfa\xb0" : "\x79\x74",
"\xfa\xb1" : "\x79\x75",
"\xfa\xb2" : "\x79\x76",
"\xfa\xb3" : "\x79\x77",
"\xfa\xb4" : "\x79\x78",
"\xfa\xb5" : "\x79\x79",
"\xfa\xb6" : "\x79\x7a",
"\xfa\xb7" : "\x79\x7b",
"\xfa\xb8" : "\x79\x7c",
"\xfa\xb9" : "\x79\x7d",
"\xfa\xba" : "\x79\x7e",
"\xfa\xbb" : "\x7a\x21",
"\xfa\xbc" : "\x7a\x22",
"\xfa\xbd" : "\x7a\x23",
"\xfa\xbe" : "\x7a\x24",
"\xfa\xbf" : "\x7a\x25",
"\xfa\xc0" : "\x7a\x26",
"\xfa\xc1" : "\x7a\x27",
"\xfa\xc2" : "\x7a\x28",
"\xfa\xc3" : "\x7a\x29",
"\xfa\xc4" : "\x7a\x2a",
"\xfa\xc5" : "\x7a\x2b",
"\xfa\xc6" : "\x7a\x2c",
"\xfa\xc7" : "\x7a\x2d",
"\xfa\xc8" : "\x7a\x2e",
"\xfa\xc9" : "\x7a\x2f",
"\xfa\xca" : "\x7a\x30",
"\xfa\xcb" : "\x7a\x31",
"\xfa\xcc" : "\x7a\x32",
"\xfa\xcd" : "\x7a\x33",
"\xfa\xce" : "\x7a\x34",
"\xfa\xcf" : "\x7a\x35",
"\xfa\xd0" : "\x7a\x36",
"\xfa\xd1" : "\x7a\x37",
"\xfa\xd2" : "\x7a\x38",
"\xfa\xd3" : "\x7a\x39",
"\xfa\xd4" : "\x7a\x3a",
"\xfa\xd5" : "\x7a\x3b",
"\xfa\xd6" : "\x7a\x3c",
"\xfa\xd7" : "\x7a\x3d",
"\xfa\xd8" : "\x7a\x3e",
"\xfa\xd9" : "\x7a\x3f",
"\xfa\xda" : "\x7a\x40",
"\xfa\xdb" : "\x7a\x41",
"\xfa\xdc" : "\x7a\x42",
"\xfa\xdd" : "\x7a\x43",
"\xfa\xde" : "\x7a\x44",
"\xfa\xdf" : "\x7a\x45",
"\xfa\xe0" : "\x7a\x46",
"\xfa\xe1" : "\x7a\x47",
"\xfa\xe2" : "\x7a\x48",
"\xfa\xe3" : "\x7a\x49",
"\xfa\xe4" : "\x7a\x4a",
"\xfa\xe5" : "\x7a\x4b",
"\xfa\xe6" : "\x7a\x4c",
"\xfa\xe7" : "\x7a\x4d",
"\xfa\xe8" : "\x7a\x4e",
"\xfa\xe9" : "\x7a\x4f",
"\xfa\xea" : "\x7a\x50",
"\xfa\xeb" : "\x7a\x51",
"\xfa\xec" : "\x7a\x52",
"\xfa\xed" : "\x7a\x53",
"\xfa\xee" : "\x7a\x54",
"\xfa\xef" : "\x7a\x55",
"\xfa\xf0" : "\x7a\x56",
"\xfa\xf1" : "\x7a\x57",
"\xfa\xf2" : "\x7a\x58",
"\xfa\xf3" : "\x7a\x59",
"\xfa\xf4" : "\x7a\x5a",
"\xfa\xf5" : "\x7a\x5b",
"\xfa\xf6" : "\x7a\x5c",
"\xfa\xf7" : "\x7a\x5d",
"\xfa\xf8" : "\x7a\x5e",
"\xfa\xf9" : "\x7a\x5f",
"\xfa\xfa" : "\x7a\x60",
"\xfa\xfb" : "\x7a\x61",
"\xfa\xfc" : "\x7a\x62",
"\xfb\x40" : "\x7a\x63",
"\xfb\x41" : "\x7a\x64",
"\xfb\x42" : "\x7a\x65",
"\xfb\x43" : "\x7a\x66",
"\xfb\x44" : "\x7a\x67",
"\xfb\x45" : "\x7a\x68",
"\xfb\x46" : "\x7a\x69",
"\xfb\x47" : "\x7a\x6a",
"\xfb\x48" : "\x7a\x6b",
"\xfb\x49" : "\x7a\x6c",
"\xfb\x4a" : "\x7a\x6d",
"\xfb\x4b" : "\x7a\x6e",
"\xfb\x4c" : "\x7a\x6f",
"\xfb\x4d" : "\x7a\x70",
"\xfb\x4e" : "\x7a\x71",
"\xfb\x4f" : "\x7a\x72",
"\xfb\x50" : "\x7a\x73",
"\xfb\x51" : "\x7a\x74",
"\xfb\x52" : "\x7a\x75",
"\xfb\x53" : "\x7a\x76",
"\xfb\x54" : "\x7a\x77",
"\xfb\x55" : "\x7a\x78",
"\xfb\x56" : "\x7a\x79",
"\xfb\x57" : "\x7a\x7a",
"\xfb\x58" : "\x7a\x7b",
"\xfb\x59" : "\x7a\x7c",
"\xfb\x5a" : "\x7a\x7d",
"\xfb\x5b" : "\x7a\x7e",
"\xfb\x5c" : "\x7b\x21",
"\xfb\x5d" : "\x7b\x22",
"\xfb\x5e" : "\x7b\x23",
"\xfb\x5f" : "\x7b\x24",
"\xfb\x60" : "\x7b\x25",
"\xfb\x61" : "\x7b\x26",
"\xfb\x62" : "\x7b\x27",
"\xfb\x63" : "\x7b\x28",
"\xfb\x64" : "\x7b\x29",
"\xfb\x65" : "\x7b\x2a",
"\xfb\x66" : "\x7b\x2b",
"\xfb\x67" : "\x7b\x2c",
"\xfb\x68" : "\x7b\x2d",
"\xfb\x69" : "\x7b\x2e",
"\xfb\x6a" : "\x7b\x2f",
"\xfb\x6b" : "\x7b\x30",
"\xfb\x6c" : "\x7b\x31",
"\xfb\x6d" : "\x7b\x32",
"\xfb\x6e" : "\x7b\x33",
"\xfb\x6f" : "\x7b\x34",
"\xfb\x70" : "\x7b\x35",
"\xfb\x71" : "\x7b\x36",
"\xfb\x72" : "\x7b\x37",
"\xfb\x73" : "\x7b\x38",
"\xfb\x74" : "\x7b\x39",
"\xfb\x75" : "\x7b\x3a",
"\xfb\x76" : "\x7b\x3b",
"\xfb\x77" : "\x7b\x3c",
"\xfb\x78" : "\x7b\x3d",
"\xfb\x79" : "\x7b\x3e",
"\xfb\x7a" : "\x7b\x3f",
"\xfb\x7b" : "\x7b\x40",
"\xfb\x7c" : "\x7b\x41",
"\xfb\x7d" : "\x7b\x42",
"\xfb\x7e" : "\x7b\x43",
"\xfb\x80" : "\x7b\x44",
"\xfb\x81" : "\x7b\x45",
"\xfb\x82" : "\x7b\x46",
"\xfb\x83" : "\x7b\x47",
"\xfb\x84" : "\x7b\x48",
"\xfb\x85" : "\x7b\x49",
"\xfb\x86" : "\x7b\x4a",
"\xfb\x87" : "\x7b\x4b",
"\xfb\x88" : "\x7b\x4c",
"\xfb\x89" : "\x7b\x4d",
"\xfb\x8a" : "\x7b\x4e",
"\xfb\x8b" : "\x7b\x4f",
"\xfb\x8c" : "\x7b\x50",
"\xfb\x8d" : "\x7b\x51",
"\xfb\x8e" : "\x7b\x52",
"\xfb\x8f" : "\x7b\x53",
"\xfb\x90" : "\x7b\x54",
"\xfb\x91" : "\x7b\x55",
"\xfb\x92" : "\x7b\x56",
"\xfb\x93" : "\x7b\x57",
"\xfb\x94" : "\x7b\x58",
"\xfb\x95" : "\x7b\x59",
"\xfb\x96" : "\x7b\x5a",
"\xfb\x97" : "\x7b\x5b",
"\xfb\x98" : "\x7b\x5c",
"\xfb\x99" : "\x7b\x5d",
"\xfb\x9a" : "\x7b\x5e",
"\xfb\x9b" : "\x7b\x5f",
"\xfb\x9c" : "\x7b\x60",
"\xfb\x9d" : "\x7b\x61",
"\xfb\x9e" : "\x7b\x62",
"\xfb\x9f" : "\x7b\x63",
"\xfb\xa0" : "\x7b\x64",
"\xfb\xa1" : "\x7b\x65",
"\xfb\xa2" : "\x7b\x66",
"\xfb\xa3" : "\x7b\x67",
"\xfb\xa4" : "\x7b\x68",
"\xfb\xa5" : "\x7b\x69",
"\xfb\xa6" : "\x7b\x6a",
"\xfb\xa7" : "\x7b\x6b",
"\xfb\xa8" : "\x7b\x6c",
"\xfb\xa9" : "\x7b\x6d",
"\xfb\xaa" : "\x7b\x6e",
"\xfb\xab" : "\x7b\x6f",
"\xfb\xac" : "\x7b\x70",
"\xfb\xad" : "\x7b\x71",
"\xfb\xae" : "\x7b\x72",
"\xfb\xaf" : "\x7b\x73",
"\xfb\xb0" : "\x7b\x74",
"\xfb\xb1" : "\x7b\x75",
"\xfb\xb2" : "\x7b\x76",
"\xfb\xb3" : "\x7b\x77",
"\xfb\xb4" : "\x7b\x78",
"\xfb\xb5" : "\x7b\x79",
"\xfb\xb6" : "\x7b\x7a",
"\xfb\xb7" : "\x7b\x7b",
"\xfb\xb8" : "\x7b\x7c",
"\xfb\xb9" : "\x7b\x7d",
"\xfb\xba" : "\x7b\x7e",
"\xfb\xbb" : "\x7c\x21",
"\xfb\xbc" : "\x7c\x22",
"\xfb\xbd" : "\x7c\x23",
"\xfb\xbe" : "\x7c\x24",
"\xfb\xbf" : "\x7c\x25",
"\xfb\xc0" : "\x7c\x26",
"\xfb\xc1" : "\x7c\x27",
"\xfb\xc2" : "\x7c\x28",
"\xfb\xc3" : "\x7c\x29",
"\xfb\xc4" : "\x7c\x2a",
"\xfb\xc5" : "\x7c\x2b",
"\xfb\xc6" : "\x7c\x2c",
"\xfb\xc7" : "\x7c\x2d",
"\xfb\xc8" : "\x7c\x2e",
"\xfb\xc9" : "\x7c\x2f",
"\xfb\xca" : "\x7c\x30",
"\xfb\xcb" : "\x7c\x31",
"\xfb\xcc" : "\x7c\x32",
"\xfb\xcd" : "\x7c\x33",
"\xfb\xce" : "\x7c\x34",
"\xfb\xcf" : "\x7c\x35",
"\xfb\xd0" : "\x7c\x36",
"\xfb\xd1" : "\x7c\x37",
"\xfb\xd2" : "\x7c\x38",
"\xfb\xd3" : "\x7c\x39",
"\xfb\xd4" : "\x7c\x3a",
"\xfb\xd5" : "\x7c\x3b",
"\xfb\xd6" : "\x7c\x3c",
"\xfb\xd7" : "\x7c\x3d",
"\xfb\xd8" : "\x7c\x3e",
"\xfb\xd9" : "\x7c\x3f",
"\xfb\xda" : "\x7c\x40",
"\xfb\xdb" : "\x7c\x41",
"\xfb\xdc" : "\x7c\x42",
"\xfb\xdd" : "\x7c\x43",
"\xfb\xde" : "\x7c\x44",
"\xfb\xdf" : "\x7c\x45",
"\xfb\xe0" : "\x7c\x46",
"\xfb\xe1" : "\x7c\x47",
"\xfb\xe2" : "\x7c\x48",
"\xfb\xe3" : "\x7c\x49",
"\xfb\xe4" : "\x7c\x4a",
"\xfb\xe5" : "\x7c\x4b",
"\xfb\xe6" : "\x7c\x4c",
"\xfb\xe7" : "\x7c\x4d",
"\xfb\xe8" : "\x7c\x4e",
"\xfb\xe9" : "\x7c\x4f",
"\xfb\xea" : "\x7c\x50",
"\xfb\xeb" : "\x7c\x51",
"\xfb\xec" : "\x7c\x52",
"\xfb\xed" : "\x7c\x53",
"\xfb\xee" : "\x7c\x54",
"\xfb\xef" : "\x7c\x55",
"\xfb\xf0" : "\x7c\x56",
"\xfb\xf1" : "\x7c\x57",
"\xfb\xf2" : "\x7c\x58",
"\xfb\xf3" : "\x7c\x59",
"\xfb\xf4" : "\x7c\x5a",
"\xfb\xf5" : "\x7c\x5b",
"\xfb\xf6" : "\x7c\x5c",
"\xfb\xf7" : "\x7c\x5d",
"\xfb\xf8" : "\x7c\x5e",
"\xfb\xf9" : "\x7c\x5f",
"\xfb\xfa" : "\x7c\x60",
"\xfb\xfb" : "\x7c\x61",
"\xfb\xfc" : "\x7c\x62",
"\xfc\x40" : "\x7c\x63",
"\xfc\x41" : "\x7c\x64",
"\xfc\x42" : "\x7c\x65",
"\xfc\x43" : "\x7c\x66",
"\xfc\x44" : "\x7c\x67",
"\xfc\x45" : "\x7c\x68",
"\xfc\x46" : "\x7c\x69",
"\xfc\x47" : "\x7c\x6a",
"\xfc\x48" : "\x7c\x6b",
"\xfc\x49" : "\x7c\x6c",
"\xfc\x4a" : "\x7c\x6d",
"\xfc\x4b" : "\x7c\x6e",
}

_kana_fulltohalf = {
u'\u3001':u'\uff64',
u'\u3002':u'\uff61',
u'\u30fb':u'\uff65',
u'\u30fc':u'\uff70',
u'\u300c':u'\uff62',
u'\u300d':u'\uff63',
u'\u30a1':u'\uff67',
u'\u30a2':u'\uff71',
u'\u30a3':u'\uff68',
u'\u30a4':u'\uff72',
u'\u30a5':u'\uff69',
u'\u30a6':u'\uff73',
u'\u30a7':u'\uff6a',
u'\u30a8':u'\uff74',
u'\u30a9':u'\uff6b',
u'\u30aa':u'\uff75',
u'\u30ab':u'\uff76',
u'\u30ac':u'\uff76\uff9e',
u'\u30ad':u'\uff77',
u'\u30ae':u'\uff77\uff9e',
u'\u30af':u'\uff78',
u'\u30b0':u'\uff78\uff9e',
u'\u30b1':u'\uff79',
u'\u30b2':u'\uff79\uff9e',
u'\u30b3':u'\uff7a',
u'\u30b4':u'\uff7a\uff9e',
u'\u30b5':u'\uff7b',
u'\u30b6':u'\uff7b\uff9e',
u'\u30b7':u'\uff7c',
u'\u30b8':u'\uff7c\uff9e',
u'\u30b9':u'\uff7d',
u'\u30ba':u'\uff7d\uff9e',
u'\u30bb':u'\uff7e',
u'\u30bc':u'\uff7e\uff9e',
u'\u30bd':u'\uff7f',
u'\u30be':u'\uff7f\uff9e',
u'\u30bf':u'\uff80',
u'\u30c0':u'\uff80\uff9e',
u'\u30c1':u'\uff81',
u'\u30c2':u'\uff81\uff9e',
u'\u30c3':u'\uff6f',
u'\u30c4':u'\uff82',
u'\u30c5':u'\uff82\uff9e',
u'\u30c6':u'\uff83',
u'\u30c7':u'\uff83\uff9e',
u'\u30c8':u'\uff84',
u'\u30c9':u'\uff84\uff9e',
u'\u30ca':u'\uff85',
u'\u30cb':u'\uff86',
u'\u30cc':u'\uff87',
u'\u30cd':u'\uff88',
u'\u30ce':u'\uff89',
u'\u30cf':u'\uff8a',
u'\u30d0':u'\uff8a\uff9e',
u'\u30d1':u'\uff8a\uff9f',
u'\u30d2':u'\uff8b',
u'\u30d3':u'\uff8b\uff9e',
u'\u30d4':u'\uff8b\uff9f',
u'\u30d5':u'\uff8c',
u'\u30d6':u'\uff8c\uff9e',
u'\u30d7':u'\uff8c\uff9f',
u'\u30d8':u'\uff8d',
u'\u30d9':u'\uff8d\uff9e',
u'\u30da':u'\uff8d\uff9f',
u'\u30db':u'\uff8e',
u'\u30dc':u'\uff8e\uff9e',
u'\u30dd':u'\uff8e\uff9f',
u'\u30de':u'\uff8f',
u'\u30df':u'\uff90',
u'\u30e0':u'\uff91',
u'\u30e1':u'\uff92',
u'\u30e2':u'\uff93',
u'\u30e3':u'\uff6c',
u'\u30e4':u'\uff94',
u'\u30e5':u'\uff6d',
u'\u30e6':u'\uff95',
u'\u30e7':u'\uff6e',
u'\u30e8':u'\uff96',
u'\u30e9':u'\uff97',
u'\u30ea':u'\uff98',
u'\u30eb':u'\uff99',
u'\u30ec':u'\uff9a',
u'\u30ed':u'\uff9b',
u'\u30ef':u'\uff9c',
u'\u30f2':u'\uff66',
u'\u30f3':u'\uff9d',
u'\u30f4':u'\uff73\uff9e',
}

_kana_halftofull = dict((v, k) for k, v in _kana_fulltohalf.items())


_fulltohalf = {
u'\uff01':u'!',	# EXCLAMATION MARK
u'\uff02':u'"',	# QUOTATION MARK
u'\uff03':u'#',	# NUMBER SIGN
u'\uff04':u'$',	# DOLLAR SIGN
u'\uff05':u'%',	# PERCENT SIGN
u'\uff06':u'&',	# AMPERSAND
u'\uff07':u"'",	# APOSTROPHE
u'\uff08':u'(',	# LEFT PARENTHESIS
u'\uff09':u')',	# RIGHT PARENTHESIS
u'\uff0a':u'*',	# ASTERISK
u'\uff0a':u'*',	# FORMS LIGHT VERTICAL
u'\uff0b':u'+',	# PLUS SIGN
u'\uff0c':u',',	# COMMA
u'\uff0d':u'-',	# HYPHEN-MINUS
u'\uff0e':u'.',	# FULL STOP
u'\uff0f':u'/',	# SOLIDUS
u'\uff10':u'0',	# DIGIT ZERO
u'\uff11':u'1',	# DIGIT ONE
u'\uff12':u'2',	# DIGIT TWO
u'\uff13':u'3',	# DIGIT THREE
u'\uff14':u'4',	# DIGIT FOUR
u'\uff15':u'5',	# DIGIT FIVE
u'\uff16':u'6',	# DIGIT SIX
u'\uff17':u'7',	# DIGIT SEVEN
u'\uff18':u'8',	# DIGIT EIGHT
u'\uff19':u'9',	# DIGIT NINE
u'\uff1a':u':',	# COLON
u'\uff1b':u';',	# SEMICOLON
u'\uff1c':u'<',	# LESS-THAN SIGN
u'\uff1d':u'=',	# EQUALS SIGN
u'\uff1e':u'>',	# GREATER-THAN SIGN
u'\uff1f':u'?',	# QUESTION MARK
u'\uff20':u'@',	# COMMERCIAL AT
u'\uff21':u'A',	# LATIN CAPITAL LETTER A
u'\uff22':u'B',	# LATIN CAPITAL LETTER B
u'\uff23':u'C',	# LATIN CAPITAL LETTER C
u'\uff24':u'D',	# LATIN CAPITAL LETTER D
u'\uff25':u'E',	# LATIN CAPITAL LETTER E
u'\uff26':u'F',	# LATIN CAPITAL LETTER F
u'\uff27':u'G',	# LATIN CAPITAL LETTER G
u'\uff28':u'H',	# LATIN CAPITAL LETTER H
u'\uff29':u'I',	# LATIN CAPITAL LETTER I
u'\uff2a':u'J',	# LATIN CAPITAL LETTER J
u'\uff2b':u'K',	# LATIN CAPITAL LETTER K
u'\uff2c':u'L',	# LATIN CAPITAL LETTER L
u'\uff2d':u'M',	# LATIN CAPITAL LETTER M
u'\uff2e':u'N',	# LATIN CAPITAL LETTER N
u'\uff2f':u'O',	# LATIN CAPITAL LETTER O
u'\uff30':u'P',	# LATIN CAPITAL LETTER P
u'\uff31':u'Q',	# LATIN CAPITAL LETTER Q
u'\uff32':u'R',	# LATIN CAPITAL LETTER R
u'\uff33':u'S',	# LATIN CAPITAL LETTER S
u'\uff34':u'T',	# LATIN CAPITAL LETTER T
u'\uff35':u'U',	# LATIN CAPITAL LETTER U
u'\uff36':u'V',	# LATIN CAPITAL LETTER V
u'\uff37':u'W',	# LATIN CAPITAL LETTER W
u'\uff38':u'X',	# LATIN CAPITAL LETTER X
u'\uff39':u'Y',	# LATIN CAPITAL LETTER Y
u'\uff3a':u'Z',	# LATIN CAPITAL LETTER Z
u'\uff3b':u'[',	# LEFT SQUARE BRACKET
u'\uff3c':u'\\',	# REVERSE SOLIDUS
u'\uff3d':u']',	# RIGHT SQUARE BRACKET
u'\uff3e':u'^',	# CIRCUMFLEX ACCENT
u'\uff3f':u'_',	# LOW LINE
u'\uff40':u'`',	# GRAVE ACCENT
u'\uff41':u'a',	# LATIN SMALL LETTER A
u'\uff42':u'b',	# LATIN SMALL LETTER B
u'\uff43':u'c',	# LATIN SMALL LETTER C
u'\uff44':u'd',	# LATIN SMALL LETTER D
u'\uff45':u'e',	# LATIN SMALL LETTER E
u'\uff46':u'f',	# LATIN SMALL LETTER F
u'\uff47':u'g',	# LATIN SMALL LETTER G
u'\uff48':u'h',	# LATIN SMALL LETTER H
u'\uff49':u'i',	# LATIN SMALL LETTER I
u'\uff4a':u'j',	# LATIN SMALL LETTER J
u'\uff4b':u'k',	# LATIN SMALL LETTER K
u'\uff4c':u'l',	# LATIN SMALL LETTER L
u'\uff4d':u'm',	# LATIN SMALL LETTER M
u'\uff4e':u'n',	# LATIN SMALL LETTER N
u'\uff4f':u'o',	# LATIN SMALL LETTER O
u'\uff50':u'p',	# LATIN SMALL LETTER P
u'\uff51':u'q',	# LATIN SMALL LETTER Q
u'\uff52':u'r',	# LATIN SMALL LETTER R
u'\uff53':u's',	# LATIN SMALL LETTER S
u'\uff54':u't',	# LATIN SMALL LETTER T
u'\uff55':u'u',	# LATIN SMALL LETTER U
u'\uff56':u'v',	# LATIN SMALL LETTER V
u'\uff57':u'w',	# LATIN SMALL LETTER W
u'\uff58':u'x',	# LATIN SMALL LETTER X
u'\uff59':u'y',	# LATIN SMALL LETTER Y
u'\uff5a':u'z',	# LATIN SMALL LETTER Z
u'\uff5b':u'{',	# LEFT CURLY BRACKET
u'\uff5c':u'|',	# VERTICAL LINE
u'\uff5d':u'}',	# RIGHT CURLY BRACKET
u'\uff5e':u'~',	# TILDE
u'\uffe0':u'\xa2',	# CENT SIGN
u'\uffe1':u'\xa3',	# POUND SIGN
u'\uffe2':u'\xac',	# NOT SIGN
u'\uffe5':u'\\',	# YEN SIGN
}

_halftofull = dict((v, k) for k, v in _fulltohalf.items())


def _is_jis(c):
     return '\x21' <= c <= '\x7e'

def _is_euc(c):
     return '\xa1' <= c <= '\xfe'

def _is_gaiji1(c):
     return '\xf0' <= c <= '\xf9'

def _is_ibmgaiji1(c):
    return '\xfa' <= c <= '\xfc'

def _is_sjis1(c):
     if '\x81' <= c <= '\x9f':
         return True
     if '\xe0' <= c <= '\xef':
         return True
     if _is_gaiji1(c) or _is_ibmgaiji1(c):
         return True

def _is_sjis2(c):
    return ('\x40' <= c <= '\xfc') and (c != '\x7f')
    
def _is_half_kana(c):
    return '\xa0' <= c <= '\xdf'

def _utf8_len(c):
    if '\xc0' <= c <= '\xdf': return 2
    if '\xe0' <= c <= '\xef': return 3
    if '\xf0' <= c <= '\xf7': return 4
    if '\xf8' <= c <= '\xfb': return 5
    if '\xfc' <= c <= '\xfd': return 6
    return 0

def _is_utf8_trail(c):
    return '\x80' <= c <= '\xbf'

def _jis_to_sjis(h, l):
    if h & 1:
        if l < 0x60:
            l += 0x1f
        else:             
            l += 0x20
    else:
        l += 0x7e

    if h < 0x5f:
        h = (h + 0xe1) >> 1
    else:
        h = (h + 0x161) >> 1
    
    return chr(h & 0xff)+chr(l & 0xff)


def _jis_to_mskanji(h, l):
    c = h+l
    if c in _tbl_jis2mskanji:
        return _tbl_jis2mskanji[c]
    else:
        return _jis_to_sjis(ord(h), ord(l))

def _sjis_to_jis(h, l):
    if h < 0x9f:
        if l < 0x9f:
            h = (h << 1) - 0xe1
        else:
            h = (h << 1) - 0xe0
    else:
        if l < 0x9f:
            h = (h << 1) - 0x161
        else:
            h = (h << 1) - 0x160
    
    if l < 0x7f:
        l -= 0x1f
    elif l < 0x9f:
        l -= 0x20
    else:
        l -= 0x7e
    
    return chr(h & 0xff)+chr(l & 0xff)


def _mskanji_to_jis(h, l):
    c = h+l
    if _is_gaiji1(c):
        return CONV_FAILED

    if c in _tbl_mskanji2jis:
        return _tbl_mskanji2jis[c]
    else:
        return _sjis_to_jis(ord(h), ord(l))
    

def guess(s):
    # check BOM
    bom = s[:2]
    if bom == "\xff\xfe":
        return UTF16_LE
    if bom == "\xfe\xff":
        return UTF16_BE
    if s[:3] == "\xef\xbb\xbf":
        return UTF8
    
    # check JIS
    if '\x1b' in s:
        return JIS

    # check ascii
    if max(s) < '\x80':
        return ASCII

    ascii = 1
    sjis = jis = euc = utf8 = 0
    bad_ascii = bad_sjis = bad_euc = bad_utf8 = 0
    sjis_error = euc_error = utf8_error = 0
    slen = len(s)

    # check SJIS
    i = 0
    halfkana = 0
    while i < slen:
        c = s[i]
        if _is_half_kana(c):
            # half-kana
            sjis += 7
            halfkana += 1
        else:
            if halfkana == 1:
                # single halfwidth-kana is bad sign.
                    bad_sjis += 7
            halfkana = 0
            
            if _is_sjis1(c):
                if c == '\x8e':
                    # looks like euc.
                    bad_sjis += 10

                if (i+1 < slen) and _is_sjis2(s[i+1]):
                    sjis += 16
                    i += 1
                else:
                    sjis_error = 1
                    break
            elif c >= '\x80':
                sjis_error = 1
                break
        i += 1
        

    # check EUC
    i = 0
    halfkana = 0
    while i < slen:
        c = s[i]
        if c == '\x8e':
            if (i+1 < slen) and _is_half_kana(s[i+1]):
                euc += 8
                i += 1
                halfkana += 1
            else:
                euc_error = 1
                break
        else:
            if halfkana == 1:
                bad_euc += 5
            halfkana = 0

            if _is_euc(c):
                if (i+1 < slen) and _is_euc(s[i+1]):
                    euc += 16
                    i += 1
                else:
                    euc_error = 1
                    break
            elif c == '\x8f':
                if (i+2 < slen) and _is_euc(s[i+1]) and _is_euc(s[i+2]):
                    euc += 16
                    i += 2
                else:
                    euc_error = 1
                    break
            elif c >= '\x80':
                euc_error = 1
                break

        i += 1

    # check UTF8
    i = 0
    halfkana = 0
    while i < slen:
        c = s[i]
        clen = _utf8_len(c)
        if clen:
            if i+clen-1 >= slen:
                utf8_error = 1
                break

            for j in xrange(i+1, i+clen):
                if not _is_utf8_trail(s[j]):
                    utf8_error = 1
                    break
            
            if utf8_error:
                break
            
            utf8 += 16*(clen*2//3)+1
            i += clen

        elif c >= '\x80':
            utf8_error = 1
            break
        
        else:
            i += 1

#    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
#    print sjis_error, bad_sjis, sjis
#    print euc_error, bad_euc, euc
#    print utf8_error, bad_utf8, utf8

    if sjis_error and euc_error and utf8_error:
        return UNKNOWN

    if sjis_error:
        if euc_error:
            return UTF8
        elif utf8_error:
            return EUC
        if euc-bad_euc > utf8-bad_utf8:
            return EUC
        else:
            return UTF8
            
    if euc_error:
        if sjis_error:
            return UTF8
        elif utf8_error:
            return SJIS
        if sjis-bad_sjis > utf8-bad_utf8:
            return SJIS
        else:
            return UTF8
            
    if utf8_error:
        if sjis_error:
            return EUC
        elif sjis_error:
            return EUC
        if sjis-bad_sjis > euc-bad_euc:
            return SJIS
        else:
            return EUC
    
    if sjis-bad_sjis >= euc-bad_euc:
        if utf8-bad_utf8 >= sjis-bad_sjis:
            return UTF8
        else:
            return SJIS
    else:
        if utf8-bad_utf8 >= euc-bad_euc:
            return UTF8
        else:
            return EUC


def euctosjis(s):
    ret = []
    slen = len(s)
    i = 0
    while i < slen:
        if (i+1 < slen) and _is_euc(s[i]) and _is_euc(s[i+1]):
            c1 = ord(s[i]) & 0x7f
            c2 = ord(s[i+1]) & 0x7f
            ret.append(_jis_to_mskanji(chr(c1), chr(c2)))
            i += 2
        elif (i+1 < slen) and s[i] == '\x8e' and _is_half_kana(s[i+1]):
            ret.append(s[i+1])
            i += 2
        else:
            ret.append(s[i])
            i += 1
    return "".join(ret)


def jistosjis(s):
    ret = []
    slen = len(s)
    i = 0
    NORMAL, KANJI, HALFKANA = range(0, 3)
    mode = NORMAL
    
    while i < slen:
        if s[i:i+3] in ("\x1b$@", "\x1b$B"):
            mode = KANJI
            i += 3
        elif s[i:i+4] == "\x1b$(O":
            mode = KANJI
            i += 4
        elif s[i:i+3] in ("\x1b(B", "\x1b(J"):
            mode = NORMAL;
            i += 3
        elif s[i:i+3] == "\x1b(I":
            mode = HALFKANA
            i += 3
        elif s[i] == '\x0e':
            mode = HALFKANA
            i += 1
        elif s[i] == '\x0f':
            mode = NORMAL
            i += 1
        elif mode == KANJI and (i+1) < slen:
            ret.append(_jis_to_mskanji(s[i], s[i+1]))
            i += 2
        elif mode == HALFKANA:
            ret.append(chr((ord(s[i]) | 0x80) & 0xff))
            i += 1
        else:
            ret.append(s[i])
            i += 1
    return "".join(ret)



def sjistoeuc(s):
    ret = []
    slen = len(s)
    i = 0
    
    while i < slen:
        if _is_sjis1(s[i]) and (i+1) < slen:
            c1, c2 = _mskanji_to_jis(s[i], s[i+1])
            ret.append(chr((ord(c1) | 0x80) & 0xff))
            ret.append(chr((ord(c2) | 0x80) & 0xff))
            i += 2
        elif _is_half_kana(s[i]):
            ret.append("\x8e")
            ret.append(s[i])
            i += 1
        else:
            ret.append(s[i])
            i += 1

    return "".join(ret)
    
def sjistojis(s):
    ret = []
    slen = len(s)
    i = 0

    NORMAL, KANJI, HALFKANA = range(0, 3)
    mode = NORMAL
    
    while i < slen:
        if _is_sjis1(s[i]) and (i+1) < slen:
            c1, c2 = _mskanji_to_jis(s[i], s[i+1])
            if mode != KANJI:
                mode = KANJI;
                ret.append("\x1b$B")

            ret.append(c1)
            ret.append(c2)
            i += 2

        elif _is_half_kana(s[i]):
            if mode != HALFKANA:
                mode = HALFKANA;
                ret.append("\x1b(I")
                
            ret.append(chr(ord(s[i]) & 0x7f))
            i += 1

        else:
            if mode != NORMAL:
                mode = NORMAL
                ret.append("\x1b(B")

            ret.append(s[i])
            i += 1
    
    if mode != NORMAL:
        ret.append("\x1b(B")
            
    return "".join(ret)


def jistoeuc(s):
    return sjistoeuc(jistosjis(s))

def euctojis(s):
    return sjistojis(euctosjis(s))

def _callsub(s, _re, d):
    if not isinstance(s, unicode):
        raise TypeError("argument 1 must be unicode, not %s" % type(s))

    def _rep(m, d=d):
        c = m.group(0)
        return d[c]
    return _re.sub(_rep, s)

_re_kana_full = re.compile(
    u"|".join(u'%s' % c for c in _kana_fulltohalf.keys()))

def kanatohalf(s):
    return _callsub(s, _re_kana_full, _kana_fulltohalf)

_re_kana_half = re.compile(
    u"|".join(u'%s' % c for c in _kana_halftofull.keys()))

def kanatofull(s):
    return _callsub(s, _re_kana_half, _kana_halftofull)

_re_full = re.compile(
    u"|".join(u'%s' % re.escape(c) for c in _halftofull.keys()))
def tofull(s):
    return _callsub(s, _re_full, _halftofull)

_re_half = re.compile(
    u"|".join(u'%s' % re.escape(c) for c in _fulltohalf.keys()))
def tohalf(s):
    return _callsub(s, _re_half, _fulltohalf)



_from_dates = [
    (1868, 1, 1),
    (1912, 7, 30),
    (1926, 12, 25),
    (1989, 1, 8)
]
_nengo = [
u" ",
u'\u660e\u6cbb',
u'\u5927\u6b63',
u'\u662d\u548c',
u'\u5e73\u6210',
]

_nengo_c = u" MTSH"

def getnengo(y, m, d, letter=False):
    if y < 1868:
        raise ValueError()
        
    n = bisect.bisect(_from_dates, (y, m, d))
    if letter:
        nengo = _nengo_c[n]
    else:
        nengo = _nengo[n]
    return nengo, y - _from_dates[n-1][0] + 1


def heiseitoyear(h):
    if h <= 0: raise ValueError()
    return 1989+h-1


def showatoyear(s):
    if s <= 0: raise ValueError()
    return 1926+s-1


def taishotoyear(t):
    if t <= 0: raise ValueError()
    return 1912+t-1


def meijitoyear(m):
    if m <= 0: raise ValueError()
    return 1868+m-1


_re_word = re.compile(ur".[。、,.!;]|\w+|.")

def _splitword(s):
    # todo: surrogate pair/combining character(e.g. U+309A)
    slen = len(s)
    f = pos = 0
    for m in _re_word.finditer(s):
        yield m.group()

def _calccols(s):
    d = {'Na':1, 'N':1, 'H':1, 'W':2, 'F':2, 'A':2}
    ret = [d[unicodedata.east_asian_width(c)] for c in s]
    return ret

    
def wrap(s, maxcol):
    if not isinstance(s, unicode):
        raise TypeError("argument 1 must be unicode, not %s" % type(s))
    if maxcol < 1:
        raise ValueError("maxcol should be greater than zero")
        
    lines = s.splitlines()
    for line in lines:
        words = []
        col = 0
        for word in _splitword(line):
            cols = _calccols(word)
            wordlen = sum(cols)
            if col+wordlen > maxcol:
                if col > 0:
                    yield u"".join(words)
                    col = 0
                    words = []

                for char, w in zip(word, cols):
                    words.append(char)
                    col += w
                    if col >= maxcol:
                        yield u"".join(words)
                        col = 0
                        words = []
            else:
                words.append(word)
                col += wordlen
        if col:
            yield u"".join(words)

