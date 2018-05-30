# PeterHuang@NCTU

import numpy as np
import os
from PIL import Image, ImageDraw

import xmltodict

# This function help you to parse MIT LabelMe annotation into polygon list.
# Input: xml_path(This should give xml absolute file path), product(This should give the object labeled name in LabelMe)
# Output: file_exist(0 for xml file is not exists or label be deleted, 1 for xml file exists and has labeled), xpts(list for polygon x locations in order), ypts(list for polygon y locations in order)

def xml2dict(xml_path, product):

	file_exist = os.path.isfile(xml_path)    # True
	# print xml_path
	pts = []
	xpts = []
	ypts = []

	if file_exist:

		with open(xml_path) as fd:
			label_dict = xmltodict.parse(fd.read())
	else: 
	
		return file_exist, xpts, ypts


	
	try:
		for object_ in label_dict['annotation']['object']:	
			if object_['name'] == product  and object_['deleted'] == '0':
				pts.append(object_['polygon']['pt'])

				for pts_idx in range(0,len(object_['polygon']['pt'])):
					xpts.append(int(object_['polygon']['pt'][pts_idx]['x']))
					ypts.append(int(object_['polygon']['pt'][pts_idx]['y']))

	except:

		try: ## xml exist and have label
			object_ = label_dict['annotation']['object']
			#print object_
			if object_['name'] == product  and object_['deleted'] == '0':
				
				#print object_['polygon']['pt']			
				pts.append(object_['polygon']['pt'])
				# print pts
				for pts_idx in range(0,len(object_['polygon']['pt'])):
					xpts.append(int(object_['polygon']['pt'][pts_idx]['x']))
					ypts.append(int(object_['polygon']['pt'][pts_idx]['y']))

				return file_exist, xpts,ypts


			else: #xml exist, labeld has been deleted
				xpts = []
				ypts = []
				file_exist = False
				return file_exist, xpts, ypts
			



		except: ## xml exist, but no label polygon
			xpts = []
			ypts = []
			file_exist = False
			return file_exist, xpts, ypts
	

	else:
		file_exist = False
		return file_exist, xpts, ypts

# This function help you to prepare polygon format needed by PIL, But you should check mixed_x_y is empty or not before calling poly2mask function.
def merge_x_y_pts(file_exist, xpts, ypts):
	mixed_x_y = []
	if file_exist:
		for pt_idx in range(0,len(xpts)):
			mixed_x_y.append(xpts[pt_idx])
			mixed_x_y.append(ypts[pt_idx])
			
	return mixed_x_y



# This function help you to return a mask, In this mask, only the pixels in bounding box area are set to 255, other pixels are set to 0.
def poly2mask(mixed_x_y, fill_value=255):
	width = 640
	height = 480
	img = Image.new('L', (width, height), 0)
	ImageDraw.Draw(img).polygon(mixed_x_y, outline=1, fill=fill_value)
	mask = np.array(img)
	return mask
