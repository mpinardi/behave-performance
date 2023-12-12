import sys
import asyncio
from behave_performance.runtime import BehavePerformance
from behave_performance.configuration import Configuration

async def main(argv):
    """Behave Performance Command Line Main

    Args:
        argv (value args): Command line arguments.

    Returns:
        bool: The result of behave performance.
    """
    config = Configuration(argv)
    try:
        be_perf = BehavePerformance(config)
        return await be_perf.run()
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    sys.exit(0 if asyncio.run(main(sys.argv[1:])) else 1)
