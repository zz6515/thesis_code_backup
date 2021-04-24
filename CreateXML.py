from xml.dom import minidom
import os
def createXML(_filename,_width,_height,_depth,_name,data):
    dom = minidom.Document()
    annotation = dom.createElement('annotation')

    filename = dom.createElement('filename')
    filename_text = dom.createTextNode(_filename)
    filename.appendChild(filename_text)
    source = dom.createElement('source')
    database = dom.createElement('database')
    database_text = dom.createTextNode('DIOR')
    database.appendChild(database_text)
    source.appendChild(database)

    size = dom.createElement('size')
    width = dom.createElement('width')
    height = dom.createElement('height')
    depth = dom.createElement('depth')

    width_text = dom.createTextNode(str(_width))
    height_text = dom.createTextNode(str(_height))
    depth_text = dom.createTextNode(str(_depth))
    width.appendChild(width_text)
    height.appendChild(height_text)
    depth.appendChild(depth_text)
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)

    segmented = dom.createElement('segmented')
    segmented_text = dom.createTextNode('0')
    segmented.appendChild(segmented_text)

    annotation.appendChild(filename)
    annotation.appendChild(source)
    annotation.appendChild(size)
    annotation.appendChild(segmented)
    for index,solo_data in enumerate(data):
        print("now",index)
        __xmin, __ymin, __xmax, __ymax =solo_data
        object = dom.createElement('object')
        name = dom.createElement('name')
        name_text = dom.createTextNode(_name)
        name.appendChild(name_text)

        pose = dom.createElement('pose')
        pose_text = dom.createTextNode('Unspecified')
        pose.appendChild(pose_text)

        bndbox = dom.createElement('bndbox')
        xmin = dom.createElement('xmin')
        xmin_text = dom.createTextNode(str(__xmin))
        xmin.appendChild(xmin_text)
        ymin = dom.createElement('ymin')
        ymin_text = dom.createTextNode(str(__ymin))
        ymin.appendChild(ymin_text)
        xmax = dom.createElement('xmax')
        xmax_text = dom.createTextNode(str(__xmax))
        xmax.appendChild(xmax_text)
        ymax = dom.createElement('ymax')
        ymax_text = dom.createTextNode(str(__ymax))
        ymax.appendChild(ymax_text)

        bndbox.appendChild(xmin)
        bndbox.appendChild(ymin)
        bndbox.appendChild(xmax)
        bndbox.appendChild(ymax)

        object.appendChild(name)
        object.appendChild(pose)
        object.appendChild(bndbox)

        annotation.appendChild(object)


    dom.appendChild(annotation)

    xmlname = os.path.splitext(_filename)[0]
    try:
        with open('DIOR/train/Annotations/'+xmlname+'.xml', 'w', encoding='UTF-8') as fh:
            dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
            print('OK')
    except Exception as err:
        print('错误：{err}'.format(err=err))
