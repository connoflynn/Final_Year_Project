from shapely.geometry import Polygon

# if area of overlap is greater than (area of space/a threshold percentage) then return true
threshold = 0.35

# function to check if each space is occupied and to add occupied tag to space_dict
def get_occupied(spaces_dict, Cars):
	for space in spaces_dict["spaces"]:
		co_ordinates = space["co_ordinates"]
		occupied = False
		for car in Cars:
			p1 = Polygon(car)
			p2 = Polygon(co_ordinates)
			overlap = findOverlap(p1,p2)
			if overlap == True:
				occupied = True
		
		# add occupied to space dict
		if occupied == True:
			space["occupied"] = 1
		else:
			space["occupied"] = 0

	# return updated dict with occupied key
	return spaces_dict



# find if two boxes overlap with eachother
def findOverlap(box1, box2):
	global threshold
	# make sure there is an overlap
	if box1.intersection(box2).area > 0.0:
		#if the intersection area divided by the area of the space is greater than the threshold
		if ((box1.intersection(box2).area)/(box2.area)) > threshold:
			return True
		else:
			return False
	else:
		return False