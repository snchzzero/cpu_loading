#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import asyncio
import os
import sys
import asyncio
import nest_asyncio
nest_asyncio.apply()



async def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpu_loading.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

#loop2 = asyncio.get_event_loop()

if __name__ == '__main__':
    asyncio.run(main())
    #loop2.run_until_complete(main())
