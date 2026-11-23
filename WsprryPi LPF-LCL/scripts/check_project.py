"""Check fixed interfaces, local assets, placement grids, and exported netlist.

Run after KiCad CLI exports generated/connectivity.net. Standard library only.
The interface contract records the original C-first board's exact geometry.
"""
from pathlib import Path
import json, math, re
from sexp import parse, child, children, val, uq

PROJECT = Path(__file__).resolve().parents[1]
NAME = PROJECT.name

def reference(fp):
    return next(uq(x[2]) for x in children(fp, 'property') if uq(x[1]) == 'Reference')

def clean(node):
    return [clean(x) if isinstance(x, list) else x for x in node
            if not (isinstance(x, list) and x and x[0] == 'uuid')]

def interface(board):
    result = {'outline': [], 'connectors': {}}
    for item in board:
        if not isinstance(item, list):
            continue
        if item[0].startswith('gr_') and child(item, 'layer') == ['layer', '"Edge.Cuts"']:
            result['outline'].append(clean(item))
    for fp in children(board, 'footprint'):
        ref = reference(fp)
        if ref in ['J1', 'J2', 'J3']:
            result['connectors'][ref] = {key: [clean(x) for x in children(fp, key)]
                                        for key in ['at', 'layer', 'pad', 'model']}
    result['outline'].sort(key=str)
    return result

def xy_world(fp, pad):
    at = child(fp, 'at'); angle = math.radians(float(at[3]) if len(at) > 3 else 0)
    x, y = map(float, child(pad, 'at')[1:3])
    return (float(at[1])+x*math.cos(angle)+y*math.sin(angle),
            float(at[2])-x*math.sin(angle)+y*math.cos(angle))

