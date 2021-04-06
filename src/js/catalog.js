const csep = '\x04'; // The separator between "context" marker and "text" value, as per Django
const contextualize = (context, text) => `${context}${csep}${text}` //Return a 'contextualized' string, appending context and marker to key
/*
Type checking helps to determine whether we found a value
in the dictionary and whether there are plural forms of this string
*/
const is_undef = (value) => typeof(value) == 'undefined';
const is_str = (value) => typeof(value) == 'string';
const is_arr = (value) => Array.isArray(value)

/*
Determining if a given count should use a plural form of a word or not
Plural / Singular forms are passed as an array
*/
const pluralidx = (count) => count == 1 ? 0 : 1

const gettext = (catalog, msgid) => {
    /*
    For the simplest case of a single word or phrase translation
    this looks up the w/p from the catalog
    */
    let value = catalog[msgid];
    if (is_undef(value)){
        return gettext_noop(msgid);
    } else if (is_str(value)){
        return value;
    } else if (is_arr(value)){
        return value[0]
    }
};

const ngettext = (catalog, msgid, plural, count) => {
    /*
    plural is a fallback value if not found in the dictionary
    */
    let value = catalog[msgid];
    if (is_undef(value)){
        return (count == 1 || !plural) ? gettext_noop(msgid) : plural;
    } else if (is_str(value)){
        return value;
    } else if (is_arr(value)){
        return value[pluralidx(count)];
    }
};

const gettext_noop = (msgid) => msgid;

const pgettext = (catalog, context, msgid) => {
    let value = gettext(catalog, contextualize(context, msgid));

    if (value.indexOf(csep) != -1) {
        value = msgid;
    }
    return value;
};

const npgettext = (catalog, context, msgid, plural, count) => {
    let value = ngettext(
        catalog,
        contextualize(context, msgid),
        contextualize(context, plural),
        count
    );
    if (value.indexOf(csep) != -1) {
        value = ngettext(catalog, msgid, plural, count);
    }
    return value;
};

const do_named_interpolate = (fmt, obj) => fmt.replace(/%\(\w+\)s/g, function(match) {return String(obj[match.slice(2,-2)])});
const do_interpolate = (fmt, obj) => fmt.replace(/%s/g, function(match){return String(obj.shift())});

export default class Catalog {
    constructor(content, translate_url) {
        this.content = content;
        this.translate_url = translate_url;
        this.waitingTranslations = [];
        this.timer = undefined;
        this.timeout = 300;
    };

    fetchTranslations() {
        const response = fetch(this.translate_url, {
            method: "POST",
            body: JSON.stringify(this.waitingTranslations),
            headers: {
                "Content-Type": "application/json",
            }
        });
        this.waitingTranslations = [];
        return response;
    }

    collect(context, msgid, plural) {
        clearTimeout(this.timer);
        this.waitingTranslations.push([context, msgid, plural]);
        this.timer = setTimeout(this.fetchTranslations, this.timeout);
    }

    translate (context, msgid, plural, count, interpolate, interpolate_named) {
        /*
        Return the output of an appropriately chosen translation function.
        Depending on the parameters passed this will range from a simple lookup
        to something which outputs a plural string from a contextual dictionary
        */
        const catalog = this.content || {};
        let message;

        /* Broadly speaking, go from 'most complex' to 'least complex' case */
        if (context && msgid && plural && count) { message = npgettext(catalog, context, msgid, plural, parseInt(count)) }
        else if (msgid && plural && count) { message = ngettext(catalog, msgid, plural, parseInt(count)) }
        else if (msgid && context) { message = pgettext(catalog, context, msgid) }
        else if (msgid) { message = gettext(catalog, msgid) }

        /* Further processing by string interpolation */
        if (interpolate_named) { message = do_named_interpolate(message, interpolate_named) }
        else if (interpolate) { message = do_interpolate(message, interpolate) }
        return message;
    };
    has(context, msgid) {
        return !is_undef(this.content[context ? contextualize(context, msgid) : msgid]);
    }
};
