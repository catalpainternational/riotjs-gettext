const csep = "\x04"; // The separator between "context" marker and "text" value, as per Django
const contextualize = (context, text) => `${context}${csep}${text}`; //Return a 'contextualized' string, appending context and marker to key
/*
Type checking helps to determine whether we found a value
in the dictionary and whether there are plural forms of this string
*/
const is_undef = (value) => typeof value == "undefined";
const is_str = (value) => typeof value == "string";
const is_arr = (value) => Array.isArray(value);

/*
Determining if a given count should use a plural form of a word or not
Plural / Singular forms are passed as an array
*/
const pluralidx = (count) => (count == 1 ? 0 : 1);

const _gettext = (catalog, msgid) => {
  /*
    For the simplest case of a single word or phrase translation
    this looks up the w/p from the catalog
    */
  let value = catalog[msgid];
  if (is_undef(value)) {
    return _gettext_noop(msgid);
  } else if (is_str(value)) {
    return value;
  } else if (is_arr(value)) {
    return value[0];
  }
};

const _ngettext = (catalog, singular, plural, count) => {
  /*
    plural is a fallback value if not found in the dictionary
    */
  let value = catalog[singular];
  if (is_undef(value)) {
    return count == 1 || !plural ? _gettext_noop(singular) : plural;
  } else if (is_str(value)) {
    return value;
  } else if (is_arr(value)) {
    return value[pluralidx(count)];
  }
};

const _gettext_noop = (msgid) => msgid;

const _pgettext = (catalog, context, msgid) => {
  let value = _gettext(catalog, contextualize(context, msgid));

  if (value.indexOf(csep) != -1) {
    value = msgid;
  }
  return value;
};

const _npgettext = (catalog, context, singular, plural, count) => {
  let value = _ngettext(
    catalog,
    contextualize(context, singular),
    contextualize(context, plural),
    count
  );
  if (value.indexOf(csep) != -1) {
    value = _ngettext(catalog, singular, plural, count);
  }
  return value;
};

const do_named_interpolate = (fmt, obj) =>
  fmt.replace(/%\(\w+\)s/g, function (match) {
    return String(obj[match.slice(2, -2)]);
  });
const do_interpolate = (fmt, obj) =>
  fmt.replace(/%s/g, function (match) {
    return String(obj.shift());
  });

export default class Catalog {
  constructor(content, translate_url) {
    this.content = content;
    this.translate_url = translate_url;
    this.waitingTranslations = [];
    this.timer = undefined;
    this.timeout = 300;
  }

  fetchTranslations() {
    const response = fetch(this.translate_url, {
      method: "POST",
      body: JSON.stringify(this.waitingTranslations),
      headers: {
        "Content-Type": "application/json",
      },
    });
    this.waitingTranslations = [];
    return response;
  }

  collect(context, msgid, plural) {
    clearTimeout(this.timer);
    this.waitingTranslations.push([context, msgid, plural]);
    this.timer = setTimeout(this.fetchTranslations, this.timeout);
  }

  translate(context, msgid, plural, count, interpolate, interpolate_named) {
    /*
        Return the output of an appropriately chosen translation function.
        Depending on the parameters passed this will range from a simple lookup
        to something which outputs a plural string from a contextual dictionary
        */
    const catalog = this.content || {};
    let message;

    /* Broadly speaking, go from 'most complex' to 'least complex' case */
    if (context && msgid && !is_undef(plural) && count) {
      message = this.npgettext(context, msgid, plural, parseInt(count));
    } else if (msgid && !is_undef(plural) && count) {
      message = this.ngettext(msgid, plural, parseInt(count));
    } else if (msgid && context) {
      message = this.pgettext(context, msgid);
    } else if (msgid) {
      message = this.gettext(msgid);
    }

    /* Further processing by string interpolation */
    if (interpolate_named) {
      message = do_named_interpolate(message, interpolate_named);
    } else if (interpolate) {
      message = do_interpolate(message, interpolate);
    }
    return message;
  }

  /* These have the same function signature as Django's js translation functions */
  gettext(msgid) {
    return _gettext(this.content, msgid);
  }
  ngettext(singular, plural, count) {
    return _ngettext(this.content, singular, plural, count);
  }
  pgettext(context, msgid) {
    return _pgettext(this.content, context, msgid);
  }
  npgettext(context, singular, plural, count) {
    return _npgettext(this.content, context, singular, plural, count);
  }

  interpolate(fmt, obj, named) {
    return named ? do_named_interpolate(fmt, obj) : do_interpolate(fmt, obj);
  }
}
