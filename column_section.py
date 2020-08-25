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

#input_format
column_data = [{
    "mark":"C1",
    "width":"300",
    "height":"300",
    "rebar_options": {
        #4mainbar
        "main":{
            "size":12
        },
        #extra_bar
        "vertical": {
            "number":3,
            "size":12
        }
        #extra_bar
        ,"horizontal":{
            "number":3,
            "size":12
        }
        ,"stirrup_1":{ #1 , 2, 2A , 2B , 3 , 3A , 3B
            "size":12
        }
        ,"stirrup_2A":{ #1 , 2, 2A , 2B , 3 , 3A , 3B สี่เหลี่ยม 45
            "size":12
        }
        ,"stirrup_2B":{ #1 , 2, 2A , 2B , 3 , 3A , 3B   สี่เหลี่ยม
            "size":12
        }

        # ,"stirrup_3A":{ #1 , 2, 2A , 2B , 3 , 3A , 3B     สี่เหลี่ยมตั้ง
        #     "size":12
        # }
        # ,"stirrup_3B":{ #1 , 2, 2A , 2B , 3 , 3A , 3B     สี่เหลี่ยมแนวนอน
        #     "size":12
        # }
    }
},
               {
    "mark":"C2",
    "width":"800",
    "height":"600",
    "rebar_options": {
        #extra_bar
        "vertical": {
            "number":5,
            "size":12
        },
        "vertical_2": {
            "number":5,
            "size":12
        }
        #extra_bar
        ,"horizontal":{
            "number":3,
            "size":12
        }
        ,"stirrup_1":{ #1 , 2, 2A , 2B , 3 , 3A , 3B
            "number":1,
            "size":12
        }
        # ,"stirrup_2A":{ #1 , 2, 2A , 2B , 3 , 3A , 3B สี่เหลี่ยม 45
        #     "number":1,
        #     "size":12
        # }
        # ,"stirrup_2B":{ #1 , 2, 2A , 2B , 3 , 3A , 3B   สี่เหลี่ยม
        #     "number":1,
        #     "size":12
        # }
        # ,"stirrup_3A":{ #1 , 2, 2A , 2B , 3 , 3A , 3B     สี่เหลี่ยมตั้ง
        #     "size":12
        # }
        # ,"stirrup_3B":{ #1 , 2, 2A , 2B , 3 , 3A , 3B     สี่เหลี่ยมแนวนอน
        #     "size":12
        # }
    }
},
               {
    "mark":"C3",
    "width":"1600",
    "height":"1000",
    "rebar_options": {
        #extra_bar
        "vertical": {
            "number":10,
            "size":12
        },
        "vertical_2": {
            "number":10,
            "size":12
        }
        #extra_bar
        ,"horizontal":{
            "number":6,
            "size":12
        }
        ,"stirrup_1":{ #1 , 2, 2A , 2B , 3 , 3A , 3B
            "number":2,
            "size":12
        }
        # ,"stirrup_2A":{ #1 , 2, 2A , 2B , 3 , 3A , 3B สี่เหลี่ยม 45
        #     "number":1,
        #     "size":12
        # }
        # ,"stirrup_2B":{ #1 , 2, 2A , 2B , 3 , 3A , 3B   สี่เหลี่ยม
        #     "number":1,
        #     "size":12
        # }
        ,"stirrup_3A":{ #1 , 2, 2A , 2B , 3 , 3A , 3B     สี่เหลี่ยมตั้ง
            "number":2,
            "size":12
        }
        ,"stirrup_3B":{ #1 , 2, 2A , 2B , 3 , 3A , 3B     สี่เหลี่ยมแนวนอน
            "number":2,
            "size":12
        }
    }
}]