def main():
    board = parse((PROJECT/(NAME+'.kicad_pcb')).read_text())
    schematic = parse((PROJECT/(NAME+'.kicad_sch')).read_text())
    contract = json.loads((PROJECT/'validation/interface-contract.json').read_text())
    current_interface = interface(board)
    assert current_interface['outline'] == contract['interface']['outline'], 'Fixed outline changed'
    assert current_interface['connectors']['J1'] == contract['interface']['connectors']['J1'], 'Fixed headers changed'
    fps = {reference(fp): fp for fp in children(board, 'footprint')}
    assert set(fps) == {'J1','J2','J3','L1','L3','L5','CA2','CB2','CA4','CB4'}
    for ref, x, angle in [('J2',114.0,-90.0),('J3',159.96,90.0)]:
        fp = fps[ref]
        assert uq(fp[1]) == NAME+':SMA_Adafruit_1865_EdgeMount'
        assert [float(v) for v in child(fp,'at')[1:]] == [x,99.12,angle]
        assert len(children(fp,'pad')) == 5
        for pad in children(fp,'pad'):
            assert abs(float(child(pad,'at')[2])+2.057) < 1e-6
            assert abs(float(child(pad,'size')[2])-4.014) < 1e-6
            expected_net = ('/RF_IN' if ref=='J2' else '/RF_OUT') if uq(pad[1])=='1' else 'GND'
            assert uq(val(pad,'net')) == expected_net
    rules = (PROJECT/(NAME+'.kicad_dru')).read_text()
    assert "A.Type == 'Pad'" in rules and "B.Type == 'Pad'" in rules
    assert "memberOfFootprint('J2')" in rules and "memberOfFootprint('J3')" in rules
    assert '(constraint edge_clearance (min 0mm))' in rules
    settings = json.loads((PROJECT/(NAME+'.kicad_pro')).read_text())
    assert settings['board']['design_settings']['rules']['min_copper_edge_clearance'] == .5
    for ref, fp in fps.items():
        if ref not in ['J1','J2','J3']:
            assert all(abs(float(x)/.25-round(float(x)/.25)) < 1e-6
                       for x in child(fp,'at')[1:3]), ref
    # Only electrical symbol origins, label anchors, and wire endpoints use the
    # 50 mil connection grid; graphic/property positions are not connections.
    for item in schematic:
        if isinstance(item,list) and item[0] in ['symbol','label','junction','wire']:
            points = children(item,'at') if item[0]!='wire' else children(child(item,'pts'),'xy')
            for point in points:
                assert all(abs(float(x)/1.27-round(float(x)/1.27)) < 1e-6 for x in point[1:3]), point
    spacings = []
    for a,b in [('CA2','CB2'),('CA4','CB4')]:
        pads = {ref: {uq(p[1]):xy_world(fps[ref],p) for p in children(fps[ref],'pad')} for ref in [a,b]}
        for ref in [a,b]:
            assert abs(math.dist(pads[ref]['1'],pads[ref]['2'])-2.5)<1e-6
        for left,right in [(pads[a]['1'],pads[b]['2']),(pads[b]['1'],pads[a]['2'])]:
            assert abs(math.dist(left,right)-5)<1e-6
        spacings.append({'pair':[a,b], 'individual_pitch_mm':2.5, 'cross_pair_pitch_mm':5.0})
    for fp in fps.values():
        assert uq(fp[1]).startswith(NAME+':')
        footprint = uq(fp[1]).split(':',1)[1]
        assert (PROJECT/'libraries/footprints'/f'{NAME}.pretty'/f'{footprint}.kicad_mod').is_file()
    sources = [PROJECT/(NAME+'.kicad_pcb'), *list((PROJECT/'libraries').rglob('*.kicad_mod'))]
    models = set()
    for source in sources:
        for path in re.findall(r'\(model "([^"]+)"', source.read_text()):
            assert path.startswith('${KIPRJMOD}/')
            local = PROJECT/path.removeprefix('${KIPRJMOD}/')
            assert local.is_file(),local
            models.add(str(local.relative_to(PROJECT)))
    library = parse((PROJECT/'libraries/symbols'/f'{NAME}.kicad_sym').read_text())
    library_symbols = {uq(s[1]) for s in children(library,'symbol')}
    for symbol in children(schematic,'symbol'):
        nickname, symbol_name = uq(val(symbol,'lib_id')).split(':',1)
        assert nickname==NAME and symbol_name in library_symbols
    netlist = parse((PROJECT/'generated/connectivity.net').read_text())
    nets = {uq(val(net,'name')):{(uq(val(n,'ref')),uq(val(n,'pin'))) for n in children(net,'node')}
            for net in children(child(netlist,'nets'),'net')}
    expected = {
      '/RF_IN':{('J1','2'),('J1','3'),('J2','1'),('L1','2')},
      '/LPF_NODE1':{('L1','1'),('L3','2'),('CA2','2'),('CB2','2')},
      '/LPF_NODE2':{('L3','1'),('L5','2'),('CA4','2'),('CB4','2')},
      '/RF_OUT':{('L5','1'),('J1','6'),('J1','7'),('J3','1')},
      'GND':{('J1','1'),('J1','4'),('J1','5'),('J1','8'),('J2','2'),('J3','2'),
             ('CA2','1'),('CB2','1'),('CA4','1'),('CB4','1')}}
    assert nets==expected, nets
    report={'fixed_outline_and_headers_match':True,'adafruit_edge_launch_geometry_verified':True,
            'global_copper_edge_clearance_mm':.5,'SMA_pad_edge_clearance_override_mm':0,
            'SMA_copper_setback_mm':.05,'filter_placement_grid_mm':.25,
            'schematic_connection_grid_mm':1.27,'fixed_connector_grid_exceptions':['J1','J2','J3'],
            'capacitor_mounting':spacings,'local_model_count':len(models),
            'local_symbol_count':len(library_symbols),'local_footprint_count':len(list((PROJECT/'libraries/footprints').rglob('*.kicad_mod'))),
            'independent_netlist_topology_verified':True}
    (PROJECT/'validation/geometry-and-connectivity.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
