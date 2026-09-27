"""ip-stresser-lab — plugin-host IP stresser.

Public surface:
    - PluginHost          : boot + lifecycle owner
    - ExtensionRegistry   : plugin discovery / load / unload
    - StressContract      : the interface every extension implements
"""

__version__ = "0.6.3"

from ip_stresser_lab.core.host import PluginHost
from ip_stresser_lab.core.registry import ExtensionRegistry
from ip_stresser_lab.contracts.stress_contract import StressContract

__all__ = ["PluginHost", "ExtensionRegistry", "StressContract", "__version__"]