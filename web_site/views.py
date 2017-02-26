# coding=utf-8
import json
import requests
from queue import Queue

from django.http import HttpResponse
MAX_QUEUE_SIZE = 500

que = Queue(MAX_QUEUE_SIZE)


def bfs(start_node, sought):
    """
        поиск в n-арном дереве в ширину
        :param start_node: стартовый узел (или корень)
        :param sought: искомое значение узла, критерий
        :return: искомый узел или предупреждение
    """

    que.put(start_node)
    start_node.update({'visited': True})

    if not sought:
        return {'Interrupted': '!!! parameter sought is none !!!'}

    while(not que.empty()):
        if que.full():
            return {'Interrupted': '!!! queue is full !!!'}

        node = que.get()
        if node.get('cat', {}).get('path', '') == sought:
            node.pop('visited')
            return node

        for child in node.get('child', node.get('tree', [])):
            if not child.get('visited'):
                que.put(child)
                child.update({'visited': True})

    return {'Warning': '!!! Sought node not found !!!'}

def get_nodes_path():
    return

def rend(request):
    path = request.GET.get('path', '')
    resourse = requests.get('http://api.samson-pharma.ru/v1/production/categories-tree?l=3&fields=id,title,path')

    try:
        tree = resourse.json()
    except:
        return {'response rejected': '!!! resourse tree is not json !!!'}

    return HttpResponse(json.dumps(bfs(tree, path)))
