"""Renderizador HTML com template pirâmide."""
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, BaseLoader


# Template inline para casos sem arquivo externo
INLINE_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Synapsis Mind Map</title>
    <style>
        :root {
            --bg-primary: #0a0a0f;
            --bg-card: #1a1a24;
            --bg-hover: #252532;
            --text-primary: #f5f5f7;
            --text-secondary: #8e8e93;
            --border-color: #2c2c3a;
            --accent: #6366f1;
            --line-color: #3a3a4a;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', -apple-system, sans-serif;
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
            overflow: auto;
        }
        .app { min-width: fit-content; padding: 40px; display: flex; flex-direction: column; align-items: center; }
        .header { position: fixed; top: 20px; left: 20px; z-index: 100; }
        .badge {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 8px 16px; background: var(--bg-card);
            border: 1px solid var(--border-color); border-radius: 100px;
            font-size: 12px; color: var(--text-secondary);
        }
        .badge::before { content: ''; width: 6px; height: 6px; background: #34c759; border-radius: 50%; }
        .mind-map { display: flex; flex-direction: column; align-items: center; padding-top: 60px; }
        .node { display: flex; flex-direction: column; align-items: center; }
        .node-content {
            display: flex; align-items: center; gap: 10px;
            padding: 12px 20px; background: var(--bg-card);
            border: 1px solid var(--border-color); border-radius: 12px;
            cursor: pointer; transition: all 0.2s; white-space: nowrap; position: relative;
        }
        .node-content::before {
            content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
            border-radius: 12px 0 0 12px; background: var(--node-color, var(--accent));
        }
        .node-content:hover {
            background: var(--bg-hover); border-color: var(--node-color, var(--accent));
            transform: scale(1.02); box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .node-icon { font-size: 18px; }
        .node-text { font-size: 14px; font-weight: 500; }
        .node-root > .node-content {
            padding: 16px 28px; background: linear-gradient(135deg, var(--bg-card), #1e1e2e);
            border: 2px solid var(--accent); box-shadow: 0 0 40px rgba(99,102,241,0.15);
        }
        .node-root > .node-content .node-icon { font-size: 24px; }
        .node-root > .node-content .node-text { font-size: 18px; font-weight: 600; }
        .node-connector { width: 2px; height: 24px; background: var(--line-color); }
        .node-children {
            display: flex; flex-direction: row; align-items: flex-start;
            position: relative; padding-top: 24px;
        }
        .node-children.hidden { display: none; }
        .node-children::before {
            content: ''; position: absolute; top: 0; height: 2px;
            background: var(--line-color); left: 50px; right: 50px;
        }
        .node-children:has(.node-branch:only-child)::before { display: none; }
        .node-branch {
            display: flex; flex-direction: column; align-items: center;
            padding: 0 12px; position: relative;
        }
        .node-branch::before {
            content: ''; position: absolute; top: -24px; left: 50%;
            transform: translateX(-50%); width: 2px; height: 24px; background: var(--line-color);
        }
        .node-branch .node-content { padding: 10px 16px; }
        .node-branch .node-icon { font-size: 16px; }
        .node-branch .node-text { font-size: 13px; }
        .node-branch .node-branch .node-content { padding: 8px 14px; background: rgba(26,26,36,0.7); }
        .node-branch .node-branch .node-icon { font-size: 14px; }
        .node-branch .node-branch .node-text { font-size: 12px; }
        .node-branch .node-branch .node-branch .node-content { padding: 6px 12px; background: rgba(26,26,36,0.5); }
        .node-branch .node-branch .node-branch .node-text { font-size: 11px; color: var(--text-secondary); }
        .toggle-btn {
            position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%);
            width: 16px; height: 16px; background: #12121a;
            border: 1px solid var(--border-color); border-radius: 50%;
            color: #636366; cursor: pointer; display: flex;
            align-items: center; justify-content: center; font-size: 8px; z-index: 10;
        }
        .toggle-btn:hover { background: var(--bg-hover); border-color: var(--accent); color: var(--text-primary); }
        .toggle-btn.collapsed { transform: translateX(-50%) rotate(-90deg); }
    </style>
</head>
<body>
    <div class="app">
        <header class="header"><div class="badge">Synapsis</div></header>
        <div id="mindMap" class="mind-map"></div>
    </div>
    <script>
        const DATA = {{ data | safe }};
        
        function renderNode(node, isRoot = false) {
            const div = document.createElement('div');
            div.className = `node ${isRoot ? 'node-root' : ''}`;
            
            const content = document.createElement('div');
            content.className = 'node-content';
            if (node.color) content.style.setProperty('--node-color', node.color);
            
            if (node.icon) {
                const icon = document.createElement('span');
                icon.className = 'node-icon';
                icon.textContent = node.icon;
                content.appendChild(icon);
            }
            
            const text = document.createElement('span');
            text.className = 'node-text';
            text.textContent = node.title;
            content.appendChild(text);
            div.appendChild(content);
            
            if (node.children?.length) {
                const toggle = document.createElement('button');
                toggle.className = `toggle-btn ${node.expanded === false ? 'collapsed' : ''}`;
                toggle.innerHTML = '▼';
                toggle.onclick = (e) => {
                    e.stopPropagation();
                    const children = div.querySelector(':scope > .node-children');
                    const connector = div.querySelector(':scope > .node-connector');
                    if (children) {
                        children.classList.toggle('hidden');
                        if (connector) connector.classList.toggle('hidden');
                        toggle.classList.toggle('collapsed');
                    }
                };
                content.appendChild(toggle);
                
                const connector = document.createElement('div');
                connector.className = `node-connector ${node.expanded === false ? 'hidden' : ''}`;
                div.appendChild(connector);
                
                const childrenDiv = document.createElement('div');
                childrenDiv.className = `node-children ${node.expanded === false ? 'hidden' : ''}`;
                node.children.forEach(child => {
                    const branch = document.createElement('div');
                    branch.className = 'node-branch';
                    branch.appendChild(renderNode(child));
                    childrenDiv.appendChild(branch);
                });
                div.appendChild(childrenDiv);
            }
            return div;
        }
        
        document.getElementById('mindMap').appendChild(renderNode(DATA, true));
    </script>
</body>
</html>'''


def get_template_path() -> Path:
    """Retorna caminho do template pyramid.html."""
    return Path(__file__).parent.parent / "templates" / "pyramid.html"


def render_html(yaml_str: str, output: str = None) -> str:
    """Renderiza YAML em HTML standalone. Retorna caminho do arquivo."""
    import yaml as pyyaml
    import json
    
    data = pyyaml.safe_load(yaml_str)
    data_json = json.dumps(data, ensure_ascii=False)
    
    # Usa template inline com Jinja2
    env = Environment(loader=BaseLoader())
    template = env.from_string(INLINE_TEMPLATE)
    html = template.render(data=data_json)
    
    # Define output path
    if output is None:
        output = "mindmap.html"
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    
    return str(output_path.absolute())
