from scigraph.scigraph_util import SciGraph
import json

sg = SciGraph()

def test_node():
    n = sg.node(id="MP:0000272")
    print(str(n))
    assert n.lbl == "abnormal aorta morphology"

def test_bio_operations():
    zp="ZP:0004204"
    enodes = sg.phenotype_to_entity_list(id=zp)
    assert len(enodes)>0
