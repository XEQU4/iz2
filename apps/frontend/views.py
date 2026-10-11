"""Serve the compiled React application without changing saved domain data."""
import json
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render


MAX_STATIC_CHUNKS = 1024
MAX_STATIC_IMPORTS = 4096
MAX_STATIC_STYLES = 4096


def _relative_path(name):
    if (
        not isinstance(name, str)
        or not name
        or not name.isprintable()
        or any(character in name for character in '\\:%?#')
        or any(part in ('', '.', '..') for part in name.split('/'))
    ):
        raise ValueError('Invalid frontend manifest path.')
    return name


def _asset_url(name):
    name = _relative_path(name)
    if not name.startswith('assets/'):
        raise ValueError('Invalid frontend asset path.')
    # Vite imports refer to its own hashed names. A second storage hash
    # would give the entry two URLs, re-running React and its contexts.
    return settings.STATIC_URL.rstrip('/') + '/frontend/' + name


def _frontend_assets(entries):
    if not isinstance(entries, dict):
        raise ValueError('Invalid frontend manifest.')

    # Static chunks can own CSS even when the entry has its own stylesheet.
    # Visit dependencies first so the entry's styles retain their cascade.
    # An iterative walk handles valid chunk cycles without recursion limits.
    pending = [('index.html', False)]
    visited = set()
    style_urls = []
    seen_styles = set()
    import_count = style_count = 0
    while pending:
        key, completed = pending.pop()
        if completed:
            for name in entries[key].get('css', []):
                url = _asset_url(name)
                if url not in seen_styles:
                    seen_styles.add(url)
                    style_urls.append(url)
            continue
        if key in visited:
            continue
        _relative_path(key)
        chunk = entries[key]
        if not isinstance(chunk, dict):
            raise ValueError('Invalid frontend chunk.')
        _asset_url(chunk['file'])
        imports, styles = chunk.get('imports', []), chunk.get('css', [])
        if not isinstance(imports, list) or not isinstance(styles, list):
            raise ValueError('Invalid frontend chunk dependencies.')
        import_count += len(imports)
        style_count += len(styles)
        if (
            len(visited) >= MAX_STATIC_CHUNKS
            or import_count > MAX_STATIC_IMPORTS
            or style_count > MAX_STATIC_STYLES
        ):
            raise ValueError('Frontend dependency limits exceeded.')
        for dependency in imports:
            _relative_path(dependency)
        for name in styles:
            _asset_url(name)
        visited.add(key)
        pending.append((key, True))
        pending.extend((dependency, False) for dependency in reversed(imports))
        # dynamicImports belong to Vite's lazy loader, not the initial document.
    return {
        'entry_script': _asset_url(entries['index.html']['file']),
        'entry_styles': style_urls,
    }


def home(request):
    return redirect('/app/')


def index(request, path=''):
    candidates = [Path(settings.STATIC_ROOT) / 'frontend/vite-manifest.json', Path(settings.BASE_DIR) / 'static/frontend/vite-manifest.json']
    manifest = next((item for item in candidates if item.is_file()), None)
    if manifest is None:
        return HttpResponse('The React interface has not been built. Run npm.cmd ci and npm.cmd run build in frontend, then python manage.py collectstatic --noinput and restart Django.', status=503, content_type='text/plain; charset=utf-8')
    try:
        entries = json.loads(manifest.read_text(encoding='utf-8'))
        context = _frontend_assets(entries)
        response = render(request, 'frontend/index.html', context)
        response['Cache-Control'] = 'no-cache'
        return response
    except (KeyError, TypeError, ValueError, OSError):
        return HttpResponse('The React build or static manifest is incomplete. Rebuild frontend, collect static assets and restart Django.', status=503, content_type='text/plain; charset=utf-8')
