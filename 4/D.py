#!/bin/env python
import re
import sys
import argparse
import unittest
from itertools import groupby
from random import choice, randint


def check_positive(x):
    y = int(x)
    if y <= 0:
        raise argparse.ArgumentTypeError(
                '%s is ' % x + 'an invalid positive int value')
    return y


def tokenize(text):
    r = re.compile('[^\W\d_]+|\d+|\n|\W', re.UNICODE)
    return re.findall(r, text)


def group_by_endline(tokens):
    return [list(g) for k, g in groupby(tokens, lambda x: x == '\n') if not k]


def get_chains_endings(tokens, depth, regexp):
    proba = {}
    tokens = list(filter(lambda x: regexp.match(x), tokens))
    lines = group_by_endline(tokens)
    for size in range(depth + 1):
        for line in lines:
            for start in range(0, len(line) - size):
                current_chain = ' '.join(line[start:start + size])
                post_tokens = proba.get(current_chain, [])
                post_tokens.append(line[start + size])
                proba[current_chain] = post_tokens
    return proba


def count_words_proba(tokens, depth):
    r = re.compile('[^\W\d_]+|\n', re.UNICODE)
    proba = get_chains_endings(tokens, depth, r)
    for key in proba:
        current = sorted(proba[key])
        l = len(current)
        proba[key] = [(k, len(list(g)) * 1. / l) for k, g in groupby(current)]
    return proba


def generate(tokens, depth, size):
    r = re.compile('[^\W\d_]+|\d+|[,.:;!?]|\n', re.UNICODE)
    endings = get_chains_endings(tokens, depth, r)
    new_text = []
    current_length = 0
    line = []
    while current_length <= size:
        # trying to find completion token for random size chain
        while True:
            if current_length > size:
                break
            # If it's the beginning of the line we should pick small
            # window_size otherwise it should be big enough
            # to generate sth with sense
            window_size = randint(min(depth // 3, len(line)), depth)
            chain = ' '.join(line[current_length - window_size:current_length])
            if chain in endings:
                next_word = choice(endings[chain])
                # we should generate new separators only after words
                sep = re.compile('[,.!?:;]')
                if (len(line) == 0 or sep.match(line[-1])) and sep.match(
                                                               next_word):
                    continue
                line.append(next_word)
                # if it's the end of the sentence and text length bigger
                # size we should finish
                if re.match('[.!?;]', next_word) and current_length > size:
                    break
                current_length += 1
            elif window_size > 2 * depth // 3:
                # we can't generate word even with wide window
                # so it's the end of the line
                new_text.append(line)
                line = []
    new_text.append(line)
    return new_text


class Test(unittest.TestCase):
    def test_tokenize(self):
        text = 'Hello, world!'
        tokens = list(filter(lambda x: x != '\n', tokenize(text)))
        valid_tokens = ['Hello', ',', ' ', 'world', '!']
        self.assertListEqual(tokens, valid_tokens)

    def test_tokenize_empty(self):
        text = ''
        tokens = list(filter(lambda x: x != '\n', tokenize(text)))
        valid_tokens = []
        self.assertListEqual(tokens, valid_tokens)

    def test_tokenize_digits(self):
        text = 'Hello 123 321\nworld!'
        tokens = list(filter(lambda x: x != '\n', tokenize(text)))
        valid_tokens = ['Hello', ' ', '123', ' ', '321', 'world', '!']
        self.assertListEqual(tokens, valid_tokens)

    def test_tokenize_separators(self):
        text = '.,:\n;!?'
        tokens = list(filter(lambda x: x != '\n', tokenize(text)))
        valid_tokens = ['.', ',', ':', ';', '!', '?']
        self.assertListEqual(tokens, valid_tokens)

    def test_probabilities(self):
        text = 'First test sentence\nSecond test line'
        probs = count_words_proba(tokenize(text), 1)
        valid_probs = {}
        valid_probs[''] = [('First', 1./6), ('Second', 1./6),
                           ('line', 1./6), ('sentence', 1./6), ('test', 1./3)]
        valid_probs['Second'] = [('test', 1.0)]
        valid_probs['test'] = [('line', 0.5), ('sentence', 0.5)]
        valid_probs['First'] = [('test', 1.0)]
        self.assertDictEqual(probs, valid_probs)

    def test_probabilities_one_word(self):
        text = 'test test test'
        probs = count_words_proba(tokenize(text), 2)
        valid_probs = {}
        valid_probs[''] = [('test', 1.)]
        valid_probs['test'] = [('test', 1.0)]
        valid_probs['test test'] = [('test', 1.)]
        self.assertDictEqual(probs, valid_probs)

    def test_probabilities_empty(self):
        text = ''
        probs = count_words_proba(tokenize(text), 1)
        valid_probs = {}
        self.assertDictEqual(probs, valid_probs)

    def test_probabilities_two_lines(self):
        text = 'one word one\n word'
        probs = count_words_proba(tokenize(text), 2)
        valid_probs = {}
        valid_probs[''] = [('one', 0.5), ('word', 0.5)]
        valid_probs['one'] = [('word', 1.)]
        valid_probs['word'] = [('one', 1.)]
        valid_probs['one word'] = [('one', 1.)]
        self.assertDictEqual(probs, valid_probs)

    def test_generate(self):
        text = 'a a a'
        tokens = tokenize(text)
        generated = generate(tokens, 2, 5)
        self.assertListEqual(generated, [['a', 'a', 'a', 'a', 'a', 'a']])


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar={
        'tokenize', 'probabilities', 'generate', 'test'}, dest='command')
    parser_tokenize = subparsers.add_parser('tokenize')

    parser_prob = subparsers.add_parser('probabilities')
    parser_prob.add_argument('--depth', type=check_positive, required=True)

    parser_gen = subparsers.add_parser('generate')
    parser_gen.add_argument('--depth', type=check_positive, required=True)
    parser_gen.add_argument('--size', type=check_positive, required=True)

    parser_test = subparsers.add_parser('test')

    args = parser.parse_args(input().split())

    text = sys.stdin.read()
    tokens = tokenize(text)

    if args.command == 'tokenize':
        tokens = list(filter(lambda x: x != '\n', tokens))
        print(*tokens, sep='\n')
        return

    if args.command == 'probabilities':
        proba = count_words_proba(tokens, args.depth)
        for chain in sorted(proba):
            print(chain)
            for k, v in proba[chain]:
                print('  {}: {:.2f}'.format(k, v))
        return

    if args.command == 'generate':
        generated = [' '.join(line) for line in generate(
                            tokens, args.depth, args.size)]
        for line in generated:
            if line[-1] == ',':
                line = line[:-2]
        new_text = '. '.join(generated)
        print(new_text)
        return

    if args.command == 'test':
        unittest.main()
        return


if __name__ == '__main__':
    main()
