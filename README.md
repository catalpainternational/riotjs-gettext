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

The catalog class above exposes a public method, "translate". This takes a number of parameters in order of approximately most important to least important. It also has public methods with the same sig as Django's implemetation for five additional functions:

 - gettext
 - ngettext
 - pgettext
 - npgettext
 - interpolate

### Use As A Riot Module

The simplest example of a complete Riot tag is as follows:
```html
<parent-tag>
    <trans-late catalog="{ state.catalog }" msgid="Project"/>
    <script>
        import TransLate from "Gettext/tags/trans_late.riot";
        import Catalog from "Gettext/js/catalog";

        export default {
            components: {
                TransLate
            },
            onBeforeMount(props, state) {
                state.catalog = new Catalog({
                    'Project': 'Projetu',
                })
            }
        }

    </script>
</parent-tag>
```

Note that the equivalent could be achieved using the Catalog class only:

```html
<parent-tag>
    { state.catalog.gettext("Project") }
    <script>
        import TransLate from "Gettext/tags/trans_late.riot";
        import Catalog from "Gettext/js/catalog";
        const tet = new Catalog({
            'Project': 'Projetu',
        })
    </script>
</parent-tag>
```
This method allows to replace text in othet situations, such as within tag attributes.


# Setting Up Translations

To write translations, this module currently uses an intermediate Python file listing the required translations

Step 1: Write to python
`./manage.py riot_py`
Step 2: Makemessages for your locales
`./manage.py makemessages gettext_utils --locale en`
`./manage.py makemessages gettext_utils --locale my`

(Repeat for the language codes relevant to your project)

Step 3: Rosetta compile as per usual
