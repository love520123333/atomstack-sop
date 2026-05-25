import zipfile, xml.etree.ElementTree as ET, json

xlsx_path = 'C:/Users/amyxu/Music/海外客服SOP&邮件模板.xlsx'
ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    ss_xml = z.read('xl/sharedStrings.xml')
    ss_root = ET.fromstring(ss_xml)
    shared = []
    for si in ss_root.findall(f'{{{ns}}}si'):
        t = si.find(f'{{{ns}}}t')
        if t is not None:
            shared.append(t.text or '')
        else:
            parts = []
            for r in si.findall(f'{{{ns}}}r'):
                rt = r.find(f'{{{ns}}}t')
                if rt is not None and rt.text:
                    parts.append(rt.text)
            shared.append(''.join(parts))

    wb_xml = z.read('xl/workbook.xml')
    wb_root = ET.fromstring(wb_xml)
    
    rels_xml = z.read('xl/_rels/workbook.xml.rels')
    rels_root = ET.fromstring(rels_xml)
    rns = 'http://schemas.openxmlformats.org/package/2006/relationships'
    rid_to_file = {}
    for rel in rels_root.findall(f'{{{rns}}}Relationship'):
        rid_to_file[rel.attrib['Id']] = rel.attrib['Target']
    
    sheets_info = []
    for s in wb_root.findall(f'.//{{{ns}}}sheet'):
        rid = s.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        fname = rid_to_file.get(rid, '')
        sheets_info.append({'name': s.attrib['name'], 'file': fname})
    
    def cell_val(c, shared):
        t = c.attrib.get('t', '')
        v = c.find(f'{{{ns}}}v')
        if v is None:
            return ''
        if t == 's':
            return shared[int(v.text)]
        return v.text or ''
    
    all_data = {}
    for sh in sheets_info:
        fname = 'xl/' + sh['file'] if not sh['file'].startswith('xl/') else sh['file']
        if fname not in z.namelist():
            continue
        ws_xml = z.read(fname)
        ws_root = ET.fromstring(ws_xml)
        rows_data = []
        for row in ws_root.findall(f'.//{{{ns}}}row'):
            row_cells = {}
            for c in row.findall(f'{{{ns}}}c'):
                col_ref = ''.join(filter(str.isalpha, c.attrib.get('r', '')))
                row_cells[col_ref] = cell_val(c, shared)
            if any(v for v in row_cells.values()):
                rows_data.append(row_cells)
        all_data[sh['name']] = rows_data

with open('C:/Users/amyxu/WorkBuddy/20260525151842/sheet_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print('Done. Sheets:', list(all_data.keys()))
for name, rows in all_data.items():
    print(f'  {name}: {len(rows)} rows')
