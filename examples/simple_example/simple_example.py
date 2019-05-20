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
