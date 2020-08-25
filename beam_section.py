import ezdxf
import numpy

doc = ezdxf.new(dxfversion='R2010')
doc.header['$MEASUREMENT'] = 1
doc.header['$INSUNITS'] = 4 # mil

# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.new('TEXTLAYER', dxfattribs={'color': 2})
doc.layers.new('STRCUT', dxfattribs={'color': 5})
doc.layers.new('REBAR', dxfattribs={'color': 1})

msp = doc.modelspace()

#input format
beam_data = [{
  "width": 200,
  "height": 500,
  "rebar_options": {
    "Top1": {
      "number": 2,
      "size": 16
    },
    "Bottom1": {
      "number": 4,
      "size": 20
    }
  }
}, {
  "width": 200,
  "height": 500,
  "rebar_options": {
    "Top1": {
      "number": 4,
      "size": 20
    },
    "Bottom1": {
      "number": 4,
      "size": 20
    }
  }
}, {
  "width": 200,
  "height": 500,
  "rebar_options": {
    "Top1": {
      "number": 4,
      "size": 20
    },
    "Bottom1": {
      "number": 4,
      "size": 20
    }
  }
}, {
  "width": 200,
  "height": 500,
  "rebar_options": {
    "Top1": {
      "number": 4,
      "size": 20
    },
    "Bottom1": {
      "number": 4,
      "size": 20
    }
    ,
    "Bottom2": {
      "number": 4,
      "size": 16
    }
  }
}, {
  "width": 200,
  "height": 500,
  "rebar_options": {
    "Top1": {
      "number": 4,
      "size": 20
    },
    "Bottom1": {
      "number": 4,
      "size": 20
    }
    ,
    "Bottom2": {
      "number": 4,
      "size": 16
    }
  }
}, {
  "width": 400,
  "height": 800,
  "rebar_options": {
    "Top1": {
      "number": 4,
      "size": 20
    },
    "Bottom1": {
      "number": 4,
      "size": 20
    }
    ,
    "Bottom2": {
      "number": 4,
      "size": 16
    }
  }
}, {
  "width": 300,
  "height": 600,
  "rebar_options": {
    "Top1": {
      "number": 4,
      "size": 20
    },
    "Bottom1": {
      "number": 4,
      "size": 20
    }
  }
}]

def plot_beam_section(w,d,locx,locy ,covering, rebar_options ):
    points = [(locx, locy), (locx + w, locy),(locx + w , locy + d), (locx, locy + d), (locx , locy)]
    msp.add_lwpolyline(points , dxfattribs={'layer': 'STRCUT'})
    dim = msp.add_aligned_dim(p1=(locx, locy), p2=(locx, locy + d), distance=100 ,
    override={
        'dimtxsty': 'Standard',
        'dimtxt': 30,
        'dimclrt': 1,
        'dimexe': 25,  # length above dimension line
        'dimexo': 50,  # offset from measurement point
    })
    dim.set_tick(size=25 )
    dim.render()


    dim = msp.add_aligned_dim(p1=(locx, locy + d), p2=(locx + w , locy + d)  , distance=100 ,
    override={
        'dimtxsty': 'Standard',
        'dimtxt': 30,
        'dimclrt': 1,
        'dimexe': 25,  # length above dimension line
        'dimexo': 50,  # offset from measurement point
    })
    dim.set_tick(size=25 )
    dim.render()

    msp.add_text("{} {} X {}".format("BEAM",str(w),str(d)),
             dxfattribs={
                 'style': 'Standard',
                 'height': 50}
             ).set_pos(((locx+w/2.00) - 30, locy -180), align='CENTER')
    
    if "Top1" in rebar_options.keys():

        number_of_rebar = int(rebar_options["Top1"]["number"])
        rebar_sizing = int(rebar_options["Top1"]["size"])
        loc_start = locx + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locx + w - (rebar_sizing/2.00) - covering # +- diameter
        loc_y =  d + locy - covering - (rebar_sizing/2.00)
        # placing_point = [[i , d + locy - covering - (rebar_sizing/2.00)] for i in numpy.linspace(loc_start , loc_end , (loc_end - loc_start)/number_of_rebar)]
        placing_point = [[i , loc_y] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
    
    if "Top2" in rebar_options.keys():

        number_of_rebar = int(rebar_options["Top2"]["number"])
        rebar_sizing = int(rebar_options["Top2"]["size"])
        loc_start = locx + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locx + w - (rebar_sizing/2.00) - covering # +- diameter
        loc_y =  d + locy - covering - (rebar_sizing/2.00)*2 - rebar_sizing
        # placing_point = [[i , d + locy - covering - (rebar_sizing/2.00)] for i in numpy.linspace(loc_start , loc_end , (loc_end - loc_start)/number_of_rebar)]
        placing_point = [[i , loc_y] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
    
    if "Bottom1" in rebar_options.keys():

        number_of_rebar = int(rebar_options["Bottom1"]["number"])
        rebar_sizing = int(rebar_options["Bottom1"]["size"])
        loc_start = locx + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locx + w - (rebar_sizing/2.00) - covering # +- diameter
        loc_y = locy + covering + (rebar_sizing/2.00)
        # placing_point = [[i , d + locy - covering - (rebar_sizing/2.00)] for i in numpy.linspace(loc_start , loc_end , (loc_end - loc_start)/number_of_rebar)]
        placing_point = [[i , loc_y] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})

    if "Bottom2" in rebar_options.keys():

        number_of_rebar = int(rebar_options["Bottom2"]["number"])
        rebar_sizing = int(rebar_options["Bottom2"]["size"])
        loc_start = locx + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locx + w - (rebar_sizing/2.00) - covering # +- diameter
        loc_y = locy + covering + (rebar_sizing/2.00)*2 + rebar_sizing
        # placing_point = [[i , d + locy - covering - (rebar_sizing/2.00)] for i in numpy.linspace(loc_start , loc_end , (loc_end - loc_start)/number_of_rebar)]
        placing_point = [[i , loc_y] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
    

    #stirrup no.1
    msp.add_line(start=(locx + covering , locy + covering + (rebar_sizing/2.00) ),end= (locx + covering , locy + d - covering - (rebar_sizing/2.00) ))
    msp.add_line(start=(locx + w - covering , locy + covering + (rebar_sizing/2.00) ),end= (locx + w - covering , locy + d - covering - (rebar_sizing/2.00) ))
    msp.add_line(start=(locx + covering + (rebar_sizing/2.00) , locy + covering ),end= (locx + w - covering - (rebar_sizing/2.00), locy + covering))
    msp.add_line(start=(locx + covering + (rebar_sizing/2.00) , locy + d - covering ),end= (locx + w - covering - (rebar_sizing/2.00), locy + d - covering))

for i , val in enumerate(beam_data):
    plot_beam_section(val["width"],val["height"], i * 1000 , 500 ,covering= 25 ,rebar_options = val["rebar_options"])


doc.saveas('test3.dxf')