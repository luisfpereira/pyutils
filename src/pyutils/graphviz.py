import os


def export_graph(filename, outputs_dir=".", program="dot", fmt="svg"):
    """
    Notes:
        New file basename will be the same as current, but with different format.
    """

    new_filename = os.path.join(outputs_dir, _get_basename(filename, fmt))
    cmd = f"{program} -T{fmt} {filename} > {new_filename}"
    os.system(cmd)

    print(f"Exported to {new_filename}")


def _get_basename(filename, fmt):
    return f"{''.join(os.path.basename(filename).split('.')[:-1])}.{fmt}"
