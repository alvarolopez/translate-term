ranslate-term
======

Command-line translator relying on [WordReference](http://wordreference.com)
for translation and coded in Python.

After several years of being disappointed with google translate, I discovered
the website [WordReference](http://wordreference.com), which offers far better
translations for about any word. What I particularly enjoy is the fact that it
tries to translate all the variations in meaning, as words don't necessarily
match perfectly. And it also works fairly well with expressions.

So, since I'm a sucker for everything related to terminals, I came up with this
little tool. Nothing fancy, just good translation at the fingertip

Install
------

You can install directly this package with pip:
```
pip install translate-term
```

Usage
------

You simply need to call it from a terminal with the `translate [dict] [word]`
syntax. 

- The `dict` argument is a 4 letter string, the first two letters being 
the key corresponding to the initial language and the last 2 the key to the
language to translate to
- The `word` argument is the word or expression to be translated. If the case
  of an expression, remember to put quotes around it.

For example, if you want to translate 'speak' from English to French, you need
to type:
```
translate enfr speak
```

And if you want to translate an expression:
```
translate enfr "speak out"
```

If you want the list of available dictionaries, just pass the `-l` or `--list`
argument:
```
translate -l
translate --list
```

Any doute, just call for `--help`!:
```
translate -h
translate --help
```

Note
------

This utility doesn't rely on any API, so there is practically no limit in the
number of translations that you can perform.

There are a few strange characters that appear here and there. They come from
the html, and I'm too lazy to handle them.

Also you might notice that the returned table doesn't include all the results
that you would find on the website. That is completely intentional. The
objective of this utility is to present a large enough variations of a a word,
without displaying the whole dictionary either. It also helps limiting the
width of the table, which becomes a mess if it is too wide.

