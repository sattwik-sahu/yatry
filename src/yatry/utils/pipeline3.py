import numpy as np
from yatry.utils.data.locations import Location
from yatry.utils.helpers.route import get_valid_shared_route
from yatry.utils.models import Passenger
from yatry.utils.models.map import Map
from yatry.utils.data.map import BHOPAL
from yatry.utils.data.io import create_random_passengers
from numpy import typing as npt
from datetime import datetime, timedelta
from yatry.utils.helpers.time import time_affinity_score
from yatry.utils.optim.clustering import affinity_propagation_ride_sharing
from yatry.utils.optim.assign import VehicleAssignmentModel
from yatry.utils.optim.time import optimize_passengers_dep_time
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.cluster import AffinityPropagation
from collections import defaultdict

# Rich library imports
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.padding import Padding
from rich.columns import Columns
from rich import box

# Initialize Rich console
console = Console()


def main():
    # Create a header panel
    console.print(
        Panel(
            "[bold blue]Ride Sharing Optimization System[/bold blue]",
            subtitle="[italic]Powered by YATRY[/italic]",
            border_style="blue",
        )
    )

    # Get the random passengers
    saving = []
    x_vals = []

    # Create a table to display the experiment setup
    setup_table = Table(title="Experiment Configuration", box=box.ROUNDED)
    setup_table.add_column("Parameter", style="cyan")
    setup_table.add_column("Value", style="green")
    setup_table.add_row("City Map", "BHOPAL")
    setup_table.add_row("Affinity Propagation Damping", "0.7")
    setup_table.add_row("Affinity Percentile", "50%")
    console.print(setup_table)

    # Set up the passenger range
    start_passengers = 500
    end_passengers = 501  # Inclusive range

    for N_PASSENGERS in range(start_passengers, end_passengers):
        x_vals.append(N_PASSENGERS)
        console.print(f"[bold cyan]Processing {N_PASSENGERS} passengers...[/bold cyan]")

        # Create a status spinner while generating passengers
        with console.status(
            f"[bold green]Generating {N_PASSENGERS} random passengers...",
            spinner="dots",
        ):
            passengers: list[Passenger] = create_random_passengers(
                n_passengers=N_PASSENGERS,
                time_range=(datetime.now(), datetime.now() + timedelta(hours=1)),
            )

        # Print passenger info summary
        passenger_summary = Table(title=f"Passenger Summary (Total: {N_PASSENGERS})")
        passenger_summary.add_column("Statistic", style="cyan")
        passenger_summary.add_column("Value", style="green")

        # Calculate some basic statistics
        avg_time_window = (
            sum(
                (p.dep_time_range[1] - p.dep_time_range[0]).total_seconds()
                for p in passengers
            )
            / N_PASSENGERS
        )

        passenger_summary.add_row("Total Passengers", str(N_PASSENGERS))
        t_min, t_max = passengers[0].dep_time_range
        passenger_summary.add_row(
            "Time Range",
            f"{t_min.strftime('%H:%M')} - {t_max.strftime('%H:%M')}",
        )
        passenger_summary.add_row(
            "Avg Time Window", f"{avg_time_window / 60:.1f} minutes"
        )
        console.print(passenger_summary)

        # Calculate affinity matrices with status indicators
        with console.status(
            "[bold yellow]Calculating time affinity matrix...", spinner="point"
        ):
            tau: npt.NDArray[np.float64] = np.zeros(shape=(N_PASSENGERS, N_PASSENGERS))
            for i, p_i in enumerate(passengers):
                for j, p_j in enumerate(passengers):
                    t1_min, t1_max = p_i.get_dep_time_range_num()
                    t2_min, t2_max = p_j.get_dep_time_range_num()
                    tau[i, j] = time_affinity_score(
                        t1_min=t1_min, t1_max=t1_max, t2_min=t2_min, t2_max=t2_max
                    )

        with console.status(
            "[bold yellow]Calculating route affinity matrix...", spinner="dots"
        ):
            rho: npt.NDArray[np.float64] = BHOPAL.get_passenger_route_affinity_matrix(
                passengers=passengers
            )

        console.print(
            "[bold green]✓[/bold green] Affinity matrices calculated successfully"
        )

        # Create the affinity matrix
        affinity_matrix: npt.NDArray[np.float64] = rho * tau

        # Visualize affinity matrix
        with console.status(
            "[bold magenta]Generating affinity matrix visualization...",
            spinner="earth",
        ):
            plt.figure(figsize=(10, 8))
            sns.heatmap(affinity_matrix, cbar_kws={"label": "Affinity Score"})
            plt.title("Combined Route-Time Affinity Matrix")
            plt.xlabel("Passenger Index")
            plt.ylabel("Passenger Index")
            plt.tight_layout()
            plt.savefig("fig.pdf")
            plt.close()
            console.print("[bold green]✓[/bold green] Heatmap saved to fig.pdf")

        # Run clustering algorithm with progress indication
        with console.status(
            "[bold cyan]Running clustering algorithm...", spinner="monkey"
        ):
            preference_val = np.percentile(affinity_matrix, 50)
            ap = AffinityPropagation(
                affinity="precomputed",
                damping=0.7,
                max_iter=500,
                preference=preference_val,
            )
            min_val = np.min(affinity_matrix)
            max_val = np.max(affinity_matrix)
            scaled_affinity = (affinity_matrix - min_val) / (max_val - min_val + 1e-10)
            cluster_passenger_inxs: np.ndarray = ap.fit_predict(X=scaled_affinity)

        grouped_indices = defaultdict(list)
        for idx, val in enumerate(cluster_passenger_inxs):
            grouped_indices[val].append(idx)

        # Filter only those values that have more than one index (i.e., grouped)
        groups = {val: idxs for val, idxs in grouped_indices.items() if len(idxs) > 0}

        # Display clustering results
        cluster_table = Table(title="Clustering Results")
        cluster_table.add_column("Metric", style="cyan")
        cluster_table.add_column("Value", style="green")
        cluster_table.add_row("Total Groups", str(len(groups)))
        cluster_table.add_row(
            "Average Group Size",
            f"{sum(len(ids) for ids in groups.values()) / len(groups):.2f}",
        )
        cluster_table.add_row(
            "Min Group Size", str(min(len(ids) for ids in groups.values()))
        )
        cluster_table.add_row(
            "Max Group Size", str(max(len(ids) for ids in groups.values()))
        )
        console.print(cluster_table)

        # Process each group with detailed stats
        total_total_saving = 0

        with console.status(
            "[bold green]Processing auto groups...", spinner="arrow"
        ) as status:
            for auto_number, (val, idxs) in enumerate(sorted(groups.items()), start=1):
                status.update(
                    f"[bold green]Processing Auto #{auto_number}/{len(groups)}..."
                )

                group = [passengers[idx] for idx in idxs]
                total_fare = 0
                sum_fare = 0
                total_saving = 0

                # Calculate original fares
                for passenger_ in group:
                    original_fare = BHOPAL.get_fare_on_route(
                        BHOPAL._find_route(passenger_.source, passenger_.destination)
                    )
                    if original_fare > total_fare:
                        total_fare = original_fare
                    sum_fare += original_fare

                # Optimize departure time
                try:
                    status.update(
                        f"[bold yellow]Optimizing departure time for Auto #{auto_number}/{len(groups)}..."
                    )
                    dep_time: float = optimize_passengers_dep_time(passengers=group)
                except Exception as e:
                    console.print(
                        f"[bold red]Warning: Optimization failed for group #{auto_number}: {e}[/bold red]"
                    )
                    # Fallback: Use average of min departure times
                    dep_time = float(
                        np.mean([p.get_dep_time_range_num()[0] for p in group])
                    )

                # Create a table for the auto details
                auto_table = Table(box=box.SIMPLE)
                auto_table.add_column("Detail", style="cyan")
                auto_table.add_column("Value", style="yellow")
                auto_table.add_row(
                    "Optimized Departure Time",
                    f"[bold green]{datetime.fromtimestamp(dep_time).strftime('%H:%M %d %b %Y')}[/bold green]",
                )
                auto_table.add_row("Total Passengers", str(len(group)))
                auto_table.add_row("Total Fare", f"₹{total_fare:.2f}")

                # Create a passenger table for this auto
                passenger_table = Table(box=box.SIMPLE)
                passenger_table.add_column("Passenger", style="blue")
                passenger_table.add_column("Route", style="cyan")
                passenger_table.add_column("Original Fare", style="yellow")
                passenger_table.add_column("New Fare", style="green")
                passenger_table.add_column("Savings", style="dim magenta")
                passenger_table.add_column("Savings (%)", style="magenta")

                # Calculate new fare for each passenger
                for passenger_ in group:
                    original_fare = BHOPAL.get_fare_on_route(
                        route=BHOPAL._find_route(
                            passenger_.source, passenger_.destination
                        )
                    )

                    new_fare = original_fare * total_fare / sum_fare
                    saving_amount = original_fare - new_fare
                    total_saving += saving_amount

                    passenger_table.add_row(
                        passenger_.name,
                        f"{passenger_.source.value} → {passenger_.destination.value}",
                        f"₹{original_fare:.2f}",
                        f"₹{new_fare:.2f}",
                        f"[bold]₹{saving_amount:.2f}[/bold]",
                        f"[bold]{100 * saving_amount / original_fare:.2f}[/bold]",
                    )

                auto_table.add_row(
                    "Total Savings",
                    f"[bold magenta]₹{total_saving:.2f}[/bold magenta]",
                )

                # Create a layout for this auto details
                auto_layout = Layout()
                auto_layout.split(
                    Layout(auto_table, name="details"),
                    Layout(passenger_table, name="passengers"),
                )

                status.stop()
                console.print(
                    Panel(
                        auto_layout,
                        title=f"[bold blue]Auto #{auto_number}[/bold blue]",
                        border_style="blue",
                        subtitle=f"[italic]Group ID: {val}[/italic]",
                    )
                )
                status.start()

                total_total_saving += total_saving

        # Summary statistics
        summary_panel = Panel(
            Padding(
                Text.from_markup(
                    f"""
[bold cyan]Summary Statistics:[/bold cyan]
Number of Passengers: [yellow]{N_PASSENGERS}[/yellow]
Number of Auto Groups: [yellow]{len(groups)}[/yellow]
Total Savings: [bold green]₹{total_total_saving:.2f}[/bold green]
Average Saving per Passenger: [bold green]₹{total_total_saving / N_PASSENGERS:.2f}[/bold green]
                """,
                    justify="center",
                ),
                (2, 4),
            ),
            title="[bold green]Optimization Results[/bold green]",
            border_style="green",
        )
        console.print(summary_panel)

        saving_pp = total_total_saving / N_PASSENGERS
        saving.append(saving_pp)

    # Plot the savings per passenger
    with console.status(
        "[bold cyan]Generating savings visualization...", spinner="bouncingBar"
    ):
        plt.figure(figsize=(10, 6))
        plt.plot(
            x_vals,
            saving,
            marker="o",
            linestyle="-",
            color="green",
            linewidth=2,
            markersize=8,
        )
        plt.xlabel("Number of Passengers")
        plt.ylabel("Average Saving per passenger (₹)")
        plt.title("Average Saving per Passenger vs Number of Passengers")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.xticks(x_vals)
        plt.tight_layout()
        plt.savefig("savings_vs_passengers.png")

    console.print(
        "[bold green]✓[/bold green] Savings visualization saved to savings_vs_passengers.png"
    )

    # Final message
    console.print(
        Panel(
            "[bold blue]Ride Sharing Optimization Complete![/bold blue]",
            subtitle="[italic]Thank you for using YATRY[/italic]",
            border_style="blue",
        )
    )


if __name__ == "__main__":
    main()
