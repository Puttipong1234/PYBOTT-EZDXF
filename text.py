import ezdxf

# Create a new DXF document.
doc = ezdxf.new(dxfversion='R2010')

# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.new('TEXTLAYER', dxfattribs={'color': 2})

# DXF entities (LINE, TEXT, ...) reside in a layout (modelspace, 
# paperspace layout or block definition).  
msp = doc.modelspace()

# Add entities to a layout by factory methods: layout.add_...() 
for i in range(0,100,10):
    # msp.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
    msp.add_text(
        'Beam 200 x 200', 
        dxfattribs={
            'layer': 'TEXTLAYER'
        }).set_pos((i, i + 0.2), align='CENTER')

# Save DXF document.
doc.saveas('test.dxf')