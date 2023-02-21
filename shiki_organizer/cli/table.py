from rich.table import Table

from shiki_organizer.cli.formatting import duration_to_str


def create_intervals_table(intervals):
    headers = []
    table = Table(title="Intervals", show_header=True, header_style="bold")
    for interval in intervals:
        for key in interval.keys():
            if key not in headers and key != "notes":
                headers.append(key)
    for header in headers:
        if header in ["id", "recurrence", "parent"]:
            justify = "right"
        else:
            justify = "left"
        table.add_column(header, header_style="bold", justify=justify)
    last_start_date = intervals[0]["start"].date()
    total_duration = 0
    for i in range(len(intervals)):
        row = []
        for header in headers:
            if header in intervals[i] and intervals[i][header]:
                if header == "duration":
                    row.append(duration_to_str(intervals[i][header]))
                else:
                    row.append(str(intervals[i][header]))
            else:
                row.append("")
        if (
            i + 1 < len(intervals)
            and intervals[i + 1]["start"].date() != intervals[i]["start"].date()
        ) or i + 1 == len(intervals):
            total_duration += intervals[i]["duration"]
            table.add_row(*row, duration_to_str(total_duration))
            table.add_section()
            total_duration = 0
        else:
            table.add_row(*row)
            total_duration += intervals[i]["duration"]
        # last_start_date = intervals[i]["start"].date()
    return table
