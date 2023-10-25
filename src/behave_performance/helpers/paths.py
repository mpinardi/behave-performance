import glob 
import os

def expand_plan_paths(plan_paths:[str])->[str]:
    """Expand plan paths to find all plan files.

    Args:
        plan_paths ([str]): The paths to check

    Returns:
        [str]: The expanded paths
    """
    plan_paths = [p.replace(r'(:\d+)*$', '')
                  for p in plan_paths]  # Strip line numbers
    return expand_paths(plan_paths, '.plan')


def expand_paths(unexpandedPaths:[str], defaultExtension:str)->[str]:
    """Iterate through paths and recursively find all files with the default extension.

    Args:
        unexpandedPaths ([str]): The list of starting paths.
        defaultExtension (str): The extension to search for.

    Returns:
        [str]: A list of paths to files using the extension
    """
    files = list()
    for path in unexpandedPaths:
        if os.path.isdir(path):
            files.extend(glob.glob(fix_slashes(os.path.join(path,'**'+defaultExtension)),recursive=True))
        else:
            files.append(path)
    return files

def get_absolute_path(path:str)->str:
    """Check if the path is abosulte or if it is relative. 
    `Return the path if absoulte else it combined with the working directory.

    Args:
        path (str): The path to check

    Returns:
        str: The absolute path
    """
    if os.path.isabs(path):
        return path
    return os.path.join(os.getcwd(),path)

    
def fix_slashes(path:str)->str:
    """Fix mixed os path slashes

    Args:
        path (str): the path

    Returns:
        str: a fixed path
    """
    if os.sep == '\\':
        return path.replace('/', '\\')
    else:
        return path.replace('\\', '/')



