Examples
========
You can find the code for examples in the `examples folder <https://github.com/GIlunga/JSON-Configparser/tree/master/examples>`_.

==============
Simple Example
==============

In this example we want to read a list of words, filter them based on their size, and then translate them using a dictionary.
Below is a definition of the JSON file (args.json). The *fail* flag indicates if a ValueError should be raised on a word
fails to pass the length check.

.. code-block:: json

    {
        "words": ["hello", "world", "I", "am", "Python", "notproperlytokenizedlongword"],
        "max_size": 10,
        "fail": false,
        "translation": {
            "hello": "Ola",
            "world": "mundo",
            "I": "eu",
            "am": "sou",
            "Python": "Python",
            "notproperlytokenizedlongword": "notproperlytokenizedlongword"
        }
    }

We must now create a options.py file with the Options NamedTuple definition, the bounds, extra validations, and a function
which returns an instance of the NamedTuple, given a path to a valid JSON.

Below is the full options.py file.

.. code-block:: python

    from typing import NamedTuple, List, Dict
    import json_configparser


    class Options(NamedTuple):
        words: List[str]
        max_size: int = 2
        fail: bool = False
        translation: Dict[str, str] = {}


    bounds = [json_configparser.Bounds("max_size", lower_bound=1)]


    def extra_validations(args_dict):
        for word in args_dict["words"]:
            if word not in args_dict["translation"]:
                raise ValueError("Unknown word: {}".format(word))


    def create_options_object(path_to_json):
        args_object = json_configparser.ConfigArgs(Options, bounds, extra_validations)
        dict_args = args_object.parse_json(path_to_json)
        return Options(**dict_args)

We added some defaults and a lower bound for the max_size argument. Also, we added an extra validation which states that
all elements in the words argument should be keys of the translation argument.

Finally, we can implement the main code, which you can find below.

.. code-block:: python

    import options


    def filter_words(args: options.Options):
        filtered_words = []
        for word in args.words:
            if len(word) > args.max_size:
                if args.fail:
                    raise ValueError("{} exceeds the maximum size of {} characters".format(word, args.max_size))
                else:
                    print("Ignoring '{}', because it exceeds the maximum "
                          "size of {} characters".format(word, args.max_size))
            else:
                filtered_words.append(word)

        return filtered_words


    def main(args: options.Options):
        filtered_words = filter_words(args)
        translations = [args.translation[word] for word in filtered_words]
        print(" ".join(translations))


    if __name__ == '__main__':
        path_to_json = "args.json"
        main(options.create_options_object(path_to_json))

We first instantiate the Options class by calling the options.create_options_object function.
From this point, we are now sure that the arguments have been validated and they can no longer be changed.
The rest of the code simple uses the attributes of the NamedTuple to filter and translate the words.