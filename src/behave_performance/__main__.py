import sys
from runtime import BehavePerformance
from arguments import parse_arguments

"""
"""
import asyncio

async def main(argv):
    args = parse_arguments(argv)
    try:
        be_perf = BehavePerformance(args)
        return await be_perf.run()
    except Exception as e:
        print(e)
        return False
   
if __name__ == "__main__":
   sys.exit(0 if asyncio.run(main(sys.argv[1:])) else 1)