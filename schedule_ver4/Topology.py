import copy
from collections import deque

class Topology:
    def __init__(self, flow_dic):
        self.flow_dic = flow_dic
        self.links = {}
        self.reverse_links = {}
        self.path_dic = {}
        self.load_links("links.txt")
        self.create_reverse_links()

    def load_links(self, links_file):
        try:
            with open(links_file, "r") as links_file:
                for i, line in enumerate(links_file.readlines(), start=1):
                    src, dst = line.strip().split()
                    self.links[(src, dst)] = {}
            
        except:
            raise ValueError(f"Invalid data, please check your \"list.txt\" file")

    def create_reverse_links(self):                                                         #建立每個links(topology.links)
        for counter, (link_name, link_data) in enumerate(self.links.items(), start=1):
            src = link_name[0]
            dst = link_name[1]
            self.reverse_links[(dst, src)] = {}     #建立每個反向links

        # 合併 reverse_links 到 links
        self.links.update(self.reverse_links)

    def routing(self):                                                                      #建立路徑(topology.path_dic)
        for flow_id, key in self.flow_dic.items():
            self.create_path(flow_id, key.get('Src'), key.get('Dst'))

    def create_path(self, flow_id, src, dst):
        links_traversed = self.find_path(src, dst)
        

        if links_traversed:
            self.path_dic[flow_id] = links_traversed
            # print(f"flow = {flow_id}")
            # print(f"links = {links_traversed}")
        else:
            print(f"Error: Path not found between {src} and {dst}.")

    def find_path(self, src, dst):
        queue = deque()
        visited = set()
        parent = {}
        found = False

        queue.append(src)
        visited.add(src)

        while queue:
            current_node = queue.popleft()
            if current_node == dst:
                found = True
                break

            matching_links = [link_name for link_name, link_data in self.links.items() if link_name[0] == current_node]

            for link_name in matching_links:
                next_node = link_name[1]

                if next_node not in visited and next_node not in queue:
                    queue.append(next_node)
                    visited.add(next_node)
                    parent[next_node] = current_node

        if found:
            return self.reconstruct_path(parent, src, dst)
        else:
            return None

    def reconstruct_path(self, parent, src, dst):
        path = []
        current_node = dst

        while current_node != src:
            for link_name, link_data in self.links.items():
                if link_name[0] == parent[current_node] and link_name[1] == current_node:
                    path.append(link_name)
                    
                    break
            current_node = parent[current_node]

        path.reverse()
        path_content = []
        for link in path :                                                     #['link1', 'link2', 'link3']
            path_content.append({"Ingress":link[0], "Egress":link[1]})

        return path_content



        
 
 