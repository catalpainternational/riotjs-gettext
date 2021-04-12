const csep = "\x04"; // The separator between "context" marker and "text" value, as per Django
const contextualize = (context, text) =>
  context ? `${context}${csep}${text}` : text; //Return a 'contextualized' string, appending context and marker to key
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
This may be different for different languages
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

/**
 * Call a catalog's URL for untranslated strings
 * Return the result to the catalog for updates
 * @param {*} catalog
 */
const fetchTranslations = (catalog) => {
  /* Clone waiting messages */
  const send = catalog.waitingTranslations.map((s) => s);
  const body = JSON.stringify({
    language: catalog.language,
    translations: send,
  });

  /* Remove the translations from the catalog, so we don't fetch unnecessarily */
  catalog.dropWaitingTranslations(send);
  const response = fetch(catalog.translate_url, {
    method: "POST",
    body: body,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": catalog.csrf_token,
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (json) {
      /* Register of missing translations */
      const receivedTranslations = Object.keys(json["catalog"]);
      const sentWithCt = send.map((s) =>
        s.context
          ? contextualize(s.context, s.message || s.singular)
          : s.message || s.singular
      );
      const missingTranslations = sentWithCt.filter(
        (t) => receivedTranslations.indexOf(t) === -1
      );
      catalog.update(json["catalog"], missingTranslations);
    });
};

/**
 * Represents a dictionary catalog.
 * @class
 * @param {object} content - initial translations to load
 * @param {translate_url} translate_url - url to call for additional translations
 * @param {object} opts - additional options for the catalog
 */
export default class Catalog {
  constructor(content, translate_url, opts) {
    const opts_ = opts || {};
    this.content = content;
    this.translate_url = translate_url;
    this.waitingTranslations = [];
    this.missingTranslations = [];
    this.timer = undefined;
    this.timeout = 200; /* ms to wait for a "cool-down" after receiving translations to fire a request for translations */
    this.language = opts_.language;
    /* csrf token required for Django */
    this.csrf_token = opts_.csrf_token;
    /* registers callbacks for a received translation string */
    /* this is a hash of type { str: List[function] } */
    this.handlers = {};
    this.contextualize = contextualize;
  }

  dropWaitingTranslations(sentItems) {
    this.waitingTranslations = this.waitingTranslations.filter(
      (s) => sentItems.indexOf(s) !== -1
    );
  }

  subscribe(fn, msgid, context) {
    const key = context ? contextualize(context, msgid) : msgid;
    this.handlers[key] = this.handlers[key] || [];
    this.handlers[key].push(fn);
  }

  unsubscribe(fn, msgid, context) {
    const key = context ? contextualize(context, msgid) : msgid;
    this.handlers[key] = this.handlers[key].filter(function (item) {
      if (item !== fn) {
        return item;
      }
    });
  }
  /** Add a message to the array of requests to make against the translation URL */
  collect(context, msgid, plural) {
    const catalog = this;
    if (this.messageState(context, msgid) != "collect") {
      return this.timer;
    }

    clearTimeout(this.timer);
    var message = {};
    if (!this.translate_url) {
      return;
    }
    if (context) {
      message.context = context;
    }
    if (plural) {
      message.plural = plural;
      message.singular = msgid;
    } else {
      message.message = msgid;
    }
    /* Avoid pushing onto the stack if the response has already been received or is waiting */
    this.waitingTranslations.push(message);
    this.timer = setTimeout(fetchTranslations, this.timeout, catalog);

    return this.timer;
  }
  /** Returns a string indicating whether the message is "translated", "waitingResponse" or "untranslated" or "collect" */
  messageState(context, message) {
    const msgWithCtx = contextualize(context, message);
    if (Object.keys(this.content).indexOf(msgWithCtx) !== -1) {
      return "translated";
    }
    if (this.language == "en") {
      return "translated";
    }
    if (this.missingTranslations.indexOf(msgWithCtx) !== -1) {
      return "untranslated";
    }
    for (const waitingMsg of this.waitingTranslations) {
      if (waitingMsg.context === context && waitingMsg.singular == message) {
        return "waitingResponse";
      }
      if (
        ((waitingMsg.context === context && waitingMsg.message == message) ||
          (!waitingMsg.context && !context)) &&
        (waitingMsg.message == message || waitingMsg.singular == message)
      ) {
        return "waitingResponse";
      }
    }
    return "collect";
  }

  /**
   * Updates this catalog with additional data, ie from the translation URL
   * @param {object} translations - an array in Django's JS format
   * @param {array} missingTranslations - a list of translations which were not returned from the server
   */
  update(translations, missingTranslations) {
    this.missingTranslations = missingTranslations;
    for (let message in translations) {
      /* Values here are in Django's JS format */
      /* The key is a string of a singular format message, optionally prefixed by context and marker */
      /* The value is a string or an array of strings for plural translations */
      this.content[message] = translations[message];
      /* Callback handlers notified that there is a changed / new translation */
      if (this.handlers[message]) {
        this.handlers[message].forEach((item) => {
          item();
        });
      }
    }
    /* Callback handlers notified that there was no translation */
    for (let message of missingTranslations) {
      if (this.handlers[message]) {
        this.handlers[message].forEach((item) => {
          item();
        });
      }
    }
  }

  /**
   * Return the output of an appropriately chosen translation function.
   * Depending on the parameters passed this will range from a simple lookup
   * to something which outputs a plural string from a contextual dictionary
   * @param {string} context
   * @param {string} msgid
   * @param {string} plural
   * @param {number} count
   * @param {array} interpolate
   * @param {object} interpolate_named
   */
  translate(context, msgid, plural, count, interpolate, interpolate_named) {
    let message;
    if (!this.has(context, msgid)) {
      this.collect(context, msgid);
    }
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

  has(context, msgid) {
    return !is_undef(
      this.content[context ? contextualize(context, msgid) : msgid]
    );
  }
}
