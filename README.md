# riotjs-gettext

A class based implementation of Django's gettext functions

A RiotJS implemetation of Django's gettext functions

## Why

This project is a modern implemetation of gettext function ({n,p}gettext) as an ES6 class and (optionally) a RiotJS 5 tag. It's set up as a Django project and the intention is to interface it with Rosetta.

## Usage

### Setting Up

In webpack, you should alias 'Gettext' to the src path of this repo
```
    resolve: {
        alias: {
            ...
            Gettext: path.resolve(__dirname, "gettext_utils/src"),
            ...
        }
    },
```

### Use As An ES6 Class

The core of this project is the `Catalog` class. This contains js code adapted from the Django Project's js cataloguing code to generate translation strings with optionally plural forms and/or context markers.

To use as an ES6 class, import it into your component and instantiate with a list of strings. This example catalog demonstrates possible formats for strings in the catalog. It's intended to be broadly compatible with Django's javascript catalog generator.
```
import Catalog from "Gettext/js/catalog";

const tet = new Catalog({
    'Activity': 'Actividade',
    'Project': 'Projetu',
    'verb\x04may': 'bele',
    'month\x04may': 'maiu',
    'animal\x04Elephant': 'Amimal abu-abu neebe boot',
    'There is one activity': ['Iha atividade ida', 'Iha atividade barak'],
    'foo\x04There is one activity': ['Iha foo ida', 'Iha foo barak'],
    'bar\x04There is one activity': ['Iha bar ida', 'Iha bar barak'],
    'There is %(total)s object. Remaining: %(count)s': ['Iha %(total)s objetu. Restu mak: %(count)s', 'Iha %(total)s objetu sira. Restu mak: %(count)s'],
    'I caught %s pocket monster!. Remaining: %s': ["Hau kaer %s pokemon deit!. Sei livre: %s", "Hau kaer %s pokemon! Sei livre: %s"]
})
```

The catalog class above exposes a public method, "translate". This takes a number of parameters in order of approximately most important to least important.
