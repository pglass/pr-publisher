"""An example of a customer publisher

1. Subclass BasePublisher
2. Add optional CLI arguments for your publisher in `add_cli_arguments`
3. Implement the `publish` method
4. Register your publisher with `Main.register_publisher`
5. Call `Main().run()`

For now, this essentially creates your own custom CLI as well. So rather than
using the upstream `pr-publisher` command, you would use
`python custom_publisher.py` instead. See the `main` function at the end.

To run this,

    $ python custom_publisher.py -h

    $ python custom_publisher.py \
        --github-token <token> \
        --some-chat-url 'http://chat.example.com' \
        some-chat
"""
from pr_publisher.publishers.base import BasePublisher
from pr_publisher.main import Main


class CustomPublisher(BasePublisher):

    @classmethod
    def add_cli_arguments(cls, parser):
        # All publisher cli args should be optional. (A user may only care to
        # run a single publisher, and doesn't want to supply values for the
        # rest of the publishers)
        parser.add_argument("--some-chat-url", default=None)

    def __init__(self, args):
        super(CustomPublisher, self).__init__(args)

        if not args.some_chat_url:
            raise Exception("--some-chat-url is required")

    def publish(self, publish_entries):
        for entry in publish_entries:
            # Just printing, for the sake of this example.
            # see pr_publisher.entry.PublishEntry for all available fields.
            print("{}\n  {}".format(entry.pr.title, entry.pr.html_url))


def main():
    # Register the publisher before we run the program
    Main.register_publisher("some-chat", CustomPublisher)

    # Run the program
    Main().run()


if __name__ == "__main__":
    main()
