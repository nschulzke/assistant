from lark import Lark, Tree
from datasets import Dataset

# Grammar to tokenize input and extract token tags as if they were markdown links
grammar = Lark('''
    start: (link | text)*
    link: "[" tagged_tokens "]" "(" tag ")"
    text: TOKEN*
    tagged_tokens: TOKEN*
    tag: TOKEN
    TOKEN: /([a-zA-Z]|[0-9]|[.,;:!?'"-])+/
    %import common.CNAME
    %ignore " "
    %ignore "\\n"
''')


def traverse(tree, parent):
    """In-order traversal of the lark parse tree"""
    if isinstance(tree, Tree):
        if tree.data.value == 'text':
            for child in tree.children:
                yield from traverse(child, '0')
        elif tree.data.value == 'link':
            yield from traverse(tree.children[0], tree.children[1].children[0].value)
        else:
            for child in tree.children:
                yield from traverse(child, parent)
    else:
        yield tree.value, parent


def parse_prompts(list):
    """Traverse the tree and return the list of unique tags and the sorted list"""
    data = []
    unique_tags = []
    for prompt in list:
        tree = grammar.parse(prompt)
        tags = []
        tokens = []
        for token, tag in traverse(tree, None):
            if tag not in unique_tags:
                unique_tags.append(tag)
            tags.append(unique_tags.index(tag))
            tokens.append(token)
        data.append((tokens, tags))
    return {
        'data': [{'tokens': tokens, 'tags': tags} for tokens, tags in data],
        'unique_tags': {key: value for key, value in enumerate(unique_tags)}
    }
