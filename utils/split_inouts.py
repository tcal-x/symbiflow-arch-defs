#!/usr/bin/env python3
"""
This script provides a temporary solution for the problem of inout top level
port representation of the BLIF format.

The script loads the design from a JSON file generated by Yosys. Then it splits
all inout ports along with their nets and connections to cell ports into two.
Suffixes are automatically added to distinguish between the input and the
output part.

For example in the given design (in verilog):

 module top(
  input  A,
  output B,
  inout  C
 );

  IOBUF iobuf (
   .I(A),
   .O(B),
   .IO(C)
  );

 endmodule

the resulting design would be:

 module top(
  input  A,
  output B,
  input  C_$inp,
  output C_$out
 );

  IOBUF iobuf (
   .I(A),
   .O(B),
   .IO_$inp(C_$inp),
   .IO_$out(C_$out)
  );

 endmodule

"""
import argparse
import os
import simplejson as json

# =============================================================================


def find_top_module(design):
    """
    Looks for the top-level module in the design. Returns its name.
    """

    for name, module in design["modules"].items():
        attrs = module["attributes"]
        if "top" in attrs and attrs["top"] == 1:
            return name

    return None


def get_port_nets(port):
    """
    Returns a set of numbers corresponding to net indices used by the given
    port.
    """
    return set([n for n in port["bits"] if isinstance(n, int)])


def get_free_net(nets):
    """
    Given a set of used net indices, returns a new, free index.
    """
    sorted_nets = sorted(list(nets))

    # Find a gap in sequence
    for i in range(len(nets) - 1):
        n0 = sorted_nets[i]
        n1 = sorted_nets[i + 1]
        if n1 != (n0 + 1):
            return n0 + 1

    # No gap was found, return max + 1.
    return sorted_nets[-1] + 1


# =============================================================================


def find_and_split_inout_ports(design, module_name):

    # Get the module
    module = design["modules"][module_name]

    # Find all used net indices
    nets = set()
    for port in module["ports"].values():
        nets |= get_port_nets(port)

    # Get all inout ports
    inouts = {
        k: v
        for k, v in module["ports"].items()
        if v["direction"] == "inout"
    }

    # Split ports
    new_ports = {}
    net_map = {}
    port_map = []
    for name, port in inouts.items():

        # Remove the inout port from the module
        del module["ports"][name]
        nets -= get_port_nets(port)

        # Make an input and output port
        for dir in ["input", "output"]:
            new_name = name + "_$" + dir[:3]
            new_port = {"direction": dir, "bits": []}

            print("Mapping port '{}' to '{}'".format(name, new_name))

            for n in port["bits"]:
                if isinstance(n, int):
                    mapped_n = get_free_net(nets)
                    print("Mapping net {} to {} ({})".format(n, mapped_n, dir))

                    if n not in net_map:
                        net_map[n] = {}
                    net_map[n][dir[0]] = mapped_n
                    nets.add(mapped_n)

                    new_port["bits"].append(mapped_n)
                else:
                    new_port["bits"].append(n)

            port_map.append((
                name,
                new_name,
            ))
            new_ports[new_name] = new_port

    # Add inputs and outputs
    module["ports"].update(new_ports)

    # .....................................................
    netnames = module["netnames"]

    # Remove netnames related to inout ports
    for name, net in list(module["netnames"].items()):
        if name in inouts:
            print("Removing netname '{}'".format(name))
            del netnames[name]

    # Remove remapped nets
    for name, net in list(netnames.items()):

        # Remove "bits" used by the net that were re-mapped.
        net["bits"] = ["\"x\"" if b in net_map else b for b in net["bits"]]

        # If there is nothing left, remove the whole net.
        if all([not isinstance(b, int) for b in net["bits"]]):
            print("Removing netname '{}'".format(name))
            del netnames[name]

    # Add netnames related to new input and output ports
    for name, port in new_ports.items():
        netnames[name] = {
            "hide_name": 0,
            "bits": port["bits"],
            "attributes": {}
        }

    return port_map, net_map


def remap_connections(design, module_name, net_map):

    module = design["modules"][module_name]
    cells = module["cells"]

    # Process cells
    for name, cell in cells.items():
        port_directions = cell["port_directions"]
        connections = cell["connections"]

        # Process cell connections
        for port_name, port_nets in list(connections.items()):

            # Skip if no net of this connection were remapped
            if len(set(net_map.keys()) & set(port_nets)) == 0:
                continue

            print(
                "Processing cell '{}' of type '{}'".format(name, cell["type"])
            )

            # Split the port into two
            for dir in ["input", "output"]:
                new_port_name = port_name + "_$" + dir[:3]
                new_port_nets = []

                print(
                    "Mapping port '{}' to '{}'".format(
                        port_name, new_port_name
                    )
                )

                for n in port_nets:
                    if n in net_map:
                        mapped_n = net_map[n][dir[0]]
                    else:
                        mapped_n = "\"x\""

                    print(" Mapping connection {} to {}".format(n, mapped_n))
                    new_port_nets.append(mapped_n)

                connections[new_port_name] = new_port_nets
                port_directions[new_port_name] = dir

            # Remove old ones
            del connections[port_name]
            del port_directions[port_name]


# =============================================================================


def main():

    # Parse args
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-i", required=True, type=str, help="Input JSON")
    parser.add_argument("-o", default=None, type=str, help="Output JSON")

    args = parser.parse_args()

    # Output name
    if args.o is None:
        args.o = os.path.splitext(args.i)[0] + "_out.json"

    # Read the design
    with open(args.i, "r") as fp:
        design = json.load(fp)

    # Find the top module
    top_name = find_top_module(design)

    # Find and split inouot ports
    port_map, net_map = find_and_split_inout_ports(design, top_name)
    # Remap cell connections
    remap_connections(design, top_name, net_map)

    # Write the design
    with open(args.o, "w") as fp:
        json.dump(design, fp, sort_keys=True, indent=2)


if __name__ == "__main__":
    main()
