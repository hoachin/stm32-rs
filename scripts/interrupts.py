import os
import argparse
import xml.etree.ElementTree as ET


def parse_device(svdfile):
    interrupts = {}
    tree = ET.parse(svdfile)
    dname = tree.find("name").text
    for ptag in tree.iter('peripheral'):
        pname = ptag.find('name').text
        for itag in ptag.iter('interrupt'):
            name = itag.find('name').text
            value = itag.find('value').text
            interrupts[int(value)] = {"name": name, "pname": pname}
    return dname, interrupts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outdir", help="directory to write files to")
    parser.add_argument("svdfiles", nargs="*", help="List of SVD files")
    args = parser.parse_args()
    devices = {}
    for f in args.svdfiles:
        name, interrupts = parse_device(f)
        devices[name] = interrupts
        with open(os.path.join(args.outdir, name), "w") as f:
            for val in sorted(interrupts.keys()):
                f.write("{} {} (in {})\n".format(
                    val, interrupts[val]["name"], interrupts[val]["pname"]))


if __name__ == "__main__":
    main()
