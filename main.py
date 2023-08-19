from rich.console import Console
from rich import print
from pynput import keyboard
from decimal import *

input = Console().input
clear = Console().clear


def header() -> None:
    clear()
    print("""
    [bold red]McCalc[/bold red]: Minecraft ore sustainability calculator
    [dim bold cyan]-----------------------------------------------[/]""")


def _wait_on_press(key):
    return False


def wait() -> None:
    with keyboard.Listener(on_press=_wait_on_press) as listener:
        listener.join()


def nice_input_from_set(question: str, options: set[str]) -> str:
    correct = False
    if question.endswith("\n"):
        question = question[:-1]
    while not correct:
        header()
        data = input(question)
        if data in options:
            return data
        print("Invalid input, please try again.")


def nice_input_int(question: str, imin: int | None = None, imax: int | None = None):
    correct = False
    if question.endswith("\n"):
        question = question[:-1]
    while not correct:
        header()
        data = input(question)
        try:
            data = int(data)
        except ValueError:
            print("1 Invalid input, please try again.")
            continue
        if imax is not None and data > imax:
            print("2 Invalid input, please try again.")
            continue
        if imin is not None and data < imin:
            print("3 Invalid input, please try again.")
            continue
        return data


def nice_input_decimal(question: str, imin: Decimal | None = None, imax: Decimal | None = None):
    correct = False
    if question.endswith("\n"):
        question = question[:-1]
    while not correct:
        header()
        data = input(question)
        try:
            data = Decimal(data)
        except InvalidOperation:
            print("1 Invalid input, please try again.")
            continue
        if imax is not None and data > imax:
            print("2 Invalid input, please try again.")
            continue
        if imin is not None and data < imin:
            print("3 Invalid input, please try again.")
            continue
        return data


header()
at_y_main = nice_input_int(
    "At what [italic yellow]y[/italic yellow] level does minecraft" +
    " report you're standing? [dim italic](between [blue]-64[/blue] and [blue]320[/blue])[/dim italic] ",
    -63,
    318
)
header()
y_values_to_be_thought_about: set[int] = {at_y_main, at_y_main - 1, at_y_main + 1, at_y_main + 2}
header()
print(f"""This means that we will make a strip mine, at y level [blue]{at_y_main}[/blue],
and this means that every step through the tunnel, makes the player will see blocks in this shape:
  [ [ [dim grey]_[/dim grey] [green bold]▒[/green bold] [dim grey]_[/dim grey] ]      [dim grey]y=[/][blue]{at_y_main + 2}[/]
    [ [green bold]▒[/green bold] [green bold]▒[/green bold] [green bold]▒[/green bold] ]      [dim grey]y=[/][blue]{at_y_main + 1}[/]
    [ [green bold]▒[/green bold] [green bold]▒[/green bold] [green bold]▒[/green bold] ]      [dim grey]y=[/][blue]{at_y_main}[/]
    [ [dim grey]_[/dim grey] [green bold]▒[/green bold] [dim grey]_[/dim grey] ] ]    [dim grey]y=[/][blue]{at_y_main - 1}[/]

[bold red]PRESS ANY KEY TO CONTINUE[/bold red]""")
wait()
y_rarities = {x: 0 for x in y_values_to_be_thought_about}
for y in y_values_to_be_thought_about:
    y_rarities[y] = nice_input_decimal(f"Please enter the rarity [dim grey](as a percentage, excluding the % sign)[/] "
                                       f"of your ore at y [blue bold]{y}[/]? ", Decimal(0), Decimal(100)) / Decimal(100)

blocks_per_thousand_blocks_long_mined = (y_rarities[at_y_main] * Decimal(3000) + y_rarities[at_y_main + 1]
                                         * Decimal(3000) + y_rarities[at_y_main + 2] * Decimal(1000) + y_rarities[
                                             at_y_main - 1] * Decimal(1000))
header()
blocks_per_thousand_blocks_long_mined_str = str(blocks_per_thousand_blocks_long_mined.quantize(Decimal("0.1")))
length_of_string_used_for_dashes_in_output = len(blocks_per_thousand_blocks_long_mined_str) if \
    len(blocks_per_thousand_blocks_long_mined_str) > 4 else 4
print(f"""[bold red]Calculated the amount of ore found in a 1000 block long strip mine:[/bold red]
        {blocks_per_thousand_blocks_long_mined_str}
        {"-" * length_of_string_used_for_dashes_in_output}
        1000 blocks over [dim blue]x[/] or [dim blue]z[/]
[bold red]OR[/]""")
blocks_per_block_in_tunnel = blocks_per_thousand_blocks_long_mined / Decimal(1000)
blocks_per_block_in_tunnel_str = str(blocks_per_block_in_tunnel.quantize(Decimal("0.0000001")))
length_of_string_used_for_dashes_in_output = len(blocks_per_block_in_tunnel_str) if \
    len(blocks_per_block_in_tunnel_str) > 1 else 1
print(f"""        {blocks_per_block_in_tunnel_str}
        {"-" * length_of_string_used_for_dashes_in_output}
        1 block over [dim blue]x[/] or [dim blue]z[/]""")
print("[bold red]PRESS ANY KEY TO CONTINUE[/bold red]")
wait()
pickaxe_durability = nice_input_int("How much durability does your pickaxe have? ", 1)
tunnel_length_per_pickaxe = pickaxe_durability / Decimal(2)
ore_per_pickaxe = blocks_per_block_in_tunnel * tunnel_length_per_pickaxe
length_of_string_used_for_dashes_in_output = len(str(ore_per_pickaxe.quantize(Decimal("0.0000001")))) if \
    len(str(ore_per_pickaxe.quantize(Decimal("0.0000001")))) > 8 else 8
header()
print(f"""[bold red]Calculated the amount of ore found per pickaxe:[/bold red]:
        {ore_per_pickaxe.quantize(Decimal("0.0000001"))}
        {"-" * length_of_string_used_for_dashes_in_output}
        1 pickaxe""")
print("[bold red]PRESS ANY KEY TO CONTINUE[/bold red]")
wait()
is_this_pickaxe_made_of_the_same_material = nice_input_from_set(
    "Is this pickaxe made of the same material as the ore? [dim](y/n)[/] ", {"y", "n"})
header()
if is_this_pickaxe_made_of_the_same_material:
    if ore_per_pickaxe < Decimal(3):
        print(f"""Your ore is [bold red blink]UNSUSTAINABLE[/bold red blink]!
You will run out of ore before you can make a new pickaxe!
[cyan][bold]{ore_per_pickaxe.quantize(Decimal("0.0000001"))}[/bold] ore per pickaxe is smaller than """
              f"""the [bold]3[/bold] ore required to make a new pickaxe.[/cyan] 
[bold red]PRESS ANY KEY TO CONTINUE[/bold red]""")
        wait()
    else:
        print(f"""Your ore is [bold green]SUSTAINABLE[/bold green]!
You will be able to make a new pickaxe before you run out of ore!
[cyan][bold]{ore_per_pickaxe.quantize(Decimal("0.0000001"))}[/bold] ore per pickaxe is greater than """
                f"""the [bold]3[/bold] ore required to make a new pickaxe.[/cyan] 
[bold red]PRESS ANY KEY TO CONTINUE[/bold red]""")
        wait()

