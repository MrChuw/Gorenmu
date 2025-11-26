import asyncio
import contextlib
import importlib
import importlib.util
import os
import pkgutil
import sys
import threading
from typing import Any

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

_watched_files: dict[str, dict[str, Any]] = {}
_observer = None
_observed_dirs: set[str] = set()
_watch_lock = threading.Lock()
_handler = None


class _ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        with _watch_lock:
            for info in _watched_files.values():
                with contextlib.suppress(FileNotFoundError):
                    if os.path.samefile(event.src_path, info["path"]):
                        info["changed"] = True


def _ensure_observer_for(path: str):
    global _observer, _handler
    if _observer is None:
        _observer = Observer()
        if not _handler:
            _handler = _ReloadHandler()
    dirpath = os.path.dirname(path)
    if dirpath not in _observed_dirs:
        _observer.schedule(_handler, path=dirpath, recursive=False)
        _observed_dirs.add(dirpath)
    if not _observer.is_alive():
        _observer.start()


def _force_reload(module_name: str, element: str) -> Any:
    spec = importlib.util.find_spec(module_name)
    if spec and spec.submodule_search_locations:
        prefix = f"{module_name}."
        for _, name, _ in pkgutil.walk_packages(spec.submodule_search_locations, prefix):
            sys.modules.pop(name, None)
    sys.modules.pop(module_name, None)
    importlib.invalidate_caches()
    mod = importlib.import_module(module_name)
    return getattr(mod, element)


async def reload_and_get(module_name: str, element: str, force: bool = False) -> Any:
    spec = importlib.util.find_spec(module_name)
    if spec is None or spec.origin is None:
        raise ImportError(f"Cannot find module {module_name}")

    module_file = os.path.abspath(spec.origin)

    if force:
        return _force_reload(module_name, element)

    _ensure_observer_for(module_file)

    with _watch_lock:
        entry = _watched_files.get(module_name)
        if entry is None:
            _watched_files[module_name] = {"path": module_file, "changed": False}
            return _force_reload(module_name, element)
        if entry.get("changed"):
            entry["changed"] = False
            return _force_reload(module_name, element)

    await asyncio.sleep(0)
    return getattr(importlib.import_module(module_name), element)


async def reload_and_get_authorized(module_name: str, element: str, force: bool = False) -> Any:
    return await reload_and_get(module_name, element, force=force)


async def reload_all_translations(element: str, force: bool = False) -> list[Any]:
    results: list[Any] = []
    cogs_pkg = sys.modules["bot.cogs"]
    for _, cog_name, is_pkg in pkgutil.iter_modules(cogs_pkg.__path__, prefix="bot.cogs."):
        if not is_pkg:
            continue
        for cmd_pkg_name in (f"{cog_name}.commands", f"{cog_name}.command"):
            cmd_pkg = sys.modules.get(cmd_pkg_name, None)
            if not cmd_pkg:
                continue
            for _, mod_name, _ in pkgutil.iter_modules(cmd_pkg.__path__, prefix=f"{cmd_pkg_name}."):
                if mod_name.endswith(".translations"):
                    try:
                        val = await reload_and_get(mod_name, element, force=force)
                        results.append(val)
                    except Exception as e:
                        print(f"Failed to reload {mod_name}: {e}")
    return results


# # -*- coding: utf-8 -*-
# import asyncio
# import contextlib
# import importlib
# import importlib.util
# import importlib.util
# import os
# import pkgutil
# import sys
# import threading
# from typing import Any, List
#
# from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer
#
# _watched_files: dict[str, dict[str, Any]] = {}
# _observer = None
# _observed_dirs: set[str] = set()
# _watch_lock = threading.Lock()
# _handler = None
#
#
# class _ReloadHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         if event.is_directory:
#             return
#         with _watch_lock:
#             for mod_name, info in _watched_files.items():
#                 with contextlib.suppress(FileNotFoundError):
#                     if os.path.samefile(event.src_path, info["path"]):
#                         info["changed"] = True
#
#
# def _ensure_observer_for(path: str):
#     global _observer, _handler
#     if _observer is None:
#         _observer = Observer()
#         if not _handler:
#             _handler = _ReloadHandler()
#     dirpath = os.path.dirname(path)
#     if dirpath not in _observed_dirs:
#         _observer.schedule(_handler, path=dirpath, recursive=False)
#         _observed_dirs.add(dirpath)
#     if not _observer.is_alive():
#         _observer.start()
#
#
# async def _maybe_reload_and_get(module_name: str, element: str) -> Any:
#     spec = importlib.util.find_spec(module_name)
#     if spec is None or spec.origin is None:
#         raise ImportError(f"Cannot find module {module_name}")
#     module_file = os.path.abspath(spec.origin)
#     _ensure_observer_for(module_file)
#     with _watch_lock:
#         entry = _watched_files.get(module_name)
#         if entry is None:
#             _watched_files[module_name] = {"path": module_file, "changed": False}
#             return reload_and_get(module_name, element)
#         if entry.get("changed"):
#             entry["changed"] = False
#             return reload_and_get(module_name, element)
#     await asyncio.sleep(0)
#     return getattr(importlib.import_module(module_name), element)
#
#
# def reload_and_get(module_name: str, element: str):
#     spec = importlib.util.find_spec(module_name)
#     if spec and spec.submodule_search_locations:
#         prefix = f"{module_name}."
#         for _, name, _ in pkgutil.walk_packages(spec.submodule_search_locations, prefix):
#             sys.modules.pop(name, None)
#     sys.modules.pop(module_name, None)
#     importlib.invalidate_caches()
#     mod = importlib.import_module(module_name)
#     return getattr(mod, element)
#
#
# async def reload_and_get_authorized(module_name: str, element: str) -> Any:
#     return await _maybe_reload_and_get(module_name, element)
#
#
# async def reload_all_translations(element: str) -> List[Any]:
#     results: List[Any] = []
#     cogs_pkg = sys.modules["bot.cogs"]
#     for _, cog_name, is_pkg in pkgutil.iter_modules(cogs_pkg.__path__, prefix="bot.cogs."):
#         if not is_pkg:
#             continue
#         for cmd_pkg_name in (f"{cog_name}.commands", f"{cog_name}.command"):
#             cmd_pkg = sys.modules.get(cmd_pkg_name, None)
#             if not cmd_pkg:
#                 continue
#             for _, mod_name, _ in pkgutil.iter_modules(cmd_pkg.__path__, prefix=f"{cmd_pkg_name}."):
#                 if mod_name.endswith(".translations"):
#                     try:
#                         val = await _maybe_reload_and_get(mod_name, element)
#                         results.append(val)
#                     except Exception as e:
#                         print(f"Failed to reload {mod_name}: {e}")
#     return results
