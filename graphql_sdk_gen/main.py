import click


@click.command()
@click.version_option()
def main():
    print("hello world!")
