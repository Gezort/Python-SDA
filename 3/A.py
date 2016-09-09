#!/bin/env python
import argparse
import sys

picsels = {0: '@', 1: '%', 2: '#', 3: '*', 4: '+',
           5: '=', 6: '-', 7: ':', 8: '.', 9: ' '}
picsels_codes = {'@': 0, '%': 1, '#': 2, '*': 3, '+': 4,
                 '=': 5, '-': 6, ':': 7, '.': 8, ' ': 9}


def crop(image, left, right, top, bottom):
    result = []
    for row in image[top: len(image) - bottom]:
        result.append(row[left: len(row) - right])
    return result


def expose(image, brightness):
    for i in range(len(image)):
        new_row = ''
        for j in range(len(image[0])):
            code = picsels_codes[image[i][j]]
            code = min(9, code + brightness)
            code = max(code, 0)
            new_row += picsels[code]
        image[i] = new_row
    return image


def rotate(image, angle):
    for k in range(angle // 90):
        result = ['' for i in range(len(image[0]))]
        for row in image:
            for j in range(len(row)):
                result[len(row) - j - 1] += row[j]
        image = result
    return image


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar={'crop', 'expose', 'rotate'},
                                       dest='command')

    parser_crop = subparsers.add_parser('crop')
    parser_crop.add_argument('-l', '--left', type=int,
                             default=0, help='padding left')
    parser_crop.add_argument('-r', '--right', type=int,
                             default=0, help='padding right')
    parser_crop.add_argument('-t', '--top', type=int,
                             default=0, help='padding top')
    parser_crop.add_argument('-b', '--bottom', type=int,
                             default=0, help='padding bottom')

    parser_expose = subparsers.add_parser('expose')
    parser_expose.add_argument('brightness', type=int)

    parser_rotate = subparsers.add_parser('rotate')
    parser_rotate.add_argument('angle', type=int, choices=[0, 90, 180, 270])

    args = parser.parse_args(input().split())

    if not args.command:
        parser.error("One of crop or expose or rotate must be given")

    image = []
    for row in sys.stdin:
        image.append(row[:-1])

    if args.command == 'crop':
        image = crop(image, args.left,  args.right, args.top, args.bottom)
    elif args.command == 'expose':
        image = expose(image, args.brightness)
    else:
        image = rotate(image, args.angle)

    for row in image:
        print(row)

if __name__ == '__main__':
    main()
