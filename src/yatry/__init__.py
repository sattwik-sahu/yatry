import typer
from typing_extensions import Annotated

app = typer.Typer(name="yatry", help="Optimizing ride sharing for campus commuters")


@app.command(name="random")
def random(
    n_passengers: Annotated[
        int, typer.Argument(default=10, help="Number of passengers to simulate")
    ],
) -> None:
    print("Hello from yatry!")