def plot_column_section(w,h,locx,locy,covering, rebar_options):
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
    
    placing_point_horizontal = [] # history of placing point of rebar
    placing_point_vertical = []
    
    
    if "horizontal" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["horizontal"]["number"])
        rebar_sizing = int(rebar_options["horizontal"]["size"])
        loc_start = locx + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locx + w - (rebar_sizing/2.00) - covering # +- diameter
        loc_y_top =  d + locy - covering - (rebar_sizing/2.00)
        loc_y_bottom =  locy + covering + (rebar_sizing/2.00)
        
        # write 
        placing_point_top = [[i , loc_y_top] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        # top
        for i in placing_point_top:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
        placing_point_bottom = [[i , loc_y_bottom] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        # bottom
        for i in placing_point_bottom:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
        
        
        placing_point_horizontal = placing_point_top
        
        
    if "horizontal_2" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["horizontal_2"]["number"])
        rebar_sizing = int(rebar_options["horizontal_2"]["size"])
        
        # get location start - end
        loc_start = locx + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locx + w - (rebar_sizing/2.00) - covering # +- diameter
        loc_y_top =  d + locy - covering - (rebar_sizing/2.00)*2 - rebar_sizing
        loc_y_bottom =  locy + covering + (rebar_sizing/2.00)*2 + rebar_sizing
        
        # write 
        placing_point_top = [[i , loc_y_top] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point_top:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
        # write 
        placing_point_bottom = [[i , loc_y_bottom] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point_bottom:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
    
    if "vertical" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["vertical"]["number"])
        rebar_sizing = int(rebar_options["vertical"]["size"])
        
        # get location start - end vertical
        loc_start = locy + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locy + d - (rebar_sizing/2.00) - covering # +- diameter
        loc_x_right =  w + locx - covering - (rebar_sizing/2.00)
        loc_x_left =  locx + covering + (rebar_sizing/2.00)
        
        placing_point_right = [[i , loc_x_right] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point_right:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
        placing_point_left = [[i , loc_x_left] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point_left:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
        placing_point_vertical = placing_point_right
    
    if "vertical_2" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["vertical_2"]["number"])
        rebar_sizing = int(rebar_options["vertical_2"]["size"])
        
        # get location start - end vertical
        loc_start = locy + covering + (rebar_sizing/2.00) # +- diameter
        loc_end = locy + d - (rebar_sizing/2.00) - covering # +- diameter
        loc_x_right =  w + locx - covering - (rebar_sizing/2.00)*2 - rebar_sizing
        loc_x_left =  locx + covering + (rebar_sizing/2.00)*2 + rebar_sizing
        
        placing_point_right = [[i , loc_x_right] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point_right:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
        placing_point_left = [[i , loc_x_left] for i in numpy.linspace(loc_start , loc_end , num=number_of_rebar , endpoint=True)]
        for i in placing_point_left:
            msp.add_circle(center=(i[0],i[1]),radius=rebar_sizing/2.00,dxfattribs={'layer': 'REBAR'})
        
    
    if "stirrup_2A" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["stirrup_2A"]["number"])
        rebar_sizing = int(rebar_options["stirrup_2A"]["size"])
        
        center_x = ((locx + w)/2.00 , (locy+d) - covering - (rebar_sizing/2.00)) #1,8
        center_y = ((locx) + covering + (rebar_sizing/2.00) , (locy + d)/2.00) #2,3
        
        center_x_bottom = ((locx + w)/2.00 , (locy) + covering + (rebar_sizing/2.00)) #1,8
        center_y_right = ((locx + w) - covering - (rebar_sizing/2.00) , (locy + d)/2.00) #2,3
        
        point_1 = (center_x[0]-(rebar_sizing/2.00) , center_x[1])
        point_2 = (center_y[0] , center_x[1] +(rebar_sizing/2.00))
        
        point_3 = (center_y[0] , center_x[1] -(rebar_sizing/2.00))
        point_4 = (center_x_bottom[0]-(rebar_sizing/2.00) , center_x_bottom[1])
        
        point_5 = (center_x_bottom[0]+(rebar_sizing/2.00) , center_x_bottom[1])
        point_6 = (center_y_right[0] , center_y_right[1] -(rebar_sizing/2.00))
        
        point_7 = (center_y_right[0] , center_y_right[1] -(rebar_sizing/2.00))
        point_8 = (center_x[0]+(rebar_sizing/2.00) , center_x[1])
        
        msp.add_line(start=point_1,end= point_2)
        msp.add_line(start=point_3,end= point_4)
        msp.add_line(start=point_5,end= point_6)
        msp.add_line(start=point_7,end= point_8)
        
        if len(placing_point_horizontal) < 3:
            raise Exception("Sorry, unable to reinforce ST. type 3A , main rebar too less")
        
    # currently dev
    if "stirrup_2B" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["stirrup_2B"]["number"])
        rebar_sizing = int(rebar_options["stirrup_2B"]["size"])
        
        if 5 <= len(placing_point_horizontal) <= 8:
            rebar_point_1 = placing_point_horizontal[1]
            rebar_point_2 = placing_point_horizontal[-2]
        
        elif 9 <= len(placing_point_horizontal) :
            rebar_point_1 = placing_point_horizontal[2]
            rebar_point_2 = placing_point_horizontal[-3]
    
    if "stirrup_3A" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["stirrup_3A"]["number"])
        rebar_sizing = int(rebar_options["stirrup_3A"]["size"])
        
        if 6 <= len(placing_point_horizontal) <= 8:
            rebar_point_1 = placing_point_horizontal[1]
            rebar_point_2 = placing_point_horizontal[-2]
        
        elif 9 <= len(placing_point_horizontal) :
            rebar_point_1 = placing_point_horizontal[2]
            rebar_point_2 = placing_point_horizontal[-3]
            
        else:
            raise Exception("Sorry, unable to reinforce ST. type 3A , main rebar too less")
    
    if "stirrup_3B" in rebar_options.keys():
        
        number_of_rebar = int(rebar_options["stirrup_3B"]["number"])
        rebar_sizing = int(rebar_options["stirrup_3B"]["size"])
        
        if 5 <= len(placing_point_vertical) <= 8:
            rebar_point_1 = placing_point_vertical[1]
            rebar_point_2 = placing_point_vertical[-2]
        
        elif 9 <= len(placing_point_vertical) :
            rebar_point_1 = placing_point_vertical[2]
            rebar_point_2 = placing_point_vertical[-3]