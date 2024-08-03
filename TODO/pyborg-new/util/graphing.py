import json
import logging
import pydot
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
from pprint import pprint
logger = logging.getLogger(__name__)
from networkx.drawing.nx_agraph import write_dot
import subprocess
import random
from colorsys import hls_to_rgb
import unicodedata

graph_configs = {
    'normal': {"nodesep": "0.5", "ranksep": "1", "splines": "true", "bgcolor": "#2e2e2e", "rankdir": "LR"},
    'dashed': {'style': 'dashed'},
    'dotted': {'style': 'dotted'},
}

node_configs = {
    'normal': {'shape': 'ellipse', 'style': 'filled', 'fillcolor': 'white', 'fontsize': '12', 'fontcolor': 'black'},
    'dashed': {'shape': 'circle', 'style': 'filled', 'fillcolor': '#d3d3d3', 'fontsize': '12', 'fontcolor': 'black'},
    'dotted': {'shape': 'circle', 'style': 'filled', 'fillcolor': '#d3d3d3', 'fontsize': '12', 'fontcolor': 'black'},
}

edge_configs = {
    "normal": {"shape": "circle", "style": "filled", "fillcolor": "#d3d3d3", "fontsize": "12", "fontcolor": "black",
               'color': 'white', 'penwidth': '2', 'arrowhead': 'normal'},
    'dashed': {'color': 'white', 'penwidth': '2', 'style': 'dashed', 'arrowhead': 'normal', 'fontcolor': 'black'},
    'dotted': {'color': 'white', 'penwidth': '2', 'style': 'dotted', 'arrowhead': 'normal', 'fontcolor': 'black'},
}

arrow_types = ['normal', 'inv', 'dot', 'odot', 'none', 'tee', 'empty', 'diamond', 'ediamond', 'obox', 'crow', 'icurve', 'lcurve', 'box', 'open']

used_colors = []
num_colors = 70000

used_colors = []

def random_color():
    global used_colors
    while True:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if color in used_colors:
            continue
        else:
            used_colors.append(color)
            return color


def normalize_node_name(name):
    # Remove acentos e normaliza para NFC (Compatibilidade de Composição Normalizada)
    normalized_name = unicodedata.normalize('NFC', name)
    # Remove caracteres especiais e espaços
    normalized_name = ''.join(c for c in normalized_name if unicodedata.category(c) != 'Mn' and c.isalnum() or c.isspace())
    # Substitui espaços por _
    normalized_name = normalized_name.replace(' ', '_')
    return normalized_name

# Função para gerar a imagem do grafo usando um motor de layout específico.
def generate_graph_image(G, layout='dot', output_file='graph_demo', format='svg'):
    """
    Gera a imagem do grafo usando um motor de layout específico.

    Args:
        G (networkx.Graph): Grafo a ser visualizado.
        layout (str): Motor de layout do Graphviz a ser usado.
        output_file (str): Caminho do arquivo de saída sem extensão.
        format (str): Formato da imagem de saída (e.g., 'svg', 'pdf', 'png').
    """
    # Defina os atributos do grafo
    G.graph.update(graph_configs['normal'])  # Layout da esquerda para a direita

    # Defina atributos dos nós
    for node in G.nodes():
        G.nodes[node].update(node_configs['normal'])


    # Escreva o grafo no formato DOT
    dot_file = output_file.replace(f"_{layout}", '') + '.dot'
    write_dot(G, dot_file)

    # Use o Graphviz para converter o arquivo DOT em uma imagem.
    # subprocess.run([layout, f'-T{format}', dot_file, '-o', f'{output_file}.{format}'])

def networkx_demo(pyb, graphics=False, export=False, dot=False, limit=70):
    G = nx.Graph()
    print(pyb)
    color_index = 0
    limit = 2063
    for counter, word in enumerate(pyb.words.keys()):
        # if counter >= limit:
        #     break
        if word is None or word.strip() == "":
            continue

        # cleaned_word = normalize_node_name(word)
        if word == "%":
            word = "->%"
        G.add_node(word, label=word)
        if word == "->%":
            word = "%"
        for p in pyb.words[word]:
            # Atribui uma cor única a cada aresta.
            edge_color = random_color()
            edge_config = edge_configs['normal'].copy()  # Cria uma cópia da configuração padrão
            edge_config['color'] = edge_color  # Define a cor única
            edge_config['fontcolor'] = edge_color  # Define a cor do texto da aresta como a mesma
            edge_config['arrowhead'] = random.choice(arrow_types)
            target_node = pyb.lines.get(p["hashval"], [None])[0]
            if target_node is None or target_node.strip() == "":
                continue  # P
            if word == "%":
                word = "->%"
            G.add_edge(word, pyb.lines[p["hashval"]][0], **edge_config)

            color_index += 1

            # G.add_edge(word, pyb.lines[p["hashval"]][0], **edge_configs['normal'])

    logger.debug(G)

    if dot:
        nx.nx_agraph.write_dot(G, "./graph_demo.dot")
    if graphics:
        nx.draw(G, with_labels=True)
        plt.show()
    if export:
        data = json_graph.node_link_data(G)
        s = json.dumps(data)
        return s

    # Gerar a imagem usando o layout 'dot' (padrão)
    generate_graph_image(G, layout='dot', output_file='graph_dot', format='svg')

    # Gerar a imagem usando o layout 'neato'
    # generate_graph_image(G, layout='neato', output_file='graph_neato')

    # Gerar a imagem usando o layout 'fdp'
    # generate_graph_image(G, layout='fdp', output_file='graph_fdp', format='svg')

    # Gerar a imagem usando o layout 'sfdp'
    # generate_graph_image(G, layout='sfdp', output_file='graph_sfdp', format='svg')

    # Gerar a imagem usando o layout 'twopi'
    # generate_graph_image(G, layout='twopi', output_file='graph_twopi', format='svg')

    # Gerar a imagem usando o layout 'circo'
    # generate_graph_image(G, layout='circo', output_file='graph_circo', format='svg')

    return G
