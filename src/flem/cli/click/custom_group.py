import click


class CustomGroup(click.Group):
    def parse_args(self, ctx, args):
        if len(args) and args[0] in self.commands:
            if len(args) == 1 or args[1] not in self.commands:
                args.insert(0, "")
        super(CustomGroup, self).parse_args(ctx, args)
